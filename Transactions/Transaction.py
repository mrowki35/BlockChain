import copy
import json
import datetime as dt
from abc import ABC, abstractmethod


class Transaction(ABC):
    def __init__(self, transaction_type: str, data: dict) -> None:
        self.transaction_type = transaction_type
        self.data = data
        self.timestamp = str(dt.datetime.now())

    @abstractmethod
    def validate(self) -> bool:
        pass

    def to_dict(self) -> dict:
        return {
            "type": self.transaction_type,
            "data": self.data,
            "timestamp": self.timestamp
        }

    def clone(self):
        """
        Tworzy głęboką kopię obiektu Transcaction.
        """
        return copy.deepcopy(self)
