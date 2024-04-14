from .newspaper import Newspaper
from typing import List
from .issue import Issue

class Editor(object):
    def __init__(self, editor_id: int, name: str, address: str):
        self.editor_id: int = editor_id
        self.name: str = name
        self.address: str = address
        self.list_of_newspapers: List[Newspaper] = []
        self.list_of_issues: List[Issue] = []
        self.payment = 100

