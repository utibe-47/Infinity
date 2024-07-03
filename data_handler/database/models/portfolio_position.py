from datetime import datetime
from data_handler.database import db, Base


class PortfolioPositions(Base):
    __tablename__ = 'portfolio_positions'
    Id = db.Column(db.Integer(), primary_key=True, unique=True)
    Date = db.Column(db.DateTime(timezone=False), nullable=False, default=datetime.now())
    LeadDirection = db.Column(db.String(32))
    Lead = db.Column(db.String(32))
    NonLead = db.Column(db.String(32))
    Security = db.Column(db.String(255))
    PositionTarget = db.Column(db.Float(), default=0.0)
    Protection = db.Column(db.String(255))
    Strategy = db.Column(db.String(255))


header = ['LeadDirection', 'Lead', 'NonLead', 'Security', 'Tenor', 'PositionTarget', 'Protection',
          'Account', 'Strategy', 'DealingDesk', 'InstrumentType', 'Strike', 'ReasonCode']


header_with_date = ['Date'] + header

header_csv = ['Lead Direction', 'Lead', 'Non-Lead', 'Future/Security', 'Tenor', 'Position Target',
              'Protection Buyer/Seller', 'Account', 'Strategy', 'Dealing Desk', 'Instrument Type', 'Strike',
              'ReasonCode']

header_csv_with_date = ['Date'] + header_csv
