"""This file contains the code to connect to DynamoDB and create a table if it doesn't exist."""
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Attr
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from shared_package.config import settings

load_dotenv()

class DynamoDB:
    def __init__(self):
        """This methos initializes the DynamoDB client for local or in lambda."""
        dynamodb_client_params = {}

        if settings.IS_OFFLINE:
            dynamodb_client_params = {
                "region_name": "localhost",
                "endpoint_url": "http://localhost:8000",
                "aws_access_key_id": "MockAccessKeyId",
                "aws_secret_access_key": ""
            }

        self.dynamodb = boto3.resource("dynamodb", **dynamodb_client_params)

    def create_item(self, table_name: str, item: dict) -> dict:
        """This method creates an item in the specified DynamoDB table."""
        table = self.dynamodb.Table(table_name)
        try:
            table.put_item(Item=item)
            return item
        except ClientError as e:
            print(e)
            raise Exception("Error creating item in DynamoDB")
        
    def get_item_by_field(self, table_name: str, field_name: str, field_value: str) -> dict:
        """This method return an item from the specified DynamoDB table by a field name and value."""
        table = self.dynamodb.Table(table_name)
        try:
            response = table.scan(
                FilterExpression=Attr(field_name).eq(field_value)
            )
            items = response.get("Items", [])
            return items[0] if items else {}
        except ClientError as e:
            print(e)
            raise Exception("Error retrieving item from DynamoDB")
        

    def get_items(self, table_name: str) -> dict:
        """This method retrieves all items from the specified DynamoDB table."""
        table = self.dynamodb.Table(table_name)
        try:
            response: dict = table.scan()
            return response.get("Items", [])
        except ClientError as e:
            print(e)
            raise Exception("Error retrieving items from DynamoDB")
        
    
    def update_item(self, table_name: str, key: dict, update_expression: str, expression_attribute_names: dict, expression_attribute_values: dict) -> dict:
        """This method updates an item in the specified DynamoDB table."""
        table = self.dynamodb.Table(table_name)
        try:
            response = table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_attribute_values,
                ReturnValues="ALL_NEW"
            )
            return response.get("Attributes", {})
        except ClientError as e:
            print(e)
            raise Exception("Error updating item in DynamoDB")
        
    
    def delete_item(self, table_name: str, pk: str) -> JSONResponse:
        """This method deletes an item from the specified DynamoDB table."""
        table = self.dynamodb.Table(table_name)
        try:
            table.delete_item(Key={'pk': pk})
            return JSONResponse(
                status_code=200,
                content={ "body": f"The user with pk: {pk} has been deleted!" }
            )
        except ClientError as e:
            print(e)
            raise Exception("Error deleting item from DynamoDB")