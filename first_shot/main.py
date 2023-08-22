"""
Better to have knowledge of OpenAPI(https://www.openapis.org/)

Python 3.11.0b4

> pip install fastapi # FastAPI 0.99.0 or above
> pip install python-multipart # For using Form, File, UploadFile
> uvicorn main:app --reload # to watch the changes, visit localhost:8000 and localhost:8000/docs

The following content in main.py
"""
from typing import Annotated, Union
import time

from fastapi import (
    FastAPI,
    Query,
    Path,
    Body,
    Cookie,
    Header,
    Response,
    Form,
    File,
    UploadFile,
    HTTPException,
    Request,
    BackgroundTasks,
    Depends,
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, HttpUrl
import uvicorn

app = FastAPI()  # the name `app` matters, https://fastapi.tiangolo.com/tutorial/first-steps/#first-steps

class Image(BaseModel):
    url: HttpUrl
    name: str


class BaseItem(BaseModel):
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300,
        examples=["A very nice Item"],
    )  # Optional
    type: str | None = None  # Optional


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


class Item(BaseItem):
    name: str
    price: float = Field(gt=0, description="The price must be greater than zero", examples=[35.4])
    tax: float | None = None  # Optional
    tags: set[str] | None = None  # Optional
    images: list[Image] | None = None  # Optional


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class BaseUser(BaseModel):
    username: str
    full_name: str | None = None  # Optional

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "Name",
                    "full_name": "Full Name",
                }
            ]
        }
    }


class UserIn(BaseUser):
    password: str


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.get("/items/")
async def read_items(
    ads_id: Annotated[str | None, Cookie()] = None,  # Optional
    user_agent: Annotated[str | None, Header()] = None,  # Optional, auto converted from User-Agent in header
    x_token: Annotated[list[str] | None, Header()] = None,  # Optional
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            alias="item-query",
            pattern="^q:.*$",
            deprecated=True,
            include_in_schema=False,  # Exclude parameter from the generated OpenAPI Schema
        ),
    ] = None,  # Optional
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    if ads_id:
        results.update({"ads_id": ads_id})
    if user_agent:
        results.update({"User-Agent": user_agent})
    if x_token:
        results.update({"X-Token values": x_token})
    return results


@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Annotated[Item, Body(embed=True)]
):  # https://fastapi.tiangolo.com/tutorial/body-multiple-params/#embed-a-single-body-parameter
    results = {"item_id": item_id, "item": item}
    return results


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, lt=1e7)],  # [0, 1e7)
    q: Annotated[list[str] | None, Query(min_length=3, max_length=20)],
    size: Annotated[float, Query(gt=0, lt=10.5)],
    importance: Annotated[int, Body(ge=0)],
) -> list[Item]:
    info = {
        "item_id": item_id,
        "q": q,
        "size": size,
        "importance": importance,
    }
    print(info)
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


@app.get("/travel_items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    items = {
        "item1": {"description": "All my friends drive a low rider", "type": "car"},
        "item2": {
            "description": "Music is my aeroplane, it's my aeroplane",
            "type": "plane",
            "size": 5,
        },
    }
    return items[item_id]


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


@app.get("/offers/{offer_id}")
async def read_offer(offer_id: str) -> Offer:
    offers = {"foo": "The Foo Wrestlers"}
    if offer_id not in offers:
        raise HTTPException(
            status_code=404,
            detail="Offer not found",
            headers={"X-Error": "There goes my error"},
        )
    return offers[offer_id]


@app.post("/offers/")
async def create_offer(offer: Offer) -> Offer:
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):  # Pydantic convert string to int or float
    return weights


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://example.com/")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})


### Static files ###
app.mount("/static", StaticFiles(directory="static"), name="static")


### Form and File ###
@app.post("/login/")
async def login(username: Annotated[str, Form(alias="user-name")], password: Annotated[str, Form()]):
    return {"username": username}


@app.post("/files/", deprecated=True)
async def create_file(
    file: Annotated[bytes, File(description="A file read as bytes")],
):  # For small files
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],  # For big files
):
    return {"filename": file.filename}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    """
    An example of frontend page
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>"""
    return {"filenames": [file.filename for file in files]}


### Error Handling ###
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


### Middleware ###
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  # https://fastapi.tiangolo.com/tutorial/cors/#cors-cross-origin-resource-sharing


### Downstream tasks (only for small background tasks) ###
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

if __name__ == "__main__": # for debug
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
More Notes
# 1
Bigger Applications - Multiple Files
https://fastapi.tiangolo.com/tutorial/bigger-applications/#bigger-applications-multiple-files
# 2
Dependency Injection
https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies
# 3
Security
https://fastapi.tiangolo.com/tutorial/security/#security
# 4
Testing
https://fastapi.tiangolo.com/tutorial/testing/#testing
# 5
Extra Data Types: UUID, date, ...
https://fastapi.tiangolo.com/tutorial/extra-data-types/#extra-data-types
# 6
Disable Response Model
response_model=None
https://fastapi.tiangolo.com/tutorial/response-model/#disable-response-model
# 6.addition
Other Response Model encoding parameters
https://fastapi.tiangolo.com/tutorial/response-model/#response-model-encoding-parameters
# 7 
Override the default exception handlers
https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers
# 7.addtion
Re-use FastAPI's exception handlers
https://fastapi.tiangolo.com/tutorial/handling-errors/#re-use-fastapis-exception-handlers
# 8
JSON Compatible Encoder
https://fastapi.tiangolo.com/tutorial/encoder/#json-compatible-encoder
# 8.addition
Body - Updates
https://fastapi.tiangolo.com/tutorial/body-updates/#body-updates
# 9
Metadata and Docs URLs
https://fastapi.tiangolo.com/tutorial/metadata/#metadata-and-docs-urls
"""
