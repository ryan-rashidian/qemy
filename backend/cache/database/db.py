from sqlalchemy import create_engine, Integer, String, Float, Column, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///qemy_data.db', echo=True)

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, unique=True)
    name = Column(String)
    sector = Column(String) 
    industry = Column(String)

    price_history = relationship('price_history', back_populates='company')
#    financials = relationship('financials', back_populates='company')

class PriceHistory(Base):
    __tablename__ = 'price_history'
    ticker = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    close = Column(Float)
    owner = Column(Integer, ForeignKey('company.id'))

    company = relationship('company', back_populates='price_history')

#class Financial(Base):
#    __tablename__ = 'financials'
#    id = Column(Integer, primary_key=True)
#
#    company = relationship('company', back_populates='financials')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
