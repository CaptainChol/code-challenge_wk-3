from sqlalchemy import create_engine, MetaData
from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from main import Restaurant, Customers, Review, Base

if __name__ == "__main__":
    engine = create_engine("sqlite:///restuarant.db")
    metadata = MetaData()
    Base.metadata.create_all(engine)  
    Session = sessionmaker(bind=engine)
    session = Session()

    # session.query(Restaurant).delete()
    # session.query(Customers).delete() 
    # session.query(Review).delete()
    fake = Faker()

    customers=[]
    for i in range(50):
      customer=Customers(first_name=fake.first_name(), last_name=fake.last_name())
      session.add(customer)
      session.commit()
      customers.append(customer)

    restaurants =[]
    for i in range(25):
      restaurant = Restaurant(name=fake.company(), price=random.randint(10, 50))
      session.add(restaurant)
      session.commit()
      restaurants.append(restaurant)

    reviews = []
    for i in range(100):
      for customer in customers:
        review = Review(
        star_rating= random.randint(0,5),
        customer_id=customer.id,
        restaurant_id=restaurants[random.randint(0, len(restaurants)-1)].id
      )
      
      session.add(review)
      session.commit()
      
      reviews.append(review)