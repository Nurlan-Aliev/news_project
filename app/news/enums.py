from enum import Enum


class Status(str, Enum):
    confirm: str = "confirm"
    reject: str = "reject"
    pending: str = "pending"
