import pymongo
from mongoengine import *


class Companies(Document):
    portal_id = IntField(required=True)
    title = StringField(max_length=250, required=True)
    paid = BooleanField(default=False)


class Products(Document):
    _id = ObjectIdField()
    portal_id = IntField(required=True)
    hide = BooleanField(default=False)
    created = StringField(max_length=255, required=True)
    ts = StringField(max_length=255, required=True)
    unit = IntField()
    title = StringField(max_length=255, required=True)
    section_id = IntField(required=True)
    other_shop = StringField(max_length=255, required=True)
    company_id = IntField(required=True)
    status = IntField(required=True)
    price = IntField(required=True)
    product_model_id = IntField(required=True)
    description = StringField(max_length=255)
    brand_id = IntField()
    description_tag = StringField(max_length=255)
    article = StringField(max_length=255)
    yml_pricelist_id = IntField()
    product_url = StringField(max_length=255, required=True)
    showcase = BooleanField(default=False)
    company_collection = ReferenceField(Companies, reverse_delete_rule=CASCADE)
