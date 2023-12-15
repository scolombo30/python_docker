# Readme
- First create venv with `python -m venv venv`
- Activate venv with `venv\Scripts\activate`
- Install requirements with `pip install -r requirements.txt`
- Deactivate venv with `venv/Scripts/deactivate`
- Create .env file with `New-Item -ItemType file -Name .env`(windows) or `touch.env` (linux)
- Add in .env file values for:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
  - POSTGRES_HOST
- Run with `uvicorn main:app --reload`

### To create local db in docker:
- Run `docker run --name test-db -e POSTGRES_PASSWORD=password -e POSTGRES_USER=root -e POSTGRES_DB=db_test -p 5432:5432 -d postgres`
- For first time connect to db and create sample table:
    - `docker exec -it test-db bash`
    - `psql -U root -d db_test`
    - `CREATE TABLE IF NOT EXISTS recipe (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ingredients text[] NOT NULL
    );`
