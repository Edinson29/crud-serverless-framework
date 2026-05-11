"""This module contains the code for build de Update users in DynamoDB."""


from fastapi import HTTPException
from shared_package.dynamodb import DynamoDB
from shared_package.config import settings


TABLE_NAME: str = settings.DYNAMODB_TABLE_NAME


def build_update_user(body: dict, pk: str) -> dict:
    """This function updates a user in the DynamoDB table.
    Before updating the user, it validates if the user exists in the database by pk, if it does not exist, it raises an exception."""
    try:
        dynamo = DynamoDB()

        response: dict = dynamo.get_item_by_field(TABLE_NAME, "pk", pk)
        if not response:
            raise HTTPException(status_code=404, detail="User not updated, user does not exist in the database")
        
        update_expression, expression_attribute_name, expression_attributes_values = build_update_expression(body)

        response: dict = dynamo.update_item(TABLE_NAME, {"pk": pk}, update_expression, expression_attribute_name, expression_attributes_values)
        return response
    except Exception as e:
        print(e)
        raise e


def build_update_expression(data: dict) -> tuple[str, dict, dict]:
    """This function builds the update expression for the DynamoDB update_item method."""
    update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in data.keys()])
    expression_attribute_names = {f"#{k}": k for k in data.keys()}
    expression_attribute_values = {f":{k}": v for k, v in data.items()}
    return update_expression, expression_attribute_names, expression_attribute_values