from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from mangum import Mangum

from create_users.repository.schema import UserBody
from create_users.repository.create import register_new_user


app = FastAPI()


@app.post("/users")
async def create_users(user_body: UserBody):
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