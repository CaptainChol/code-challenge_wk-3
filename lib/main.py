from sqlalchemy import String, Integer, MetaData, Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, func

metadata = MetaData()
Base = declarative_base(metadata=metadata)
engine = create_engine("sqlite:///restuarant.db")

restuarant_customer = Table(
    "resturant_customer",
    Base.metadata,
    Column("customer_id", Integer, ForeignKey("customers.id"), primary_key=True),
    Column("restaurant_id", Integer, ForeignKey("restaurants.id"), primary_key=True),
    extend_existing=True,
)

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    customers = relationship("Customers", secondary=restuarant_customer, back_populates="restaurants")

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"RESTAURANT: {self.name} {self.price}"

    def reviews(self, session):
        return session.query(Review).filter(Review.restaurant_id == self.id).all()

    def all_reviews(self, session):
        review_strings = []
        for review in self.reviews(session):
            customer_full_name = review.customer(session).full_name()
            star_rating = review.star_rating
            review_str = f"Review for {self.name} by {customer_full_name}: {star_rating} stars."
            review_strings.append(review_str)
        return review_strings

    @classmethod
    def fanciest(cls, session):
        return session.query(cls).order_by(cls.price.desc()).first()

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)

    def customer(self, session):
        return session.query(Customers).filter_by(id=self.customer_id).first()


    def restaurant(self, session):
        return session.query(Restaurant).filter_by(id=self.restaurant_id).first()

class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    restaurants = relationship("Restaurant", secondary=restuarant_customer, back_populates="customers")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_reviews(self, session):
        return session.query(Review).filter(Review.customer_id == self.id).all()

    def get_restaurants(self, session):
        restaurant_ids = session.query(Review.restaurant_id).filter(Review.customer_id == self.id).all()
        return [session.query(Restaurant).get(restaurant_id[0]) for restaurant_id in restaurant_ids]

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self, session):
        max_rating = session.query(func.max(Review.star_rating)).filter_by(customer_id=self.id).scalar()
        if max_rating is not None:
          favorite_review = (
            session.query(Review)
            .filter_by(customer_id=self.id, star_rating=max_rating)
            .first()
        )
        if favorite_review:
            return favorite_review.restaurant(session)
        return None


    def add_reviews(self, star_rating, restaurant_id, customer_id, session):
        rev = Review(star_rating=star_rating, restaurant_id=restaurant_id, customer_id=customer_id)
        session.add(rev)
        session.commit()
        return rev

    def delete_reviews(self, restaurant, session):
         session.query(Review).filter(
            (Review.customer_id == self.id) & ( Review.restaurant_id == restaurant.id)
        ).delete()
         session.commit() 

    def __repr__(self):
        return f"CUSTOMER: {self.first_name} {self.last_name}"
