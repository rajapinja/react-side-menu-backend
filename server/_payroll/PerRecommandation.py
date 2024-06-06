from sklearn.cluster import KMeans

# Load employee data
employee_data = pd.read_csv('employee_data.csv')

# Perform K-means clustering for segmentation
kmeans = KMeans(n_clusters=3)
clusters = kmeans.fit_predict(employee_data[['performance_score', 'tenure']])

# Generate personalized recommendations based on clusters
def generate_recommendations(cluster):
    if cluster == 0:
        return "Consider a performance bonus."
    elif cluster == 1:
        return "Offer additional training opportunities."
    else:
        return "Provide career advancement opportunities."

# Example usage
employee_data['recommendation'] = employee_data['cluster'].apply(generate_recommendations)
