# Here we create the Engine Object - it's the basis which you do everything from connecting to your database to carrying out CRUD - SQL Model relies on that because it's based on SQLAlchemy
# keeping async DB API in mind we create async engine
from sqlmodel import create_engine , text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.books.config import Config

engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True, # this is used to log all the SQL statements that are being executed
    # future=True, # this is used to use the latest features of SQLAlchemy 2.0
))

# How can we make a task run when starting our application to connect to our database
# This will done through lifespan events - this is something you may want to run throught the lifespan of an application
# Each fastAPI instance is going to come with a special attribute called lifespan which is a function that runs when the application starts and stops
# To create a life span event , we will make use of specific decorator that comes from contextlib - inbuilt python library
# we write the code in src package __init__.py
# This is a special function that is called when the application starts and stops
# This is where we can connect to our database and create tables
async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hello';") # this is going to be executed as sql statement
        # to run our statement , we create a result object 
        result = await conn.execute(statement)
        print(result.all())
        # await conn.run_sync(Config.DBModel.metadata.create_all) # this is how we create all the tables in our database
        # print("Database connected successfully")