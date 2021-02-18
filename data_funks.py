import pymongo


db_client = pymongo.MongoClient("mongodb://localhost:27017")
db = db_client["gb_data_mining_15_02_2021"]
collection = db["magnit_products"]

template_data = {"some_name": "hello", "2": 22212}
collection.insert_one(template_data)
for product in collection.find(
    {"$or": [{"title": {"$regex": "[Ш|ш]околад"}}, {"promo_name": "Дари играя"}]}
):
    print(product)
