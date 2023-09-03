from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///restaurant.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(Integer)

    reviews_relationship = relationship('Review', back_populates='restaurant')

    customers = relationship('Customer', secondary='reviews', back_populates='restaurants', viewonly=True)

    def get_reviews(self):
        return self.reviews_relationship

    def get_customers(self):
        return set([review.customer for review in self.reviews_relationship])

    def __repr__(self):
        return f'<Restaurant:    id:{self.id}    name:{self.name}    price:{self.price}>\n'

class Customer(Base):
    __tablename__= 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(10))
    last_name = Column(String(10))

    reviews_relationship = relationship('Review', back_populates='customer')

    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers', viewonly=True)

    def get_reviews(self):
        return self.reviews_relationship

    def get_restaurants(self):
        return set([review.restaurant for review in self.reviews_relationship])

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        reviews = [review for review in self.get_reviews()]
        if reviews:
            max_rating = max(reviews, key=lambda r: r.star_rating)
            return f"This is {self.full_name()}'s favorite restaurant: {max_rating.restaurant.name} id:{max_rating.restaurant.id}"
        else:
            return f"{self.full_name()} has no favorite restaurant"  

    def add_review(self, restaurant, rating):
        new_review = Review(star_rating=rating, restaurant_id=restaurant.id, customer_id=self.id)

        session.add(new_review)
        session.commit()

        return new_review
    
    def delete_reviews(self, restaurant):
        for review in self.reviews_relationship:
            if review.restaurant == restaurant:
                session.delete(review)
        session.commit()  

    def __repr__(self):
         return f'<Customer:    id:{self.id}    first_name:{self.first_name}    last_name:{self.last_name}>\n'

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    restaurant = relationship('Restaurant', back_populates='reviews_relationship')
    customer = relationship('Customer', back_populates='reviews_relationship')

    def get_customer(self):
        return self.customer

    def get_restaurant(self):
        return self.restaurant

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

    def __repr__(self):
        return f'<Review:    id:{self.id}    star_rating:{self.star_rating}    restaurant_id:{self.restaurant_id}    customer_id:{self.customer_id}>\n'
