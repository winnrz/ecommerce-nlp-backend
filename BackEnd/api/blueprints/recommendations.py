from flask_cors import cross_origin
from flask import Blueprint
from firebase_admin import db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import json

recommendations_bp = Blueprint('recommendations_bp', __name__)

@recommendations_bp.route('/<product_name>', methods=['GET'])
@cross_origin()
def recommendations(product_name):
    ref = db.reference("/products")
    products_list = ref.get()
    
    # Extract the overview and name attributes into separate arrays
    product_ids = [item['id'] for item in products_list]
    product_descriptions = [item['name'] for item in products_list]

    # Create a mapping between titles and their corresponding indices
    title_to_index = {title: idx for idx, title in enumerate(product_ids)}

    # Ignores common English words in the text analysis
    tfidf = TfidfVectorizer(stop_words="english") 
    # Assigns a unique integer index to each word and calculates the Inverse Document Frequency (IDF) for each term in the vocabulary.
    tfidf_matrix = tfidf.fit_transform(product_descriptions)

    # Takes the matrices and creates a reference with each data value with the other (cosine similarity)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Create a mapping between titles and their corresponding indices
    title_to_index = {title: idx for idx, title in enumerate(product_ids)}

    product_index = title_to_index[product_name]

    idx = product_index 
    sim_scores = enumerate(cosine_sim[idx])
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    sim_index = [i[0] for i in sim_scores]
    recommended_ids = []
    for index in sim_index:
        recommended_ids.append(product_ids[index])
        
    return recommended_ids

@recommendations_bp.route('/favicon.ico')
@cross_origin()
def favicon():
    return '', 204  # Return empty response with status code 204 (No Content) to ignore the favicon request

    

    