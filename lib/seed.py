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
    # fake = Faker()

    # customers=[]
    # for i in range(50):
    #   customer=Customers(first_name=fake.first_name(), last_name=fake.last_name())
    #   session.add(customer)
    #   session.commit()
    #   customers.append(customer)

    # restaurants =[]
    # for i in range(25):
    #   restaurant = Restaurant(name=fake.company(), price=random.randint(10, 50))
    #   session.add(restaurant)
    #   session.commit()
    #   restaurants.append(restaurant)

    # reviews = []
    # for i in range(100):
    #   for customer in customers:
    #     review = Review(
    #     star_rating= random.randint(0,5),
    #     customer_id=customer.id,
    #     restaurant_id=restaurants[random.randint(0, len(restaurants)-1)].id
    #   )
      
    #   session.add(review)
    #   session.commit()
      
    #   reviews.append(review)
      
      
      # Retrieving All Reviews for a Restaurant   
    restaurant = session.query(Restaurant).filter_by(name="Davis PLC").first()
    if restaurant:
          print(f"Reviews for {restaurant.name}:")
          reviews = restaurant.all_reviews(session)
          for review in reviews:
              print(review)
    else:
          print("Restaurant not found.")
          
          
      # Finding the Fanciest Restaurant      
    
    fanciest = Restaurant.fanciest(session)
    if fanciest:
        print(f"The fanciest restaurant is {fanciest.name} with a price of {fanciest.price}")
    else:
        print("No restaurants found.")
          
      # Retrieving Customer Information for a Review   
    review = session.query(Review).first() 
    customer = review.customer(session)
    if customer:
          print(f"Customer for this review: {customer.full_name()}")
    else:
          print("Customer not found.") 
          
          
      # Retrieving Restaurant Information for a Review      
    restaurant = review.restaurant(session)
    if restaurant:
          print(f"Restaurant for this review: {restaurant.name}")
    else:
          print("Restaurant not found.")   
          
          
      #  Retrieving All Reviews Written by a Customer
    customer_reviews = customer.get_reviews(session)
    if customer_reviews:
          print(f"Reviews by {customer.full_name()}:")
          for review in customer_reviews:
              print(f"{review.restaurant(session).name}: {review.star_rating} stars")
              print("*" * 30)
    else:
          print(f"{customer.full_name()} hasn't written any reviews.")
          
          
      # Retrieving All Restaurants Reviewed by a Customer
    customer_restaurants = customer.get_restaurants(session)
    if customer_restaurants:
          print(f"Restaurants reviewed by {customer.full_name()}:")
          for restaurant in customer_restaurants:
              print(restaurant.name)
    else:
          print(f"{customer.full_name()} hasn't reviewed any restaurants.")
          
      #  Displaying the Full Name of a Customer    
    # full_name = customer.full_name()
    # print(f"Customer's Full Name: {full_name}") 
      
      
      # Finding a Customer's Favorite Restaurant      
    favorite = customer.favorite_restaurant(session)
    if favorite:
          print(f"{customer.full_name()}'s favorite restaurant is {favorite.name}")
    else:
          print(f"{customer.full_name()} hasn't reviewed any restaurants.") 
          
     
      # Adding a New Review   
    star_rating = 4  
    restaurant_id = restaurant.id
    customer_id = customer.id
    new_review = customer.add_reviews(star_rating, restaurant_id, customer_id, session)
    print(f"Review added with ID: {new_review.id}")  
      
      
    # Deleting a Review by a Customer  
    customer.delete_reviews(restaurant, session)
    print(f"Review by {customer.full_name()} for {restaurant.name} deleted.") 
         

          


