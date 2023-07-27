from pymongo.collection import Collection
from config import client, database_name

class RssDB:
    def __init__(self):
        self.files_col = Collection(client['RSS_FEED'], database_name)
        
    def find(self, data):
        return self.files_col.find_one(data)
    
    def full(self):
        return list(self.files_col.find())
    
    def range(self, offset, limit):
        return list(self.files_col.find().skip(offset).limit(limit))
    
    def rando(self, sample_size):
        pipeline = [
            { "$sample": { "size": sample_size } }
        ]
        return list(self.files_col.aggregate(pipeline))

    def count(self):
        return self.files_col.count_documents({})

    def add(self, data):
        try:
            self.files_col.insert_one(data)
        except:
            pass

    def remove(self, data):
        self.files_col.delete_one(data)