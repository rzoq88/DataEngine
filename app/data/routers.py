import uuid
from typing import Optional
from starlette.exceptions import HTTPException
import pathlib
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse

from app import utils
from app.users.decorators import login_required
from app.shortcuts import (
    render,
    redirect, 
    get_object_or_404,
    is_htmx
)

from .models import Data
from .schemas import (
    DataCreateSchema,
    DataEditSchema)
from .script import run_add_data

router = APIRouter(
    prefix='/data'
)

@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(
    request: Request,
    is_htmx=Depends(is_htmx),
):
    if is_htmx:
        return render(request, "data/htmx/create.html", {})
    return render(request, "data/create.html", {})


@router.post("/create", response_class=HTMLResponse)
@login_required
def Data_create_post_view(request: Request, is_htmx=Depends(is_htmx), title: str=Form(...), url: str = Form(...)):
    raw_data = {
        "title": title,

        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, DataCreateSchema)
    redirect_path = data.get('path') or "/data/create" 
    
    context = {
        "data": data,
        "errors": errors,
        "title": title,
        "url": url,

    }

    if is_htmx:
        """
        Handle all HTMX requests
        """
        if len(errors) > 0:
            return render(request, "data/htmx/create.html", context)
        context = {"path": redirect_path, "title": data.get('title')}
        return render(request, "data/htmx/link.html", context)
    """
    Handle default HTML requests
    """
    if len(errors) > 0:
        return render(request, "data/create.html", context, status_code=400)
    return redirect(redirect_path)

#add file to database
BASE_DIR = pathlib.Path(__file__).resolve().parent
directory = BASE_DIR /"files"
output = BASE_DIR / "output"

@router.post("/add", response_class=HTMLResponse)
@login_required
def add_data(request:Request):
    if request.user.is_authenticated:
        user_id =request.user.username
        run_add_data(directory,output,user_id) 


        

    


@router.get("/", response_class=HTMLResponse)
def Data_list_view(request: Request):
    q = Data.objects.all().limit(100)
    print(q)
    context = {
        "object_list": q
    }
    return render(request, "data/list.html", context)


# item_id='Data-1'
# f"{item_id} is cool"

@router.get("/{item_id}", response_class=HTMLResponse)
def Data_detail_view(request: Request, item_id: str):
    # print(item_id)
    q= Data.objects.get(item_id=item_id,host_service='data',source_name='file')
    print(q)
    #print(q)
    # obj = get_object_or_404(Data, item_id=item_id,host_service='data')
    print(q)
    if request.user.is_authenticated:
        user_id = request.user.username
        print(user_id)

    context = {
        "item_id": item_id,
        "object": q
    }
    return render(request, "data/detail.html", context)


@router.get("/{item_id}/edit", response_class=HTMLResponse)
@login_required
def Data_edit_view(request: Request, item_id: str):
    obj = get_object_or_404(Data, item_id=item_id,host_service='data')
    context = {
        "object": obj
    }
    return render(request, "data/edit.html", context) 



@router.post("/{item_id}/edit", response_class=HTMLResponse)
@login_required
def Data_edit_post_view(
        request: Request,
          item_id: str, 
        is_htmx=Depends(is_htmx), 
        
        email: str=Form(...), 
        url: str = Form(...)):
    raw_data = {
        "email": email,
        "url": url,
        "user_id": request.user.username
    }
    obj = get_object_or_404(Data, item_id=item_id,host_service='data')
    data, errors = utils.valid_schema_data_or_error(raw_data, DataEditSchema)
    if len(errors) > 0:
        return render(request, "data/edit.html", context, status_code=400)
    obj.email = data.get('email') or obj.email
    obj.update_Data_url(url, save=True)
    context = {
        "object": obj
    }
    return render(request, "data/edit.html", context)



@router.get("/{item_id}/hx-edit", response_class=HTMLResponse)
@login_required
def Data_hx_edit_view(
    request: Request, 
    item_id: str, 
    is_htmx=Depends(is_htmx)):
    if not is_htmx:
        raise HTTPException(status_code=400)
    obj = None
    not_found = False
    try:
        obj = get_object_or_404(Data, item_id=item_id,host_service='data')
    except:
        not_found = True
    if not_found:
        return HTMLResponse("Not found, please try again.")
    context = {
        "object": obj
    }
    return render(request, "data/htmx/edit.html", context) 



@router.post("/{item_id}/hx-edit", response_class=HTMLResponse)
@login_required
def Data_hx_edit_post_view(
        request: Request,
        item_id: str, 
        is_htmx=Depends(is_htmx), 
        title: str=Form(...), 
        url: str = Form(...),
        delete: Optional[bool] = Form(default=False)):
    if not is_htmx:
        raise HTTPException(status_code=400)
    obj = None
    not_found = False
    try:
        obj = get_object_or_404(Data, item_id=item_id)
    except:
        not_found = True
    if not_found:
        return HTMLResponse("Not found, please try again.")
    if delete:
        obj.delete()
        return HTMLResponse('Item Deleted')
    raw_data = {
        "title": title,
        "url": url,
        "user_id": request.user.username
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, DataEditSchema)
    if len(errors) > 0:
        return render(request, "Data/htmx/edit.html", context, status_code=400)
    obj.email = data.get('title') or obj.email
    obj.update_Data_url(url, save=True)
    context = {
        "object": obj
    }
    return render(request, "data/htmx/list-inline.html", context)