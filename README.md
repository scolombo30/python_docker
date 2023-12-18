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
- Create json file with environment variables for docker image with `New-Item -ItemType file -Name env.json`(windows) or `touch env.json` (linux)
- Run the container `docker run -p 8080:8080 --name test-app -d --env-file env.json test-app-image`

### Create compose.yml file (third point):
- Create compose.yml file with `New-Item -ItemType file -Name docker-compose.yml`(windows) or `touch docker-compose.yml` (linux)
- Add instructions to compose.yml as desired
- Create secret file with `New-Item -ItemType file -Name secrets.yml`(windows) or `touch secrets.yml` (linux)
- Add in secrets.yml values for:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST
- Run with `docker-compose --env-file ./secrets.yml up -d`
- To stop run `docker-compose down`

### Create Kubernetes cluster and necessary config files(fourth point):
- Install minikube
- Create local cluster with `minikube start --driver docker`
- Create namespace with `kubectl create namespace minikube-ns`
- Create secret file with `New-Item -ItemType file -Name config-secrets.yml`(windows) or `touch config-secrets.yml` (linux)
- Insert in app-secrets.yml values for (insert base64 encoded value (windows) `[convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("string to convert"))`:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST
- Create deployment.yml file where define app deployment with `New-Item -ItemType file -Name deployment.yml`(windows) or `touch deployment.yml` (linux)
- Create service.yml file where define app service with `New-Item -ItemType file -Name service.yml`(windows) or `touch service.yml
- Apply changes for secrets with `kubectl apply -f config-secrets.yml`
- Before applying changes for app load into minikube your image with: `minikube image load <image_name>` (if error 'Unable to resolve the current Docker CLI context "default"' run `docker context use default`))
- Apply changes for app with `kubectl apply -f deployment.yml` 
- Apply changes for service with `kubectl apply -f service.yml`
- Forward app-test port with `kubectl port-forward service/test-app 8080:8080`. 
  Now you can test app with `curl http://localhost:8080` or view auto-generated doc at `http://localhost:8080/docs`