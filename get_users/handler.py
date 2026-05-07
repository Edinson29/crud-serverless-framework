import os
import json
import boto3
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum


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

@app.get("/users")
async def get_users():
    try:
        response = table.scan()
        return JSONResponse(
            status_code=200,
            content={ "body": response }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
handler = Mangum(app)