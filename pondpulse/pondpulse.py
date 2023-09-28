from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Initial state of microservices
microservices = {
    "Service1": {"version": "1.0.0", "state": "healthy"},
    "Service2": {"version": "1.0.0", "state": "healthy"},
    # Add entries for other microservices
}

@app.route('/microservices', methods=['GET'])
def get_microservices():
    return jsonify(microservices)

@app.route('/microservices/<service_name>', methods=['GET'])
def get_microservice(service_name):
    if service_name in microservices:
        return jsonify(microservices[service_name])
    else:
        return jsonify({"error": "Microservice not found"}), 404

@app.route('/microservices/<service_name>/update', methods=['POST'])
def update_microservice(service_name):
    if service_name in microservices:
        # Randomly increment the SemVer and change state
        microservices[service_name]["version"] = increment_semver(microservices[service_name]["version"])
        microservices[service_name]["state"] = random.choice(["healthy", "insecure", "slow"])
        return jsonify(microservices[service_name])
    else:
        return jsonify({"error": "Microservice not found"}), 404

def increment_semver(version):
    # Implement your SemVer increment logic here
    # For simplicity, increment the last digit
    parts = version.split('.')
    parts[-1] = str(int(parts[-1]) + 1)
    return '.'.join(parts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
