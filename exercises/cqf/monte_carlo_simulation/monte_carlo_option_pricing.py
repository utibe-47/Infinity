from typing import List, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, field_validator

# Set max row to 300
pd.set_option('display.max_rows', 300)


class MonteCarloOptionPricing(BaseModel):

    S0: float = Field(..., gt=0, description="Initial stock price")
    K: float = Field(..., gt=0, alias="strike", description="Strike price")
    r: float = Field(..., ge=0, le=1, alias="rate", description="Risk-free rate")
    sigma: float = Field(..., gt=0, le=1, description="Volatility")
    T: int = Field(..., gt=0, le=3650, alias="dte", description="Days to expiration")
    N: int = Field(..., gt=0, alias="nsim", description="Number of simulations")
    ts: int = Field(252, gt=0, alias="timesteps", description="Number of timesteps")

    class Config:
        allow_population_by_field_name = True

    # alternate way to validate
    # @validator('T')
    # def check_T(cls, v):
    #     if v > 365 * 10:  # Assuming max 10 years
    #         raise ValueError("Days to expiration should not exceed 3650 (10 years)")
    #     return v

    @field_validator('N')
    def check_n(cls, v):
        if v > 1_000_000:  # Assuming max 1 million simulations
            raise ValueError("Number of simulations should not exceed 1,000,000")
        return v

    @property
    def df(self) -> float:
        return np.exp(-self.r * self.T)

    @property
    def pseudorandomnumber(self) -> np.ndarray:
        return np.random.standard_normal(self.N)

    @property
    def simulatepath(self) -> np.ndarray:
        """Simulate price path"""
        np.random.seed(2024)

        dt = self.T / self.ts

        s = np.zeros((self.ts, self.N))
        s[0] = self.S0

        for i in range(0, self.ts - 1):
            w = self.pseudorandomnumber
            s[i + 1] = s[i] * (1 + self.r * dt + self.sigma * np.sqrt(dt) * w)

        return s

    @property
    def vanillaoption(self) -> List[float]:
        """Calculate vanilla option payoff"""
        s = self.simulatepath

        vanilla_call = self.df * np.mean(np.maximum(0, s[-1] - self.K))
        vanilla_put = self.df * np.mean(np.maximum(0, self.K - s[-1]))

        return [vanilla_call, vanilla_put]

    @property
    def asianoption(self) -> List[float]:
        """Calculate asian option payoff"""
        s = self.simulatepath

        a = s.mean(axis=0)

        asian_call = self.df * np.mean(np.maximum(0, a - self.K))
        asian_put = self.df * np.mean(np.maximum(0, self.K - a))

        return [asian_call, asian_put]

    def upandoutcall(self, barrier: int = 150, rebate: int = 0) -> Tuple[float, float]:
        """Calculate up-and-out call option payoff"""
        s = self.simulatepath

        # Barrier shift
        barriershift = barrier * np.exp(0.5826 * self.sigma * np.sqrt(self.T / self.ts))

        value = 0
        for i in range(self.N):
            if s[:, i].max() < barriershift:
                value += np.maximum(0, s[-1, i] - self.K)
            else:
                value += rebate

        return self.df * value / self.N, barriershift
