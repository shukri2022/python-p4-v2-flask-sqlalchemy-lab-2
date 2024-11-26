from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # Relationships
    reviews = db.relationship(
        "Review", back_populates="customer", cascade="all, delete-orphan"
    )
    items = association_proxy("reviews", "item")

    # Serialization Rules
    serialize_rules = ("-reviews.customer",)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"


class Item(db.Model, SerializerMixin):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Relationships
    reviews = db.relationship(
        "Review", back_populates="item", cascade="all, delete-orphan"
    )

    # Serialization Rules
    serialize_rules = ("-reviews.item",)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"


class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True)

    # Relationships
    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")

    # Serialization Rules
    serialize_rules = ("-customer.reviews", "-item.reviews")

    def __init__(self, comment=None, customer=None, item=None):
        self.comment = comment
        self.customer = customer
        self.item = item

    def __repr__(self):
        return (
            f"<Review {self.id}, Customer {self.customer_id}, Item {self.item_id}, "
            f"Comment {self.comment}>"
        )
