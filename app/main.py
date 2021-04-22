import json
from typing import Dict
from fastapi import FastAPI, Query, Depends

from mongoengine import connect, disconnect

from app import settings
from app.models import Companies, Products

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome": "MongoDB API"}


@app.get("/search")
async def get_items(filter_items: dict):
    connect(host=settings.uri)
    sort_products = list()
    sort_filter = filter_items.pop('sort') if 'sort' in filter_items else None
    paid_companies = Companies.objects(paid=True) if sort_filter.get('paid_companies') else None
    paid_products = None
    try:
        for item in sort_filter.get('products'):
            sort_products.append(item['field'])
    except TypeError:
        pass

    filter_search = filter_items.copy()
    if paid_companies:
        filter_search['company_collection_in'] = paid_companies
        paid_products = Products.objects().filter(**filter_search).order_by(*sort_products)
        filter_search['company_collection_nin'] = paid_companies
        filter_search.pop('company_collection_in')

    if paid_products:
        not_paid_products = Products.objects().filter(**filter_search).order_by(*sort_products)
        products = paid_products + not_paid_products
    else:
        products = Products.objects().filter(**filter_search).order_by(*sort_products)
    disconnect()
    return products.to_json()


