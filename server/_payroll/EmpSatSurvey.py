from nltk.sentiment import SentimentIntensityAnalyzer

# Load employee survey responses
survey_responses = [
    "The salary is satisfactory.",
    "The workload is manageable.",
    "I feel undervalued in this company."
]

# Perform sentiment analysis
sid = SentimentIntensityAnalyzer()
sentiment_scores = [sid.polarity_scores(response)['compound'] for response in survey_responses]

# Analyze sentiment scores
average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
if average_sentiment > 0.5:
    print("Employees are generally satisfied.")
elif average_sentiment < -0.5:
    print("There are significant concerns among employees.")
else:
    print("Employee sentiment is mixed.")
