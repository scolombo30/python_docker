# Readme
Sample python app that uses FASTAPI framework and PostgreSQL database.
The main goal here is to:
1. Create simple REST API with FASTAPI that can be used to create, read, and delete recipes.
2. Run the app as a Docker container.
3. Use Docker Compose to create and start both app and db in one command.
4. Using Minikube to create local Kubernetes cluster and run the app there as a pod.

### Local run:
- First create venv with `python -m venv venv`
- Activate venv with `venv\Scripts\activate`
- Install requirements with `pip install -r requirements.txt`
- Deactivate venv with `venv/Scripts/deactivate`
- Create .env file with `New-Item -ItemType file -Name .env`(windows) or `touch .env` (linux)
- Add in .env file values for:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST
- Run with `uvicorn main:app --reload`

### To create local db in docker (first point):
- Run `docker run --name test-db -e POSTGRES_PASSWORD=<password> -e POSTGRES_USER=<user> -e POSTGRES_DB=<dbname> -p 5432:5432 -d postgres`
- For first time connect to db and create sample table:
    - `docker exec -it test-db bash`
    - `psql -U root -d db_test`
    - `CREATE TABLE IF NOT EXISTS recipe (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients text[] NOT NULL
    );`

### Create docker image (second point):
- Create Dockerfile file with `New-Item -ItemType file -Name Dockerfile`(windows) or `touch Dockerfile` (linux)
- Add instructions to Dockerfile as desired
- Create docker image by running `docker build -t test-app-image .`
- Create env file with environment variables for docker image with `New-Item -ItemType file -Name .env`(windows) or `touch .env` (linux)
- Add in .env file values for:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST (since we're using the network to connect to the db, don't use localhost, use the name of the db container)
- Create docker network with `docker network create test-app-net`
- Connect db to docker network with `docker network connect test-app-net test-db`
- Run the container and connect the network with `docker run -d --name test-app --network test-app-net -p 8080:8080 --env-file .env test-app-image`

### Create docker-compose.yml file (third point):
- Create docker-compose.yml file with `New-Item -ItemType file -Name docker-compose.yml`(windows) or `touch docker-compose.yml` (linux)
- Add instructions to docker-compose.yml as desired
- Create env file with environment variables for docker image with `New-Item -ItemType file -Name env.json`(windows) or `touch env.json` (linux)
- Add in secrets.yml values for:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
- Run with `docker-compose up -d`
- To stop run `docker-compose down`