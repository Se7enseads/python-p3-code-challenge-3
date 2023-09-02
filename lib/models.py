from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///restaurants.db')
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(Integer)

    reviews = relationship('Review', back_populates='restaurant')

    customers = relationship('Customer', secondary='reviews', back_populates='restaurants', viewonly=True)

    def __repr__(self):
        return f'<Restaurant: {self.id} {self.name} {self.price}>'

class Customer(Base):
    __tablename__= 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(10))
    last_name = Column(String(10))

    reviews = relationship('Review', back_populates='customer')

    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers', viewonly=True)

    def __repr__(self):
         return f'<Customer: {self.id} {self.first_name} {self.last_name}>'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def __repr__(self):
        return f'<Review: {self.id} {self.star_rating} {self.restaurant_id} {self.customer_id}>'
