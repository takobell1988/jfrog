### usefull commands ###



helm install from jfrog helm artifact:

helm install jfrog-microservices helm-repo-helm/jfrog-microservices


check the db contents: 

kubectl exec -it <postgresql-pod-name>  --  bash

psql -U dbuser -d mydb -h localhost

SELECT * FROM faulty_versions;