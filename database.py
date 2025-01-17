import pymongo
import os
from bson import ObjectId
import numpy as np



mongodb_url = ""

client = pymongo.MongoClient(mongodb_url)

Db = 'amazon_product'
collection = 'product'
db = client[Db]
col = db[collection]

def GetProduct(limit=100):
    pipeline = [
        {"$sample": {"size": limit}},
        
    ]
    return list(col.aggregate(pipeline))

def GetProductById(id):
    projection = {'plot_embedding': False}
    return col.find_one({'product_id': id})
def vectorSearch(title,limit=10):
    result=db.product.aggregate([
    {
        "$vectorSearch": {
        "index": "vector_index",
        "path": "plot_embedding",
        "queryVector": title,
        "numCandidates": 100,
        "limit": limit
        }
    }
    ])

    return list(result)
def homeRecommendation(clicked_product_ids, limit=10):
    
    embeddings = []
    for product_id in clicked_product_ids:
        product = GetProductById(int(product_id))
        if product and 'plot_embedding' in product:
            embeddings.append(product['plot_embedding'])
    
    avg_embedding = np.mean(embeddings, axis=0).tolist()
    
    result = db.product.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "plot_embedding",
                "queryVector": avg_embedding,
                "numCandidates": 100,
                "limit": limit
            }
        },
        {
            "$project": {
                "plot_embedding": 0  # Exclude plot_embedding from results
            }
        }
    ])
    
    return list(result)
    
    