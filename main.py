from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "users"

@app.post("/user", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):

    # create an instance of the User database model
    userdb = models.User(name=user.name, age=user.age, gender=user.gender, address=user.address)

    # add it to the session and commit it
    session.add(userdb)
    session.commit()
    session.refresh(userdb)

    # return the user object
    return userdb

@app.get("/user/{id}", response_model=schemas.User)
def read_user(id: int, session: Session = Depends(get_session)):

    # get the user item with the given id
    user = session.query(models.User).get(id)

    # check if user item with given id exists. If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"user item with id {id} not found")

    return user

@app.put("/user/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.User, session: Session = Depends(get_session)):

    # get the user item with the given id
    user_db = session.query(models.User).get(id)
    user_data = user.dict(exclude_unset=True)
    user_data.pop('id')

    for key, value in user_data.items():
        setattr(user_db, key, value)
        session.add(user_db)
        session.commit()
        session.refresh(user_db)

    # check if user item with given id exists. If not, raise exception and return 404 not found response
    if not user:
        raise HTTPException(status_code=404, detail=f"user item with id {id} not found")

    return user

@app.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, session: Session = Depends(get_session)):

    # get the user item with the given id
    user = session.query(models.User).get(id)

    # if user item with given id exists, delete it from the database. Otherwise raise 404 error
    if user:
        session.delete(user)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"user item with id {id} not found")

    return None

@app.get("/user", response_model = List[schemas.User])
def read_user_list(session: Session = Depends(get_session)):

    # get all user items
    user_list = session.query(models.User).all()

    return user_list