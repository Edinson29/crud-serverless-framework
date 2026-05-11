"""This file contains the code for build de Create users in DynamoDB."""
import uuid
from shared_package.dynamodb import DynamoDB
from shared_package.config import settings

TABLE_NAME: str = settings.DYNAMODB_TABLE_NAME


def register_new_user(body: dict) -> dict:
    """This function creates a user in the DynamoDB table.
    Before creating the user, it generates a unique id for the user and adds it to the body of the request.
    Also validates if the user already exists in the database by email, if it does, it raises an exception."""
    try:
        body["pk"] = str(uuid.uuid4())
        dynamo = DynamoDB()

        response: dict = dynamo.get_item_by_field(TABLE_NAME, "email", body["email"])
        if response:
            raise Exception("User not created, email already exists in the database")

        dynamo.create_item(TABLE_NAME, body)
        return body
    except Exception as e:
        print(e)
        raise e