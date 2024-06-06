import nltk
import random
from nltk.chat.util import Chat, reflections

# Define conversation patterns and responses
patterns = [
    (r'(.*)salary(.*)', ['Your salary for this month is $5000.']),
    (r'(.*)update(.*)', ['Please provide your updated personal information.']),
    (r'(.*)leave(.*)', ['Please submit a leave request through the HR portal.']),
    (r'(.*)feedback(.*)', ['Thank you for your feedback! Your opinion is valuable to us.']),
    (r'(.*)survey(.*)', ['Sure, I can help you with the survey. What is your feedback?']),
    (r'(.*)', ["I'm sorry, I didn't understand that. Could you please rephrase?"])
]


# Create chatbot
chatbot = Chat(patterns, reflections)

# Function to start conversation
def start_chat():
    print("Employee Chatbot: Hello! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Employee Chatbot: Goodbye!")
            break
        else:
            response = chatbot.respond(user_input)
            print("Employee Chatbot:", random.choice(response))

# Start conversation
start_chat()
