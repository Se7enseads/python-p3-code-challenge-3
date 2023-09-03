customer = Customer(first_name='Bad', last_name='Customer')
reveiw2 = Review(star_rating=0, customer_id=11, restaurant_id=3)

print(customer.favorite_restaurant())

customer = session.query(Customer).filter_by(id=5).first()
restaurant = session.query(Restaurant).filter_by(id=5).first()

customer.add_review(restaurant, rating=5)