! ### WELCOME TO MY JFROG SERVICES APP ### !

The purpose of the application is: to identify faulty versions of our services in our company.

The main table of services is displayed by the microservice called "pondpulse", the number of the service version increases every one minute.

When the "flytrap" application will run every 30 seconds - it will check whether faulty versions are displayed in the pondpulse table.

** faulty versions are ** :

"slow" for versions 1.1.0 to 1.1.3
"insecure" for versions 1.0.1 to 1.0.3


The "flytrap" app will send a POST request to the "pondpules" microservice in order to change the state of the service to "insecure" / "slow".


The purpose of the "postgribbit" microservice is to "fetch" the service table from the "pondpulse" application,
and if it detects a any faulty version - it will register the service and its version in the posgresql DB.




#### INSTALLETION INSTRUCTIONS ####

1.

To install all microservices, you'll need to add the following jfrog helm repo to your local helm repos by runnig the commands below: 


helm repo add helm-repo-helm https://ofirtako.jfrog.io/artifactory/api/helm/helm-repo-helm --username ofirtako@gmail.com --password cmVmdGtuOjAxOjE3Mjc2MjgyMTA6akVUakZTaDdzTjA4bzBxdjltVzdicVFUY2VL

2.

To ensure the repo is listed in your local helm repos, please run the command:

helm repo list

(Make sure the "helm-repo-helm" repo is listed.)


3.

Once you validate the repo exist in your local repos , run the following command to install it :

helm install my-app helm-repo-helm/jfrog-services-app

4.

Please be patient and Wait untill all pods are up and running.

Thats it !




### USFULE COMMANDS ###


You can check the logs of each microservice by running:

kubectl logs -f <pod-name>


You also can connect to Postgresql DB and check the table DB contents by running the commands: 

access the DB pod:

kubectl exec -it <postgresql-pod-name>  --  bash


login to the DB : 

psql -U dbuser -d mydb -h localhost


Select all rows in the table "faulty_versions" : 

SELECT * FROM faulty_versions;



THANK YOU FOR CHECKING OUT MY APP!

** PLEASE CONTACT ME IF YOU HAVE ANY QUESTIONS OR CONSIDERATIONS ABOUT HOW TO INSTALL OR CHECK THE APP **
It would be my pleasure to demonstrate it in a Zoom meeting!