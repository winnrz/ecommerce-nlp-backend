import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
#Activate venv: . .venv/bin/activate

def TFIDF(title):
    current_directory = os.path.dirname(__file__)
    json_file_path = os.path.join(current_directory, "api/models/products.json")

    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        products_data = json.load(file)

    # Extract the overview and name attributes into separate arrays
    product_descriptions = [product['description'] for product in products_data['products']]
    product_names = [product["name"] for product in products_data['products'] ]

    # Create a mapping between titles and their corresponding indices
    title_to_index = {title: idx for idx, title in enumerate(product_names)}

    # Ignores common English words in the text analysis
    tfidf = TfidfVectorizer(stop_words="english") 
    # Assigns a unique integer index to each word and calculates the Inverse Document Frequency (IDF) for each term in the vocabulary.
    tfidf_matrix = tfidf.fit_transform(product_descriptions)

    # Takes the matrices and creates a reference with each data value with the other (cosine similarity)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Create a mapping between titles and their corresponding indices
    title_to_index = {title: idx for idx, title in enumerate(product_names)}

    # Example usage to find the index of 'Avatar'
    avatar_index = title_to_index[title]
    
    idx = avatar_index
    sim_scores = enumerate(cosine_sim[idx])
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    sim_index = [i[0] for i in sim_scores]

    for index in sim_index:
        print(product_names[index])

# Call the function to test
TFIDF('Organza Flap Bag - Victory')





