"""This modules contains the handler for the delete_users endpoint, which deletes an existing user from the DynamoDB table."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from delete_users.repository.delete import validate_delete_user


app = FastAPI()


@app.delete("/users/{id}")
async def delete_users(id: str):
    try:
        validate_delete_user(id)

        return JSONResponse(
            status_code=200,
            content={ "body": f"The user with pk: {id} has been deleted!" }
        )
    except HTTPException as http_exc:
        print(http_exc.detail)
        raise http_exc
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
handler = Mangum(app)