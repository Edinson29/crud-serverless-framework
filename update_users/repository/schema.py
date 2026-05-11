"""This module contains the schema for the update_users function."""


from pydantic import BaseModel


class UserBodyPut(BaseModel):
    """This class represents the body of the create_users function."""
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: str | None = None