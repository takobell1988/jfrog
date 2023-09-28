from flask import Flask, jsonify, request
import requests
import schedule
import time
import logging

app = Flask("FlyTrap")

# Define the URL of the PondPulse app that provides microservices data
PONDPULSE_APP_URL = "http://localhost:5001/microservices"

# Function to fetch content from PondPulse and update states
def fetch_content_and_update_states():
    try:
        response = requests.get(PONDPULSE_APP_URL)
        if response.status_code == 200:
            microservices_data = response.json()
            
            # Log content retrieval
            logging.info("Fetched microservices data from PondPulse.")
            
            for service_name, service_info in microservices_data.items():
                sem_version = service_info["semVersion"]
                major, minor, patch = map(int, sem_version.split("."))
                
                # Check and update state to "insecure" for versions 1.0.1 to 1.0.3
                if major == 1 and minor == 0 and 1 <= patch <= 3:
                    if service_info["state"] != "insecure":
                        logging.info(f"Changing state of {service_name} to insecure.")
                        service_info["state"] = "insecure"
                        
                        # Send a POST request to PondPulse to update its state to "insecure"
                        update_data = {"service_name": service_name, "state": "insecure"}
                        response = requests.post(PONDPULSE_APP_URL, json=update_data)
                        if response.status_code == 200:
                            logging.info(f"State change of {service_name} to insecure successful.")
                        else:
                            logging.error(f"Failed to update state of {service_name} to insecure.")
                
                # Check and update state to "unhealthy" for versions 1.1.0 to 1.1.3
                elif major == 1 and minor == 1 and 0 <= patch <= 3:
                    if service_info["state"] != "unhealthy":
                        logging.info(f"Changing state of {service_name} to unhealthy.")
                        service_info["state"] = "unhealthy"
                        
                        # Send a POST request to PondPulse to update its state to "unhealthy"
                        update_data = {"service_name": service_name, "state": "unhealthy"}
                        response = requests.post(PONDPULSE_APP_URL, json=update_data)
                        if response.status_code == 200:
                            logging.info(f"State change of {service_name} to unhealthy successful.")
                        else:
                            logging.error(f"Failed to update state of {service_name} to unhealthy.")
                        
    except Exception as e:
        logging.error(f"Failed to fetch or update microservices data: {str(e)}")

# Schedule the fetch_content_and_update_states function to run every 30 seconds
schedule.every(30).seconds.do(fetch_content_and_update_states)

# Configure logging
logging.basicConfig(filename='flytrap.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

@app.route('/microservices', methods=['GET'])
def get_microservices():
    try:
        response = requests.get(PONDPULSE_APP_URL)
        if response.status_code == 200:
            microservices_data = response.json()
            return jsonify(microservices_data)
        else:
            return jsonify({"error": "Failed to fetch microservices data"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def my_func():
    return "Welcome to FlyTrap - The microservices state updater"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
