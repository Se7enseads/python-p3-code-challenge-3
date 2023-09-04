#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Restaurant, Customer, Review

if __name__ == '__main__':
    engine = create_engine('sqlite:///restaurant.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    fake = Faker()

    restaurants = []
    for i in range(10):
        restaurant = Restaurant(
            name=fake.unique.name(),
            price=random.randint(1000, 7500),
        )

        session.add(restaurant)
        restaurants.append(restaurant)

    customers = []
    for i in range(10):
        customer = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

        session.add(customer)
        customers.append(customer)

    reviews = []
    for restaurant in restaurants:
        for i in range(random.randint(1, 5)):
            review = Review(
                star_rating=random.randint(1, 10),
                restaurant_id=random.randint(1, 10),
                customer_id=random.randint(1, 10),
            )

            session.add(review)
            reviews.append(review)

    session.bulk_save_objects(restaurants, customers, reviews)
    session.commit()
