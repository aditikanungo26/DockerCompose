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
- Prepare the setup before initializing the airflow. Run below below commands 

```bash
mkdir ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```
- Initialize airflow 
```shell
docker-compose up airflow-init
```

##### Postgres Database Setup

- Add one more Postgres service configuration in the docker compose file

```yaml
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


