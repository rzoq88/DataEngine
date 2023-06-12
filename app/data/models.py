from .exceptions import (
    InvalidDataURLException,
    DataAlreadyAddedException
)
import uuid
from app.config import get_settings
from app.users.exceptions import InvalidUserIDException
from app.users.models import User
from app.shortcuts import templates

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import (DoesNotExist, MultipleObjectsReturned)
from app.data.extractors import generate_unique_id
from cassandra.cqlengine import management
settings = get_settings()


class Data(Model):
    __keyspace__ = settings.keyspace
    host_service = columns.Text(partition_key=True,
         primary_key=True, default='data')
    item_id = columns.Text(primary_key=True)
    source_name = columns.Text(partition_key=True,primary_key=True)
    email = columns.Text(primary_key=True, index=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)  # UUID1
    title = columns.Text(primary_key=True)
    user_id = columns.UUID()
    url = columns.Text()
    password = columns.Text(index=True)
    firstname = columns.Text()
    lastname = columns.Text()
    address = columns.Text()
    ip = columns.Text(index=True)
    hashpassword = columns.Text(index=True)
    dateofbirth = columns.Text()
    gender = columns.Text()
    username = columns.Text(primary_key=True)
    country = columns.Text(primary_key=True,index=True)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"data(title={self.title}, item_id={self.item_id}, host_service={self.host_service})"

    def render(self):
        basename = self.host_service
        template_name = f"data/renderers/{basename}.html"
        context = {"item_id": self.item_id}
        t = templates.get_template(template_name)
        return t.render(context)

    def as_data(self):
        return {f"{self.host_service}_id": self.item_id, "path": self.path, "title": self.title}

    @property
    def path(self):
        return f"/data/{self.item_id}"

    @staticmethod
    def get_or_create(url, user_id=None, **kwargs):
        item_id = generate_unique_id(url)
        obj = None
        created = False
        try:
            obj = Data.objects.get(item_id=item_id)
        except MultipleObjectsReturned:
            q = Data.objects.allow_filtering().filter(item_id=item_id)
            obj = q.first()
        except DoesNotExist:
            obj = Data.add_data(url, user_id=user_id, **kwargs)
            created = True
        except:
            raise Exception("Invalid Request")
        return obj, created

    def update_data_url(self, url, save=True):
        item_id = generate_unique_id(url)
        if not item_id:
            return None
        self.url = url
        self.item_id = item_id
        if save:
            self.save()
        return url

    @staticmethod
    def add_data(url, user_id=None, **kwargs):

        item_id = str(uuid.uuid4())

        print('here is'+item_id)

        if item_id is None:
            raise InvalidDataURLException("Invalid data URL")
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException("Invalid user_id")
        # user_obj = User.by_user_id(user_id)
        # user_obj.display_name
        # q = Data.objects.allow_filtering().filter(item_id=item_id ,user_id=user_id)
        # print(q)
        # if q.count() != 0:
        #     raise DataAlreadyAddedException("Data already added")
        # print(user_id)
        # print(item_id)
        return Data.create(item_id=item_id, user_id=user_id, url=url, **kwargs)
