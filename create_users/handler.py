import os
import json
import boto3
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from create_users.schema import UserBody


load_dotenv()
app = FastAPI()

dynamodb_client_params = {}

if os.getenv("IS_OFFLINE"):
    dynamodb_client_params = {
        "region_name": "localhost",
        "endpoint_url": "http://localhost:8000",
        "aws_access_key_id": "MockAccessKeyId",
        "aws_secret_access_key": ""
    }

dynamodb = boto3.resource("dynamodb", **dynamodb_client_params)
table = dynamodb.Table("usersTable")

@app.post("/users")
async def create_users(user_body: UserBody):
    try:
        id: str = str(uuid.uuid4())

        item: dict = user_body.model_dump()
        print(f"Item to be inserted: {item}", flush=True)
        item["pk"] = id

        table.put_item(Item=item)

        return JSONResponse(
            status_code=201,
            content={ "body": item }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
handler = Mangum(app)