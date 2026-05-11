"""This file contains the schema for the create_users function."""

from pydantic import BaseModel



class UserBody(BaseModel):
    """This class represents the body of the create_users function."""
    first_name: str
    last_name: str
    phone_number: str
    email: str