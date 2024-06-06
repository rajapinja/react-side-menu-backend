import requests

# Define your Wix Booking API endpoint and API key
wix_booking_api_url = 'https://www.wixapis.com/wix-booking/v1'
api_key = 'your_api_key_here'

# Set headers with the API key and content type
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Sample function to retrieve bookings from Wix Booking
def get_bookings():
    try:
        # Make a GET request to retrieve bookings
        response = requests.get(f'{wix_booking_api_url}/bookings', headers=headers)

        if response.status_code == 200:
            bookings = response.json()
            return bookings
        else:
            print(f'Error: {response.status_code} - {response.text}')
            return None

    except Exception as e:
        print(f'An error occurred: {e}')
        return None

# Sample function to create a booking in Wix Booking
def create_booking():
    booking_data = {
        # Define the data for the new booking
        # Adjust the data structure to match your needs
    }

    try:
        # Make a POST request to create a booking
        response = requests.post(f'{wix_booking_api_url}/bookings', headers=headers, json=booking_data)

        if response.status_code == 201:
            new_booking = response.json()
            return new_booking
        else:
            print(f'Error: {response.status_code} - {response.text}')
            return None

    except Exception as e:
        print(f'An error occurred: {e}')
        return None

# Example usage:
# bookings = get_bookings()
# if bookings:
#     print("Retrieved bookings:")
#     print(bookings)

# new_booking = create_booking()
# if new_booking:
#     print("Created a new booking:")
#     print(new_booking)
