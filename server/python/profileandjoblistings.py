import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymongo
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for your entire Flask app

# Connect to MongoDB
mongo_client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
db = mongo_client['collaboration']

# Retrieve data from MongoDB collections
joblistings_collection = db['joblistings']
profiles_collection = db['profiles']

job_listings_data = list(joblistings_collection.find())
freelancers_data = list(profiles_collection.find())

#print("job_listings_data :", job_listings_data)

# Create DataFrames from MongoDB data
job_listings = pd.DataFrame(job_listings_data)
freelancers = pd.DataFrame(freelancers_data)

# Convert job listings and freelancer skills to text for skill matching
job_skills_text = [' '.join(skills) for skills in job_listings['skills_required']]
freelancer_skills_text = [' '.join(skills) for skills in freelancers['skills']]

# Vectorize skills text using CountVectorizer
vectorizer = CountVectorizer().fit(job_skills_text + freelancer_skills_text)
job_skills_vectorized = vectorizer.transform(job_skills_text)
freelancer_skills_vectorized = vectorizer.transform(freelancer_skills_text)

# Compute cosine similarity between job listings and freelancer skills
similarity_matrix = cosine_similarity(freelancer_skills_vectorized, job_skills_vectorized)

# Create an empty list to store individual DataFrames
matches_list = []

# Iterate through each freelancer
for i, freelancer_id in enumerate(freelancers['freelancer_id']):
    # Find the job with the highest similarity score for the freelancer
    best_match_index = similarity_matrix[i].argmax()
    match_score = similarity_matrix[i, best_match_index]

    # Create a DataFrame for the current match
    match_df = pd.DataFrame({'freelancer_id': [freelancer_id], 'job_id': [job_listings['job_id'].iloc[best_match_index]], 'match_score': [match_score]})

    # Append the DataFrame to the list
    matches_list.append(match_df)

# Concatenate all the individual DataFrames into one DataFrame
matches = pd.concat(matches_list, ignore_index=True)

# Sort matches by match_score in descending order
matches = matches.sort_values(by='match_score', ascending=False)

# Display the top matches
print(matches)

@app.route('/api/get-matches', methods=['GET'])
def get_matches():
    #print("Inside get_matches...!")
    data_to_send = {"matches": matches.to_dict(orient='records')}  # Convert DataFrame to a list of dictionaries
    #print("data_to_send: ", {"matches": matches.to_dict(orient='records')})
    #print("matches.to_dict(orient='records') :", matches.to_dict(orient='records'))    
    return jsonify({"matches": data_to_send})

if __name__ == '__main__':
    app.run()  # Run the Flask app
