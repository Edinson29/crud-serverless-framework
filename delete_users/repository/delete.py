"""This modules contains the code for validate if the user exists in the database before delete it."""


from fastapi import HTTPException
from shared_package.dynamodb import DynamoDB
from shared_package.config import settings


def validate_delete_user(id: str) -> None:
    """This function validates if the user exists in the database before delete it, if it does not exist, it raises an exception."""
    try:
        dynamo = DynamoDB()
        response: dict = dynamo.get_item_by_field(settings.DYNAMODB_TABLE_NAME, "pk", id)
        if not response:
            raise HTTPException(status_code=404, detail="User not deleted, user does not exist in the database")
        
        dynamo.delete_item(settings.DYNAMODB_TABLE_NAME, id)
    except Exception as e:
        print(e)
        raise e