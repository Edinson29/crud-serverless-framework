"""This modules contains the handler for the create_users endpoint, which creates a new user in the DynamoDB table."""


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from create_users.repository.schema import UserBody
from create_users.repository.create import register_new_user


app = FastAPI()


@app.post("/users")
async def create_users(user_body: UserBody):
    """Endpoint to create a new user in the DynamoDB table.
        Args:
            user_body (UserBody): The body of the request, which contains the user's information. 
        Returns:
            JSONResponse: A JSON response with the created user's information.
    """
    try:
        item: dict = user_body.model_dump()
        response: dict = register_new_user(item)

        return JSONResponse(
            status_code=201,
            content={ "body": response }
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")
handler = Mangum(app)