"""This module contains the class for save the configuration of the application."""


import os


class Settings:
    """This class represents the settings of the application."""
    IS_OFFLINE: bool = os.getenv("IS_OFFLINE")
    DYNAMODB_TABLE_NAME: str = os.getenv("DYNAMODB_TABLE_NAME")


settings = Settings()