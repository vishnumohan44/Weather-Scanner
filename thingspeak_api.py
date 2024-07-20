import requests
import csv

# Define your ThingSpeak channel ID and API key
channel_id = ""
api_key = ""

# Define the URL for reading data from ThingSpeak
url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={api_key}&results=10"

# Make GET request to fetch data
response = requests.get(url)

# Check if request was successful (status code 200)
while response.status_code == 200:
    # Parse JSON response
    data = response.json()
    # Extract relevant data (e.g., field1, field2, field3)
    feeds = data['feeds']
    
    # Append data to CSV file
    with open('temperature.csv', 'a', newline='') as csvfile:
        fieldnames = ['Temperature']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write data to CSV file
        for feed in feeds:
            temperature = feed['field1']
            writer.writerow({'Temperature': temperature})
    
    with open('humidity.csv', 'a', newline='') as csvfile:
        fieldnames = ['Humidity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write data to CSV file
        for feed in feeds:
            humidity = feed['field2']
            writer.writerow({'Humidity': humidity})

    with open('pressure.csv', 'a', newline='') as csvfile:
        fieldnames = ['Pressure']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write data to CSV file
        for feed in feeds:
            pressure = feed['field3']
            writer.writerow({'Pressure': pressure})

    response = requests.get(url)
    print("Data appended to CSV file successfully.")       

print("Data transfer has been terminated")