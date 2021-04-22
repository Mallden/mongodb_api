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

