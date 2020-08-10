# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class SoldadoxPipeline:
    def __init__(self):
        # iniciar a conxao com o mongo
        self.client = MongoClient('mongodb://root:c7c0d4c335ddef9c6094b655c39805e4@127.0.0.1')
        self.db = self.client.soldadox


    def process_item(self, item, spider):

        try:

            if "category" in item:
                self.db[item['category'].replace(" ","_")].insert(dict(item))

        except Exception as ex:
            self.db['errors'].insert(dict(ex))

        return item
