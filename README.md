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
- Create json file with environment variables for docker image with `New-Item -ItemType file -Name .env`(windows) or `touch .env` (linux)
- Run the container `docker run -p 8080:8080 --name test-app -d --env-file .env test-app-image`