"""This file contains the schema for crud users functions."""


from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBody(BaseModel):
    """This class represents the body of the create_users function."""
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None