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

@app.put("/users/{id}")
async def update_users(id: str, user_body: UserBody):
    try:
        update_data = user_body.model_dump(exclude_unset=True)
        update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in update_data.keys()])
        expression_attribute_names = {f"#{k}": k for k in update_data.keys()}
        expression_attribute_values = {f":{k}": v for k, v in update_data.items()}

        response: dict = table.update_item(
            Key={'pk': id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW"
        )

        return JSONResponse(
            status_code=201,
            content={ "body": response.get("Attributes", {}) }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
handler = Mangum(app)