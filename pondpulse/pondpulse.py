from flask import Flask, request, jsonify
import schedule
import time
import threading
import logging

app = Flask("microservices")

# Initialize a dictionary to store microservice data
microservices = {
    "AuthenticationService": {
        "name": "Authentication Service",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "PaymentGateway": {
        "name": "Payment Gateway",
        "semVersion": "2.1.0",
        "state": "insecure"
    },
    "InventoryService": {
        "name": "Inventory Service",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "OrderProcessing": {
        "name": "Order Processing",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "UserManagement": {
        "name": "User Management",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "NotificationService": {
        "name": "Notification Service",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "AnalyticsEngine": {
        "name": "Analytics Engine",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "RecommendationSystem": {
        "name": "Recommendation System",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "SearchService": {
        "name": "Search Service",
        "semVersion": "1.0.0",
        "state": "healthy"
    },
    "ContentDelivery": {
        "name": "Content Delivery",
        "semVersion": "1.0.0",
        "state": "healthy"
    }
}

# Function to increment the semVersion of each microservice
def increment_sem_versions():
    for service_name in microservices:
        sem_version = microservices[service_name]["semVersion"]
        major, minor, patch = map(int, sem_version.split("."))
        minor += 1  # Increment minor version
        new_sem_version = f"{major}.{minor}.{patch}"
        microservices[service_name]["semVersion"] = new_sem_version
        logging.info(f"semVersion incremented for {service_name}, the new semVersion is now {new_sem_version}")

# Schedule the increment_sem_versions function to run every 5 minutes
schedule.every(1).minutes.do(increment_sem_versions)


# Configure logging
logging.basicConfig(filename='pondpulse.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Create a background thread to run the scheduled tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

@app.route('/microservices', methods=['GET', 'POST'])
def manage_microservices():
    if request.method == 'GET':
        return jsonify(microservices)
    elif request.method == 'POST':
        data = request.get_json()
        if data.get("service_name") in microservices:
            service_name = data["service_name"]
            if "state" in data:
                microservices[service_name]["state"] = data["state"]
            return jsonify({"message": f"Updated {service_name} details"})
        else:
            return jsonify({"error": "Service not found"}), 404

@app.route('/')
def my_func():
    return "Welcome to the microservices management system"

app.run(host="0.0.0.0", port=5001, debug=False)
