# test-fastapi
This is a quick guide based on the wonderful [turotial](https://fastapi.tiangolo.com/tutorial/) on FastAPI.

## First Shot
**Read the [first_shot/main.py](./first_shot/main.py), it might only take about one hour for experienced engineer.**

- Prepare
  - Some knowledge of OpenAPI(https://www.openapis.org/)
  - Set python version >= 3.10 (Python 3.11.0b4 is used in this repo)
  - If you are using [pipenv](https://pipenv.pypa.io/en/latest/)
    `cd first_shot && pipenv install`
    Otherwise,
    > pip install fastapi # FastAPI 0.99.0 or above
    > pip install python-multipart # For using Form, File, UploadFile
  - uvicorn main:app --reload # to watch the changes, visit localhost:8000 and localhost:8000/docs

- Testing
  - > pip install pytest
    > pip install httpx
    > pytest

- More Notes
  - [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/#bigger-applications-multiple-files)
  - [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/#dependencies)
  - [Security](https://fastapi.tiangolo.com/tutorial/security/#security)
  - [Testing](https://fastapi.tiangolo.com/tutorial/testing/#testing)
  - [Extra Data Types](https://fastapi.tiangolo.com/tutorial/extra-data-types/#extra-data-types): UUID, date, ...
  - [Disable Response Model](https://fastapi.tiangolo.com/tutorial/response-model/#disable-response-model) `response_model=None`
    - [Other Response Model encoding parameters](https://fastapi.tiangolo.com/tutorial/response-model/#response-model-encoding-parameters)
  - [Override the default exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers)
    - [Re-use FastAPI's exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#re-use-fastapis-exception-handlers)
  - [JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/#json-compatible-encoder)
    - [Body - Updates](https://fastapi.tiangolo.com/tutorial/body-updates/#body-updates)
  - [Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/#metadata-and-docs-urls)
