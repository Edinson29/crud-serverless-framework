"""This modules contains the handler for the update_users endpoint, which updates an existing user in the DynamoDB table."""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from update_users.repository.schema import UserBodyPut
from update_users.repository.update import build_update_user


app = FastAPI()


@app.put("/users/{id}")
async def update_users(id: str, user_body: UserBodyPut):
    try:
        update_data = user_body.model_dump(exclude_unset=True)

        response: dict = build_update_user(update_data, id)

        return JSONResponse(
            status_code=201,
            content={ "body": response }
        )
    except HTTPException as http_exc:
        print(http_exc.detail)
        raise http_exc
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Error updating user: {e}")

handler = Mangum(app)