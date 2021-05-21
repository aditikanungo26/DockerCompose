# Apache Airflow and PostgreSQL with Docker Compose

#### Apache Airflow: 
 Apache Airflow is a workflow automation and scheduling system that can be used to author and manage data pipelines. Airflow uses workflows made of directed acyclic graphs (DAGs) of tasks.

#### PostgreSQL: 
 PostgreSQL is an enterprise-class open source database management system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads
 
#### Docker-Compose:
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration


### Getting Started with the Installation:

Follow below steps to install necessary tools:

##### Install Docker:
- Install [Docker community edition](https://docs.docker.com/engine/install/ubuntu/ "Docker community edition") on the workstation.
-  Follow post installation steps  like starting the docker service and group permissions.

##### Install Docker Composer
- Install  [docker compose](https://docs.docker.com/compose/install/ "docker compose") on your workstation

##### Airflow Setup
- Fetch the latest copy of [docker compose file](https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml "docker compose file") having airflow service. This file will contains Airflow services like Scheduler, webserver, worker, airflow init, flower, postgres and redis
- Prepare the setup before initializing the airflow. Run below command

```bash
mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```
- initialize airflow 
```shell
docker-compose up airflow-init
```

##### Postgres Database Setup

- Add one more Postgres service configuration in the docker compose file (created 2 different postgres containers for this POC)

```yaml
postgres_source:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: postgres
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data_updated
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    ports:
      - 5104:5432
    restart: always
    
  postgres_target:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: tgt_postgres
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data_target
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    ports:
      - 5961:5432
    restart: always  
  ```

##### Running Ariflow
Now we can start all services
```bash
docker-compose up
```
We can access airflow UI using the link http://localhost:5884

![image](https://user-images.githubusercontent.com/78525449/119169595-d3165080-ba7f-11eb-9bae-e6ce109d56a8.png)




Now we have two Postgres services running and databases are postgres and tgt_postgres

#### Create Connections in Airflow to connect to Postgres Services

For both the database create the respective connections by providing the details like host, schema ,port ,username and password. 

- Connection for first database(Postgres)

![image](https://user-images.githubusercontent.com/78525449/119183110-42487080-ba91-11eb-9368-45dba65e5519.png)


- Connection for tgt_postgres database

![image](https://user-images.githubusercontent.com/78525449/119179522-a1f04d00-ba8c-11eb-99e8-47619d016d7f.png)

Place copy_data.py script inside airflow/dag folder.  Once that is done run the dag using the Airflow UI

![image](https://user-images.githubusercontent.com/78525449/119181146-d06f2780-ba8e-11eb-8931-402f70e238a3.png)


##### Airflow Script:
The script created uses the source and target database connection and using the cursor fetches the data from one database and store it into another database.


##### Steps to verify data into target database 

- Following command starts the web service and runs bash as its command.

```bash
docker-compose run postgres_target bash

```
-  Run below command to get into the database.

```bash
 psql --host=postgres_target --username=airflow --dbname=tgt_postgres
```

- Now we can see that data has been copied to target database

![image](https://user-images.githubusercontent.com/78525449/119183178-5ab88b00-ba91-11eb-9bab-ec92e30ccf47.png)


![image](https://user-images.githubusercontent.com/78525449/119181036-b6cde000-ba8e-11eb-8961-f35fb1910502.png)











