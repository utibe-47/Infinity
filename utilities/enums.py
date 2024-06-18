from enum import Enum, unique


@unique
class DayStrings(Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


@unique
class LeadDirection(Enum):
    Hold = 0
    Buy = 1
    Sell = 2
