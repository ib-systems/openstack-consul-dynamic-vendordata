from typing import Any, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Json, Field
from consul_client import consul_client
from oslo_config import cfg
import os, re
from oslo_serialization import jsonutils
import uvicorn
import keystonemiddleware.auth_token
from fastapi import FastAPI

from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request, Response as FResponse

conf = cfg.CONF
conf(default_config_files=[os.getcwd() + "/ocdv.conf"])

flask_app = Flask(__name__)
flask_app.wsgi_app = keystonemiddleware.auth_token.AuthProtocol(flask_app.wsgi_app, {})


@flask_app.post("/")
def flask_main():
    data = request.get_json()
    instance_id = data.get("instance-id")
    print(f"instance_id={instance_id}. whole json: {data}")
    index, data = consul_client.kv.get(f"cloud/instances/{instance_id}/vendor-data-yml")
    if data is None:
        return FResponse({}, status=200, mimetype="application/json")
    else:
        res = data["Value"].decode("utf-8")
        return jsonutils.dumps(res)


app = FastAPI()

app.mount("/ocdv", WSGIMiddleware(flask_app))


class VendordataPayload(BaseModel):
    # Get the data nova handed us for this request
    #
    # An example of this data:
    # {
    #     "hostname": "foo",
    #     "image-id": "75a74383-f276-4774-8074-8c4e3ff2ca64",
    #     "instance-id": "2ae914e9-f5ab-44ce-b2a2-dcf8373d899d",
    #     "metadata": {},
    #     "project-id": "039d104b7a5c4631b4ba6524d0b9e981",
    #     "user-data": null
    # }
    project_id: str = Field(alias="project-id", default=None)
    instance_id: Optional[str] = Field(alias="instance-id", default=None)
    image_id: Optional[str] = Field(alias="image-id", default=None)
    user_data: Optional[str] = Field(alias="user-data", default=None)
    hostname: Optional[str] = Field(alias="hostname", default=None)
    metadata: Optional[Json[Any]] = Field(alias="metadata", default=None)


@app.post("/")
async def instance_vendordata(payload: VendordataPayload):
    # TODO: Implement using only fastapi

    return "Not Implemented"

    # print(f"Data: {json.dumps(payload.__dict__)}")
    # index, data = consul_client.kv.get(
    #     f"cloud/instances/{payload.instance_id}/vendor-data"
    # )
    # if data is None:
    #     return {}
    # else:
    #     return Response(content=data["Value"], media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
