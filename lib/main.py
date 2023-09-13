from sqlalchemy import String, Integer, MetaData, Table, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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
      return session.query(Review).filter(Review.restuarant.id==self.id).all()
    
    def customers(self, session):
      customer_ids=session.query(review.customer_id).filter(review.resturant_id==self).all()
      return [session.query(Customers).get(customer_id[0]) for customer_id in customer_ids]


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

    def __repr__(self):
        return f"CUSTOMER: {self.first_name} {self.last_name}"

   