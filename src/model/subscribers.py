# from .newspaper import Newspaper
from typing import List
from .issue import Issue

class Subscriber(object):
    def __init__(self, subscriber_id: int, name: str, address: str,list_of_newspapers: List[int], list_of_issues: List[int]):
        self.subscriber_id: int = subscriber_id
        self.name: str = name
        self.address: str = address
        self.delivered_issues: List[int] = []
        self.special_issues: List[int] = []
        self.issues: List[Issue] = []
        if list_of_issues !=[0]:
            self.list_of_issues: List[int] = list_of_issues
        else:
            self.issues=[]
        if list_of_newspapers !=[0]:
            self.list_of_newspapers: List[int] = list_of_newspapers
        else:
            self.list_of_newspapers=[]




