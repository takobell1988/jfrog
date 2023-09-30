### usefull commands ###

check the db: 

kubectl exec -it <postgresql-pod-name>  --  bash

psql -U dbuser -d mydb -h localhost

SELECT * FROM faulty_versions;