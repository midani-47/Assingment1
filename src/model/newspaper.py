from typing import List
from flask_restx import Model
from .issue import Issue


class Newspaper(object):

    def __init__(self, paper_id: int, name: str, price: float, frequency: int):
        self.paper_id: int = paper_id
        self.name: str = name
        self.frequency = frequency  # the issue frequency (in days)
        self.price: float = price  # the monthly price
        self.issues: List[Issue] = []
        self.subscribers: List = []


