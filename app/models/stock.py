"""
Inventory_Item model for managing stock
"""
from typing import Any
from mongoengine import Document, StringField, IntField, FloatField
from datetime import datetime

class Stock(Document):
    id: Any
    product_name = StringField(required=True, unique=True)
    available_quantity = IntField(required=True, default=0, min_value=0)
    reserved_quantity= IntField(default=0, min_value=0)
    price=FloatField(default=0,min_value=0)
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'product_id': str(self.id),
            'product_name': str(self.product_name),
            'available_quantity': self.available_quantity,
            'reserved_quantity': self.reserved_quantity,
            'price':self.price
        }
