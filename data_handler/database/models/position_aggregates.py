from datetime import datetime
from data_handler.database import db, Base


strategy_exposures_header = ['Strategy', 'Previous', 'Current', 'Change']
asset_class_exposures_header = ['AssetClass', 'Previous', 'Current', 'Change']
top_positions_by_exposures_header = ['Position', 'Exposure']
bottom_positions_by_exposures_header = ['Position', 'Exposure']


class StrategyExposures(Base):
    __tablename__ = 'strategy_exposures'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    Date = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    Strategy = db.Column(db.String(32))
    Previous = db.Column(db.Float(), default=0.0)
    Current = db.Column(db.Float(), default=0.0)
    Change = db.Column(db.Float(), default=0.0)


class AssetClassExposures(Base):
    __tablename__ = 'asset_class_exposures'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    Date = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    AssetClass = db.Column(db.String(32))
    Previous = db.Column(db.Float(), default=0.0)
    Current = db.Column(db.Float(), default=0.0)
    Change = db.Column(db.Float(), default=0.0)


class TopPositionByExposures(Base):
    __tablename__ = 'top_positions_by_exposures'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    Date = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    Position = db.Column(db.String(32))
    Exposure = db.Column(db.Float(), default=0.0)


class BottomPositionByExposures(Base):
    __tablename__ = 'bottom_positions_by_exposures'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    Date = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    Position = db.Column(db.String(32))
    Exposure = db.Column(db.Float(), default=0.0)
