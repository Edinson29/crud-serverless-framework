import os
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from shared_package.schema import UserBody


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

@app.delete("/users/{id}")
async def delete_users(id: str):
    try:
        response: dict = table.delete_item(
            Key={'pk': id}
        )

        return JSONResponse(
            status_code=200,
            content={ "body": f"The user with pk: {id} has been deleted!" }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
handler = Mangum(app)