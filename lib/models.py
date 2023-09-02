#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///restaurants.db')

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(Integer)

    reviews = relationship('Review', backref='restaurant')

    customers = relationship('Customer', secondary='reviews', back_populates='restaurants')

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class Customer(Base):
    __tablename__= 'customers'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    reviews = relationship('Review', backref='customer')

    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

    def __repr__(self):
        return f'<Customer {self.name}>'


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(10))
    last_name = Column(String(10))

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    
    customer_id = Column(Integer, ForeignKey('customers.id'))

    def __repr__(self):
        return f'<Review {self.name}>'