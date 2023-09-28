import requests
import random
import time

# PondPulse API URL
PONDPULSE_API_URL = 'http://pondpulse:5000/microservices/'

def detect_bugs():
    while True:
        service_name = random.choice(list(microservices.keys()))
        if microservices[service_name]["state"] == "healthy":
            print(f"Detected bug in {service_name}")
            # Inform PondPulse to modify the state
            modify_state(service_name)
        time.sleep(random.randint(15, 60))

def modify_state(service_name):
    state = random.choice(["insecure", "slow"])
    response = requests.post(PONDPULSE_API_URL + f'{service_name}/update')
    if response.status_code == 200:
        print(f"Modified state of {service_name} to {state}")

if __name__ == '__main__':
    detect_bugs()
