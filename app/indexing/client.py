from algoliasearch.search_client import SearchClient

from app import config


from app.data.models import Data

from .schemas import (
    
    DataIndexSchema
)
from app.shortcuts import get_object_or_404

settings = config.get_settings()

def get_index():
    client = SearchClient.create(
            settings.algolia_app_id, 
            settings.algolia_api_key
    )
    index = client.init_index(settings.algolia_index_name)
    return index


def get_dataset():
    data_q = [dict(x) for x in Data.objects.all()]
    datas_dataset = [DataIndexSchema(**x).dict() for x in data_q]
    dataset = datas_dataset 
    return dataset

def update_index():
    index = get_index()
    dataset = get_dataset()
    idx_resp = index.save_objects(dataset).wait()
    try:
        count = len(list(idx_resp)[0]['objectIDs'])
    except:
        count = None
    return count


def search_index(query):
    index = get_index()
    post_id = [x for x in  Data.objects.filter(email__like=f'%{query}%')]
    # d=[dict(x) for x in post_id]
    # datas_dataset = [DataIndexSchema(**x).dict() for x in d]
    # print(datas_dataset)
    # print(d)
    # for i in post_id:
    #     print(i['email'])
    #     # print(i['path'])
    return post_id

def search_index_add(query):
    index = get_index()
    email=None
    ip=None
    password=None
    # q= Data.objects.filter(email__like=f'%{query[0]}%',username=query[1],country=query[2]).allow_filtering()
    # post_id = [x for x in  Data.objects.filter(email__like=f'%{query[0]}%',username=query[1],country=query[2])]
    if(query[0] !=''):    
        email = [x for x in  Data.objects.filter(email__like=f'%{query[0]}%')]
        # obj=Data.objects.filter(email__like=f'%{query[0]}%')
    if(query[1] !=''): 
        # obj=Data.objects.filter(password=f'{query[0]}')
        password = [x for x in  Data.objects.filter(password__like=f'%{query[1]}%')]
        # print(obj)
        # obj=Data.objects.filter(email__like=f'%{query[0]}%')

    if(query[2] !=''):    
        ip = [x for x in  Data.objects.filter(ip=f'%{query[2]}%')]
        # obj=Data.objects.filter(email__like=f'%{query[0]}%')

    # post_id = [x for x in  Data.objects.filter(email__like=f'%{query[0]}%',ip=f'%{query[1]}%',source_name=f'%{query[2]}%').allow_filtering()]
    # obj =get_object_or_404(Data,email=query[0],host_service='data')
    # print(obj)
    # d=[dict(x) for x in post_id]
    # datas_dataset = [DataIndexSchema(**x).dict() for x in d]
    # print(datas_dataset)
    # print(d)
    # for i in post_id:
    #     print(i['email'])
    #     # print(i['path'])
    post_id=[]
    if(password is not None):
        post_id.extend(password)
    if(email is not None):
        post_id.extend(email)
    if(ip is not None):
        post_id.extend(ip)




    return post_id

# def search_index(query):
#     index = get_index()
   
#     return index.search(query)