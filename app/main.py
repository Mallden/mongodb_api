import json
import time
from fastapi import FastAPI, Response, status

from mongoengine import connect, disconnect

from app import settings
from app.models import Companies, Products

app = FastAPI()


@app.get("/")
def read_root():
    return {"Welcome": "MongoDB API"}


@app.get("/search")
async def get_items(filter_items: str, response: Response):
    start = time.time()
    filter_items = json.loads(filter_items)
    result = {"message": "Success"}
    if not filter_items:
        response.status_code = status.HTTP_400_BAD_REQUEST
        response.content = {'error': 'empty query params'}
        return response
    connect(host=settings.uri)
    sort_products = list()
    sort_filter = filter_items.pop('sort') if 'sort' in filter_items else {}
    paid_companies = Companies.objects(paid=True) if sort_filter.get('paid_companies') else None
    paid_products = None
    try:
        for item in sort_filter.get('products'):
            sort_products.append(item)
    except TypeError:
        pass

    filter_search = filter_items.copy()
    query_size = filter_search.pop('query_size') if filter_search.get('query_size') else 30
    query_from = filter_search.pop('query_from') if filter_search.get('query_from') else 0
    try:
        filter_search.pop('query_from')
    except KeyError:
        pass
    filter_search['hide'] = True if filter_search.get('hide') else False
    query_to = query_from + query_size
    if paid_companies:
        filter_search['company_collection__in'] = paid_companies
        paid_products = Products.objects().filter(**filter_search).order_by(*sort_products)[query_from:query_to]
        query_to = query_to - len(paid_products)
        filter_search['company_collection__nin'] = paid_companies
        filter_search.pop('company_collection__in')

    if paid_products:
        not_paid_products = Products.objects().filter(**filter_search).order_by(*sort_products)[query_from:query_to]
        result["items_count"] = paid_products.count() + not_paid_products.count()
        result["items"] = json.loads(paid_products.to_json()) + json.loads(not_paid_products.to_json())
    else:
        products = Products.objects().filter(**filter_search).order_by(*sort_products)[query_from:query_to]
        result["items_count"] = products.count()
        result["items"] = json.loads(products.to_json())
    disconnect()
    stop = time.time() - start
    result['time_script'] = f"--- {stop} seconds ---"
    return result

