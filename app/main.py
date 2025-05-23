from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session
from app.schema import schema
from app.database import engine, get_db
from app.database import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_context(request: Request, db: Session = Depends(get_db)):
    return {"request": request, "db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
