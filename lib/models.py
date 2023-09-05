from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///restaurant.db')
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


# Define the Restaurant class with SQLAlchemy ORM
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(Integer)

    # Define relationships with Review and Customer
    reviews_relationship = relationship('Review', back_populates='restaurant')

    customers = relationship(
        'Customer',
        secondary='reviews',
        back_populates='restaurants',
        viewonly=True)

    def get_reviews(self):
        # Return all reviews associated with this restaurant
        return self.reviews_relationship

    def get_customers(self):
        # Return all customers who have reviewed this restaurant
        return set([review.customer for review in self.reviews_relationship])

    @classmethod
    def fanciest(cls):
        # Find the fanciest restaurant based on price
        all_restaurants = session.query(cls).all()

        f_restaurant = session.query(Restaurant).order_by(
            Restaurant.price.desc()).first()
        return f'The fanciest restaurant is {f_restaurant.name}.'

    def all_reviews(self):
        # Retrieve all reviews for the restaurant and return them
        reviews = [review.full_review() for review in self.reviews_relationship]
        return reviews

    def __repr__(self):
        return f'<Restaurant:    id:{self.id}    name:{self.name}    price:{self.price}>\n'


# Define the Customer class with SQLAlchemy ORM
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(10))
    last_name = Column(String(10))

    # Define relationships with Review and Restaurant
    reviews_relationship = relationship('Review', back_populates='customer')

    restaurants = relationship(
        'Restaurant',
        secondary='reviews',
        back_populates='customers',
        viewonly=True)

    def get_reviews(self):
        # Return all reviews written by this customer
        return self.reviews_relationship

    def get_restaurants(self):
        # Return all restaurants that this customer has reviewed
        return set([review.restaurant for review in self.reviews_relationship])

    def full_name(self):
        # Return the full name of the customer
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        reviews = [review for review in self.get_reviews()]
        if reviews:
            # Find the review with the highest star rating and return the favorite restaurant
            max_rating = max(reviews, key=lambda r: r.star_rating)
            return f"This is {self.full_name()}'s favorite restaurant: {max_rating.restaurant.name} id:{max_rating.restaurant.id}"
        else:
            return f"{self.full_name()} has no favorite restaurant"

    def add_review(self, restaurant, rating):
        # Create a new review, add it to the session, and commit it to the database
        new_review = Review(
            star_rating=rating,
            restaurant_id=restaurant,
            customer_id=self.id)

        session.add(new_review)
        session.commit()

        return new_review

    def delete_reviews(self, restaurant):
        # Delete reviews associated with a specific restaurant for this  customer
        for review in self.reviews_relationship:
            if review.restaurant == restaurant:
                session.delete(review)
        session.commit()

    def __repr__(self):
        return f'<Customer:    id:{self.id}    first_name:{self.first_name}    last_name:{self.last_name}>\n'


# Define the Review class with SQLAlchemy ORM
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)

    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    # Define relationships with Restaurant and Customer
    restaurant = relationship(
        'Restaurant', back_populates='reviews_relationship')
    customer = relationship('Customer', back_populates='reviews_relationship')

    def get_customer(self):
        # Return the associated customer for this review
        return self.customer

    def get_restaurant(self):
        # Return the associated restaurant for this review
        return self.restaurant

    def full_review(self):
        # Conditionally render 'star' or 'stars' based on the star rating
        stars_word = "star" if self.star_rating == 1 else "stars"
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} {stars_word}"

    def __repr__(self):
        return f'<Review:    id:{self.id}    star_rating:{self.star_rating}    restaurant_id:{self.restaurant_id}    customer_id:{self.customer_id}>\n'