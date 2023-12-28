from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    # serialization rules
    serialize_rules = ('-reviews.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    # a relationship named reviews that establishes a relationship with the Review model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review.
    reviews = db.relationship('Review', back_populates='customer')

    # add an association proxy named items to get a list of items through the customer's reviews relationship.
    items = association_proxy('reviews', 'item', creator=lambda item_obj: Review(item=item_obj) )

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'
    
    


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    # serialization rules
    serialize_rules = ('-reviews.item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # a relationship named reviews that establishes a relationship with the Review model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Review
    reviews = db.relationship('Review', back_populates='item')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__= 'reviews'

    # serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews',)

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign key to store customer id
    customer_id= db.Column(db.Integer, db.ForeignKey('customers.id'))
    # Foreign key to store item id
    item_id = db.Column(db.Integer,db.ForeignKey('items.id'))
    
    # Relationship named customer that establishes a relationship with the Customer model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Customer.
    customer = db.relationship('Customer', back_populates='reviews')

    # a relationship named item that establishes a relationship with the Item model. Assign the back_populates parameter to match the property name defined to the reciprocal relationship in Item.
    item = db.relationship('Item', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, {self.customer_id}, {self.item_id}>'
