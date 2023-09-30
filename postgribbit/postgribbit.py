import json
import requests
import psycopg2
import logging
import threading
import time
from flask import Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#pondpulse_url = os.environ['pondpulse_url']
# postgres_user = os.environ['POSTGRES_USER']
# postgres_pass = os.environ['POSTGRES_PASSWORD']
# postgres_dbname = os.environ['db_name']
# postgres_port = os.environ['db_port']


# PostgreSQL database configuration
db_config = {
    'dbname': 'mydb',
    'user': 'dbuser',
    'password': 'dbsecretpassword',
    'host': 'postgresql-service',
    'port': 5432
}

# Function to fetch data and store it in the database
def fetch_and_store_data():
    try:
        # Fetch data from the microservices URL
        response = requests.get("http://pondpulse-service/microservices")
        data = json.loads(response.text)
        logging.info(data)

        # Log when data is fetched
        logging.info("Data fetched successfully.")

        # Filter out unhealthy services
        filtered_data = {key: value for key, value in data.items() if value['state'] != 'healthy'}
        logging.info(f"Filtered data is: {filtered_data}")

        # Connect to PostgreSQL database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # SQL command to create the table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS faulty_versions (
            id SERIAL PRIMARY KEY,
            service_name VARCHAR(255) NOT NULL,
            sem_version VARCHAR(255) NOT NULL,
            state VARCHAR(255) NOT NULL
        )
        """
        cursor.execute(create_table_query)

        # Insert filtered data into the 'faulty_versions' table
        for service_name, service_data in filtered_data.items():
            cursor.execute(
                "INSERT INTO faulty_versions (service_name, sem_version, state) VALUES (%s, %s, %s)",
                (service_name, service_data['semVersion'], service_data['state'])
            )

        # Commit the changes and close the database connection
        connection.commit()
        connection.close()

        # Log when data is posted to the database
        logging.info("Data posted to the database successfully.")

    except Exception as e:
        logging.error(f"Error: {e}")

# Function to periodically fetch and store data
def periodic_task():
    while True:
        fetch_and_store_data()
        # Sleep for 30 seconds before the next fetch
        time.sleep(30)

# Start the periodic task in a separate thread
fetch_thread = threading.Thread(target=periodic_task)
fetch_thread.daemon = True  # Allow the thread to exit when the main program exits
fetch_thread.start()

if __name__ == '__main__':
    app.run()
