import json
import requests
import logging
import threading
import time
from flask import Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Function to fetch data and store it in the database
def fetch_and_store_data():
    try:
        # Fetch data from the microservices URL
        response = requests.get("http://pondpulse-service/microservices")
        data = json.loads(response.text)
        logging.info(data)

        # Log when data is fetched
        logger.info("Data fetched successfully.")
        logging.info("Data fetched successfully.")

        
        for service_name, service_info in data.items():
            sem_version = service_info["semVersion"]
            major, minor, patch = map(int, sem_version.split("."))
            
            # Check and update state to "insecure" for versions 1.0.1 to 1.0.3
            if major == 1 and minor == 0 and 1 <= patch <= 3:
                if service_info["state"] != "insecure":
                    logging.info(f"Changing state of {service_name} to insecure.")
                    service_info["state"] = "insecure"
                    
                    # Send a POST request to PondPulse to update its state to "insecure"
                    update_data = {"name": service_name, "state": "insecure"}
                    response = requests.post('http://pondpulse-service/microservices', json=update_data)
                    if response.status_code == 200:
                        # Log when data is posted to the pondpulse-service
                        logging.info(f"State change of {service_name} to insecure successful.")
                        logging.info("Data posted to the 'http://pondpulse-service/microservices' successfully.")
                    else:
                        logging.error(f"Failed to update state of {service_name} to insecure.")
            
            # Check and update state to "slow" for versions 1.1.0 to 1.1.3
            elif major == 1 and minor == 1 and 0 <= patch <= 3:
                if service_info["state"] != "slow":
                    logging.info(f"Changing state of {service_name} to slow.")
                    service_info["state"] = "slow"
                    
                    # Send a POST request to PondPulse to update its state to "slow"
                    update_data = {"name": service_name, "state": "slow"}
                    response = requests.post('http://pondpulse-service/microservices', json=update_data)
                    if response.status_code == 200:
                        # Log when data is posted to the pondpulse-service
                        logging.info(f"State change of {service_name} to slow successful.")
                        logging.info("Data posted to the 'http://pondpulse-service/microservices' successfully.")
                    else:
                        logging.error(f"Failed to update state of {service_name} to slow.")


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
    app.run(host="0.0.0.0", port=5003, debug=False)
