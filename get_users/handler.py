"""This module contains the handler for the get_users endpoint, which retrieves all users from the DynamoDB table."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum
from shared_package.dynamodb import DynamoDB
from shared_package.config import settings


app = FastAPI()


@app.get("/users")
async def get_users():
    """Endpoint to retrieve all users from the DynamoDB table."""
    try:
        dynamo = DynamoDB()
        response: dict = dynamo.get_items(settings.DYNAMODB_TABLE_NAME)
        return JSONResponse(
            status_code=200,
            content={ "body": response }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
handler = Mangum(app)