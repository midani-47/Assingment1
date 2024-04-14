class Issue(object):

    def __init__(self,issue_id,page_number,releasedate, editor = 0,released: bool = False): #,price
        self.releasedate = releasedate
        self.editor_id = editor
        self.released: bool = released
        # self.price=price
        self.page_number=page_number
        self.issue_id = issue_id
        self.subscribers = []
        # self.paper_id = []
        self.subscriber_id = []

    def set_editor(self, editor):
        self.editor_id=editor

    def deliver_to_subscribers(self, subscriber):
        self.subscriber_id=subscriber


        # pass

