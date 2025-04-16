from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .ms_coaches_sportsmen.schema import schema
from app.database import engine
from .ms_coaches_sportsmen import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
