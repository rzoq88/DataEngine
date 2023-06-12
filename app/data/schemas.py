import uuid
from pydantic import (
    BaseModel,
    validator,
    root_validator,
    Field
)

from app.users.exceptions import InvalidUserIDException


from .exceptions import (
    InvalidDataURLException, 
    DataAlreadyAddedException
)
from .models import Data

class DataCreateSchema(BaseModel):
    url: str # user generated
    title:str
    user_id: uuid.UUID # request.session user_id
    email :str
    password :str 
    firstname :str 
    lastname :str 
    address :str 
    ip :str 
    hashpassword :str 
    dateofbirth :str 
    gender :str 
    source_name:str
    username:str
    country:str
    # item_id:str


    @validator("url")
    def validate_Data_url(cls, v, values, **kwargs):
        url = v
        data_id = url
        if data_id is None:
            raise ValueError(f"{url} is not a valid Data URL")
        return url

    @root_validator
    def validate_data(cls, values):
        url = values.get("url")
        title = values.get("title")
        email = values.get("email")
        password = values.get("password")
        firstname = values.get("firstname")
        lastname = values.get("lastname")
        hashpassword = values.get("hashpassword")
        dateofbirth = values.get("dateofbirth")
        gender = values.get("gender")
        address = values.get("address")
        source_name = values.get("source_name")
        username = values.get("username")
        country = values.get("country")




        if url is None:
            raise ValueError("A valid url is required.")
        user_id = values.get("user_id")
        print(user_id)
        data_obj = None
        extra_data = {}
        if title is not None:
            extra_data['title'] = title
            extra_data['email'] = email
            extra_data['password'] = password
            extra_data['firstname'] = firstname
            extra_data['lastname'] = lastname
            extra_data['hashpassword'] = hashpassword
            extra_data['dateofbirth'] = dateofbirth
            extra_data['gender'] = gender
            extra_data['address'] = address
            extra_data['source_name'] = source_name
            extra_data['username'] = username
            extra_data['country'] = country





        try:
            # print('trying')
            data_obj = Data.add_data(url, user_id=user_id, **extra_data)
            # print('done')
        except InvalidDataURLException:
            raise ValueError(f"{url} is not a valid Data URL")
        except DataAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidUserIDException:
            raise ValueError("There's a problem with InvalidUserIDException, please try again.")
        except:
            raise ValueError("There's a problem with data, please try again.")
        if data_obj is None:
            raise ValueError("data_obj is none, please try again.")
        if not isinstance(data_obj, Data):
            raise ValueError("There's a problem with isinstance, please try again.")
        # if title is not None:
        #     Data_obj.title = title
        #     Data_obj.save()
        return data_obj.as_data()


        
    

class DataEditSchema(BaseModel):
    url: str # user generated
    title: str # user generated

    @validator("url")
    def validate_Data_url(cls, v, values, **kwargs):
        url = v
        data_id = url
        if data_id is None:
            raise ValueError(f"{url} is not a valid Data URL")
        return url
