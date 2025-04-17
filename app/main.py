from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.schema import schema
from app.database import engine
from app.database import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
