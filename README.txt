! ### WELCOME TO MY JFROG SERVICES APP ### !

The purpose of the application is: 
TO IDENTIFY FAULTY VERSIONS IN OUR COMPANY, AND RECORD THEM IN THE DB.


The main table of services is displayed by the microservice called "pondpulse", which increments the services version every minute.

The "flytrap" application checks the pondpulse table every 30 seconds for any faulty versions.


** faulty versions are ** :

versions 1.1.0 to 1.1.3 - are "SLOW"
versions 1.0.1 to 1.0.3 - are "INSECURE"


A POST request will be sent to the "pondpules" microservice by the "flytrap" app to change the service state to "insecure" / "slow".


The purpose of the "postgribbit" microservice is to "fetch" the service table from the "pondpulse" application,
and if it detects a any faulty version - it will register the service and its version in the posgresql DB.




#### INSTALLETION INSTRUCTIONS ####

prerequisits : 

Up and runnig k8s cluster with internet connection, minikube / docker k8s

1.

To install all microservices, you'll need to add the following jfrog helm repo to your local helm repos by runnig the commands below: 


helm repo add helm-repo-helm https://ofirtako.jfrog.io/artifactory/api/helm/helm-repo-helm --username ofirtako@gmail.com --password cmVmdGtuOjAxOjE3Mjc2MjgyMTA6akVUakZTaDdzTjA4bzBxdjltVzdicVFUY2VL

2.

To ensure the repo is listed in your local helm repos, please run the command:

helm repo list

(Make sure the "helm-repo-helm" repo is listed.)


3.

Once you validate the repo exist in your local repos , run the following command to install it :

helm install my-app helm-repo-helm/jfrog-services-app -n <namespace-name>

4.
to check the pods status : 

kubectl get po -n <namespace-name>

Please be patient and Wait untill all pods are up and running.

Thats it !




### USEFUL COMMANDS ###


cheking the logs of each microservice can be done by running:

kubectl logs -f <pod-name>


You also can connect to Postgresql DB and check the table DB contents by running the commands: 

access the DB pod:

kubectl exec -it <postgresql-pod-name> -n <namespace-name> --  bash


login to the DB : 

psql -U <user> -d mydb -h localhost


Select all rows in the table "faulty_versions" : 

SELECT * FROM faulty_versions;



THANK YOU FOR CHECKING OUT MY APP!

The architacture diagram of the app and the helm charts can be found in the git repo :

https://github.com/takobell1988/jfrog/blob/master/services_app_architacture.png

The packged main helm chart is stored in jfrog artifactory:
https://ofirtako.jfrog.io/artifactory/helm-repo-helm/jfrog-services-app-0.1.0.tgz

** PLEASE CONTACT ME IF YOU HAVE ANY QUESTIONS OR CONSIDERATIONS ABOUT HOW TO INSTALL OR CHECK THE APP **
It would be my pleasure to demonstrate it in a Zoom meeting!




