import os
from typing import Union

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ARRAY
from sqlalchemy import insert

load_dotenv()

user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
port = 5432
database = os.environ.get("POSTGRES_DB")

engine = create_engine(
    url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
        user, password, host, port, database
    )
)

metadata = MetaData()

recipe_table = Table(
    "recipe",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String),
    Column("ingredients", ARRAY(String))
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# method used to create an item and save it to the database
@app.post("/items")
def create_item(recipe: dict):
    check_and_create_recipe_table()
    stmt = insert(recipe_table).values(name=recipe["name"], ingredients=recipe["ingredients"])
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()
        return {"id": result.inserted_primary_key[0], "name": recipe["name"], "ingredients": recipe["ingredients"]}


def check_and_create_recipe_table():
    if not engine.dialect.has_table(engine.connect(), "recipe"):
        metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
