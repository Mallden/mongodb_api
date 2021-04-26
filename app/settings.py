import pymongo
import os

uri = f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASS')}@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/{os.getenv('MONGO_DB')}?authSource=admin"


class MongoClient:

    """
        Stand version pymongo search
        old settings, old realisation
    """

    def __init__(self):
        self.client = pymongo.MongoClient(
            os.getenv('MONGO_HOST'),
            port=27017,
            username='root',
            password='example'
        )
        self.db = self.client.stroyportal
        self.companies = self.db.companies
        self.products = self.db.products
        self.sort_filter, self.sort_companies =  None, None
        self.paid_companies = None
        self.sort_products = list()

    def search(self, filter_items):
        if "sort" in filter_items.keys():
            self.sort_filter = filter_items.pop('sort')
            self.sort_companies = self.sort_filter.get('companies')
            info_sort = self.sort_filter.get('products')
            try:
                for item in info_sort:
                    self.sort_products.append((item['field'], item['type_sort']))
            except TypeError:
                pass

        if self.sort_companies:
            self.paid_companies = [
                x['_id']
                for x in
                self.companies.find(
                    self.sort_companies,
                    {
                        "portal_id": 0,
                        "title": 0,
                        "paid": 0
                    }
                )
            ]
            filter_items['comp'] = self.paid_companies

        query = self.products.find(filter_items)

        if self.sort_products:
            query = query.sort(self.sort_products)


query_elastic = {
    'sort': [
        {'brandcorner': {'unmapped_type': 'boolean', 'order': 'desc'}},
        {'filials.only_delivery': {'order': 'asc'}},
        {'_script': {
            'type': 'number',
            'order': 'desc',
            'script': {
                'source': "if(doc['id'].value < 0) { 1 } else { 0 }"
            }
        }},
        {'_script': {
            'type': 'number',
            'order': 'desc',
            'script': {
                'source': "if(0 < doc['pack_num'].value) {1} else {0}"
            }
        }},
        {'stage_new': {
            'unmapped_type': 'integer',
            'order': 'asc'
        }},
        {'ctr_extra': {'order': 'desc', 'ignore_unmapped': True}}
    ],
    'ignore_exception': True,
    'vendor': [],
    'color': [],
    'in_stock': None,
    'with_brandcorner': True,
    'active': True,
    'price_range': None,
    'query_size': 30,
    'all_region': [1, 3, 4610, 7088, 7688],
    'fields': [
        'opt_prices_data',
        'childs',
        'currency',
        'list_count',
        'id',
        'unit',
        'title',
        'section',
        'section_type',
        'other_shop',
        'main_tag',
        'last_login',
        'section_str',
        'company',
        'status',
        'price',
        'in_stock',
        'vendor',
        'filials',
        'product_model',
        'product_model_title',
        'mobile_image_review',
        'detail_count',
        'nice',
        'order_call_count',
        'generated_image',
        'charasteristic_list',
        'pack_num',
        'product_model_url_title',
        'url_title',
        'pids',
        'brandcorner',
        'cost_click',
        'is_cpa'
    ],
    'section': [98],
    'search_phrase': None,
    'query_from': 0,
    'query_string': ''
}

query_mongo = {
    "sort": {
        "paid_companies": 1,
        "products": ["-ctr_extra"]
    },
    "hide": 0,
    "section_id": 98,
    "query_size": 30,
    "query_from": 0,
    "region_list__in": [1, 3, 4610, 7088, 7688]
}
