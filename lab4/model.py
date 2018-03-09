import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base

 
Base = declarative_base()


class Wallet(Base):
    __table__ = Table('wallet', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('address',String(250), nullable = False),
    Column('balance',Integer, nullable= False),
    Column('public_key',String(250), nullable = False)
    )
 

