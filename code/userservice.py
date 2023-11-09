from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc # To handle exceptions while querying
from pydantic import parse_obj_as
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
# URL to run -> http://localhost:8000/docs which opens the Swagger API documentation
# Run Uvicorn - uvicorn main:app --reload

Base = declarative_base()
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    mobile = Column(String(15), nullable=False)
    gender = Column(String(10), )
    address = Column(Text)
    age = Column(Integer(),)

class UserSchema(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    name: str   
    email: str
    mobile:str
    gender:str
    address:str
    age:int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

app = FastAPI()

 #Todo read from ini file
url = URL.create( drivername="postgresql", username="postgres", password="postgres", host="localhost", database="postgres")
engine = create_engine(url)
print("Connecting to database")
connection = engine.connect()
print("Connection successful ")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.get('/users')
def getAllUsers(response: Response):
    users = session.query(User).all()
    print(len(users))
    if len(users) == 0: #No users exists return appropraite HTTPS response
        response.status_code = status.HTTP_200_OK #Todo test after delete
        retString = "No users exists in the user database"
        json_string = '{"message": "' + retString + '"}'
        return json.loads(json_string)
    else:
        user_list = parse_obj_as(List[UserSchema], users)
        response.status_code = status.HTTP_200_OK
        return user_list

@app.get('/users/{u_id}')
def get_user(u_id: int, response: Response):
    users = session.query(User).filter(User.id == u_id).all()
    if len(users) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND #Todo test after delete
        retString = "User with id " + str(u_id) + " does not exists in user database"
        json_string = '{"message": "' + retString + '"}'
        return json.loads(json_string)
    else:
        user_list = parse_obj_as(List[UserSchema], users)
        response.status_code = status.HTTP_200_OK
        return user_list

@app.delete('/users/{u_id}',status_code=202)
def delete_user(u_id: int):
    try:
        retValue = session.query(User).filter(User.id==u_id).delete()

        if retValue == 0:
            retString = "user with user id " + str(u_id) + " does not exists"
            json_string = '{"message": "' + retString + '"}'
            return json.loads(json_string)
        else:
            session.commit()
            retString = "user with user id " + str(u_id) + " deleted successfully"
            json_string = '{"message": "' + retString + '"}'
            return json.loads(json_string)
    except:
        print('Exception occurred while deleting')

@app.put('/users/{u_id}', status_code=202)
def update_user(u_id: int, userObj: UserSchema):
    users = session.query(User).filter(User.id == u_id).all()
    if len(users) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        retString = "User with id " + str(u_id) + " does not exists in user database"
        json_string = '{"message": "' + retString + '"}'
        return json.loads(json_string)
    else:
        new_user = User(
        id=userObj.id,
        name=userObj.name,
        email=userObj.email,
        address=userObj.address,
        mobile=userObj.mobile,
        gender=userObj.gender,
        age=userObj.age
        )
        session.query(User).filter(User.id == u_id).update({User.email:new_user.email, 
        User.name:new_user.name, User.address:new_user.address, User.mobile:new_user.mobile, User.gender:new_user.gender, User.age:new_user.age})
        session.commit()
        return UserSchema.from_orm(new_user)

@app.post('/users', status_code=201)
def new_user(userObj: UserSchema):
    users = session.query(User).all()
    if len(users) == 0:
        u_id = 1
    else:
        max_id = 1
        for u in users:
            if u.id > max_id:
                max_id = u.id
        u_id = max_id + 1

    new_user = User(
        id=u_id,
        name=userObj.name,
        email=userObj.email,
        address=userObj.address,
        mobile=userObj.mobile,
        gender=userObj.gender,
        age=userObj.age
    )

    try:
        session.add(new_user)
        session.commit()
        return UserSchema.from_orm(new_user)
    
    except exc.IntegrityError:
        print("Exception Occured")
        return "Unable to add duplicate values"

    