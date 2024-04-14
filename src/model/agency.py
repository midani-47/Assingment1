from typing import List, Union, Optional
from .newspaper import Newspaper
from .editors import Editor
from .subscribers import Subscriber
from .issue import Issue

class Agency(object):
    singleton_instance = None
    def __init__(self):
        self.newspapers: List[Newspaper] = []
        self.editors: List[Editor] = []
        self.subscribers: List[Subscriber] = []
        self.issues: List[Issue] = []


    @staticmethod
    def get_instance():
        if Agency.singleton_instance is None:
            Agency.singleton_instance = Agency()
        return Agency.singleton_instance

    def add_newspaper(self, new_paper: Newspaper):
        #TODO: assert that ID does not exist  yet (or create a new one)
        # if new_paper.paper_id in [paper.paper_id for paper in self.newspapers]:
        #     raise Exception(f"Newspaper with ID {new_paper.paper_id} already exists")
        il=[i.paper_id for i in self.newspapers]
        assert new_paper.paper_id not in il, "This id already exists"
        self.newspapers.append(new_paper)


    def get_newspaper(self, paper_id: Union[int,str]) -> Optional[Newspaper]:
        for paper in self.newspapers:
            if paper.paper_id == paper_id:
                return paper
        return None

    def all_newspapers(self) -> List[Newspaper]:
        return self.newspapers

    def remove_newspaper(self, paper: Newspaper):
        self.newspapers.remove(paper)
#############################################

    def add_editor(self, new_editor: Editor):
        #TODO: assert that ID does not exist  yet (or create a new one)
        if new_editor.editor_id in [editor.editor_id for editor in self.editors]:
            raise Exception(f"Editor with ID {new_editor.editor_id} already exists")
        self.editors.append(new_editor)


    def get_editor(self, editor_id: Union[int,str]) -> Optional[Editor]:
        for editor in self.editors:
            if editor.editor_id == editor_id:
                return editor
        return None

    def all_editors(self) -> List[Editor]:
        return self.editors

    def remove_editor(self, editor: Editor):
        self.editors.remove(editor)
        # replace the editor with a new one
        # self.editors.append(new_editor)

    #############################################
    def all_subscribers(self) -> List[Subscriber]:
        return self.subscribers

    def remove_subscriber(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def add_subscriber(self, new_subscriber: Subscriber):
        #TODO: assert that ID does not exist  yet (or create a new one)
        # if new_subscriber.subscriber_id in [subscriber.subscriber_id for subscriber in self.subscribers]:
        #     raise Exception(f"Subscriber with ID {new_subscriber.subscriber_id} already exists")
        id_list = [i.subscriber_id for i in self.subscribers]
        assert new_subscriber.subscriber_id not in id_list, "This id already exists"
        self.subscribers.append(new_subscriber)

    def get_subscriber(self, subscriber_id: Union[int,str]) -> Optional[Subscriber]:
        for subscriber in self.subscribers:
            if subscriber.subscriber_id == subscriber_id:
                return subscriber
        return None
#############################################
    def get_issue(self, issue_id: Union[int,str]) -> Optional[Issue]:
        for issue in self.issues:
            if issue.issue_id == issue_id:
                return issue
        return None

    def add_issue(self, new_issue: Issue):
        # if new_issue.issue_id in [issue.issue_id for issue in self.issues]:
        #     raise Exception(f"Issue with ID {new_issue.issue_id} already exists")
        self.issues.append(new_issue)


    @classmethod
    def remove_instance(cls):
        cls.singleton_instance = None



