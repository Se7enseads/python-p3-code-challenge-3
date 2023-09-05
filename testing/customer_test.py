import unittest


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from lib.models import Customer, Restaurant


class TestCustomer(unittest.TestCase):

    def setUp(self):
        # Create a SQLAlchemy engine and session for testing
        engine = create_engine('sqlite:///restaurant.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        # Clean up resources after each test
        self.session.close()

    def test_query(self):
        # Query the customer with id 5
        customer = self.session.query(Customer).filter_by(id=5).first()

        # Check if the customer matches the expected string representation
        expected_customer_str = "<Customer:    id:5    first_name:Norma    last_name:Russell>"
        self.assertEqual(repr(customer), expected_customer_str)


if __name__ == "__main__":
    unittest.main()