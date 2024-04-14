from flask_restx import Namespace, reqparse, Resource, fields, marshal
# from typing import List
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
# from ..model.subscribers import Subscriber
from flask import jsonify
# from .subscriberNS import subscriber_model2


newspaper_ns = Namespace("newspaper", description="Newspaper related operations")
issue_ns = Namespace("issue", description="Issue related operations")
subscriber_ns = Namespace("subscriber", description="Subscriber related operations")



subscriber_model2 = subscriber_ns.model('SubscriberModel2', {
    "subscriber_id": fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='name'),
    'address': fields.String(required=True,
            help='address')
   })

subscriber_model = subscriber_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='name'),
    'address': fields.String(required=True,
            help='address'),
    'list_of_newspapers': fields.List(fields.Integer, required=True,
            help='list_of_newspapers'),
    "list_of_issues": fields.List(fields.Integer, required=True,
            help='list_of_issues')
   })

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })

paper_model2 = newspaper_ns.model('NewspaperModel2', {
    'name': fields.String(required=True,
            help='The name of thpe newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })

paper_model3 = newspaper_ns.model('NewspaperModel3', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
   })



issue_model = newspaper_ns.model('IssueModel', {
    'issue_id': fields.Integer(required=False,
            help='The unique identifier of an issue'),
    "editor_id": fields.Integer(required=True,
            help='The unique identifier of an editor'),
    'name:': fields.String(required=True,
            help='The name of the issue, e.g. first/second issue'),
    # 'frequency': fields.Integer(required=True,
    #         help='The publication frequency of the issue  (e.g. how often the magazine is issued'),
    # # 'price': fields.Float(required=True,
    #         help='The price of the issue (e.g. 10.0)'),
    "page_number": fields.Integer(required=True,
            help='The number of pages in the issue'),
    "released": fields.Boolean(required=True,
            help='Whether the issue has been released or not'),
    "releasedate": fields.Date(required=True,
            help='The date on which the issue was released'),
    'subscribers': fields.Nested(subscriber_model2, required=True,
            help='list_of_subscribers')
})

issue_model2 = newspaper_ns.model('IssueModel2', {
    # 'price': fields.Float(required=True,
    #         help='The price of the issue (e.g. 10.0)'),
    "page_number": fields.Integer(required=True,
            help='The number of pages in the issue'),
    "released": fields.Boolean(required=True,
            help='Whether the issue has been released or not'),
    "releasedate": fields.Date(required=True,
            help='The date on which the issue was released'),
    'subscribers': fields.List(fields.Integer, required=True,
            help='list_of_subscribers')
})


issue_model3 = newspaper_ns.model('IssueModel3', {
    "editor_id": fields.Integer(required=True,
            help='The unique identifier of an editor')
})

issue_model4 = newspaper_ns.model('IssueModel4', {
    "subscriber_id": fields.Integer(required=True,
            help='Send an issue to a subscriber')
})

issue_model5 = newspaper_ns.model('IssueModel5', {
    "paper_id": fields.Integer(required=True,
            help='Send an issue to a subscriber'),
    'issue_id': fields.Integer(required=False,
            help='The unique identifier of an issue'),
    "released": fields.Boolean(required=True,
            help='Whether the issue has been released or not')
})

@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model2, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        # TODO: this is not smart! you should find a better way to generate a unique ID!
        # paper_id = len(Agency.get_instance().newspapers) + 20
        paper_id = max([0] + [p.paper_id for p in Agency.get_instance().newspapers], default=0) + 1
        # frequency = newspaper_ns.payload.get('frequency', 1)
        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)
        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()


@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):
    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        #-- TODO: update newspaper
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper ID {paper_id} not found")
        else:
            targeted_paper.name = newspaper_ns.payload['name']
            targeted_paper.frequency = newspaper_ns.payload['frequency']
            targeted_paper.price = newspaper_ns.payload['price']
            return targeted_paper

    @newspaper_ns.doc(description="Delete a new newspaper")  #and all its issues?
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")


@newspaper_ns.route('/<int:paper_id>/issue')
class newspaperIssueID(Resource):
    @newspaper_ns.marshal_list_with(issue_model, envelope='newspaper')
    @newspaper_ns.doc(description="List all issues of a specific newspaper")
    def get(self, paper_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        if paper:
            return paper.issues
        return jsonify(f"Newspaper with ID {paper_id} was not found")


    # @issue_ns.marshal_list_with(issue_model, envelope='issue')
    @issue_ns.doc(description="Create a new issue")
    @issue_ns.expect(issue_model2, validate=True)
    @issue_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        newspaper = Agency.get_instance().get_newspaper(paper_id)
        if not newspaper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        issue_id = max([0] + [i.issue_id for i in newspaper.issues], default=0) + 1
        new_issue = Issue(
                          issue_id=issue_id,
                          page_number=issue_ns.payload['page_number'],
                          released=issue_ns.payload['released'],
                          releasedate=issue_ns.payload['releasedate'])
            # price=issue_ns.payload['price'])
        Agency.get_instance().add_issue(new_issue)
        newspaper.issues.append(new_issue)
        return new_issue


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class issueID(Resource):
    @newspaper_ns.marshal_with(issue_model, envelope='newspaper')
    @newspaper_ns.doc(description="Get information of a newspaper issue")
    def get(self, paper_id, issue_id):
        targeted_issue = Agency.get_instance().get_issue(issue_id)
        if targeted_issue:
            return targeted_issue


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class released(Resource):
    @issue_ns.marshal_with(issue_model, envelope='newspaper')
    @issue_ns.doc(issue_model, description="Release an issue")
    def post(self, paper_id, issue_id):
        issue = Agency.get_instance().get_issue(issue_id)#.released
        if issue:
            issue.released = True
            return issue
        return "error: issue not found"


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor')
class issueEditor(Resource):
    @issue_ns.marshal_with(issue_model, envelope='newspaper')
    @issue_ns.expect(issue_model3, validate=True)
    @issue_ns.doc(description="Specify an editor for an issue. (Transmit the editor ID as parameter) [The editor ID needs to be defined in the body of the request]")
    def post(self,  paper_id, issue_id):
        issue = Agency.get_instance().get_issue(issue_id)
        if issue:
            editor = Agency.get_instance().get_editor(issue_ns.payload['editor_id'])
            if editor:
                editor.list_of_issues.append(issue)
                issue.set_editor(issue_ns.payload['editor_id'])
                return issue
            return "error: editor not found"
        return "error: issue not found"


@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/deliver')
class deliver(Resource):
    #@newspaper_ns.marshal_with(subscriber_model2, envelope='newspaper')
    @newspaper_ns.expect(issue_model4, validate=True)
    @newspaper_ns.doc(description="Send an issue to a subscriber ' This means there should be a record of the subscriber receiving '")
    def post(self, paper_id, issue_id):
        paper = Agency.get_instance().get_newspaper(paper_id)
        subscriber_id = issue_ns.payload['subscriber_id']
        subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not subscriber:
            return "error: subscriber not found"
        if not paper:
            return "error: newspaper not found"
        issue = Agency.get_instance().get_issue(issue_id)
        if not issue:
            return "error: issue not found"
        if issue and issue.released:
            # Issue.deliver_to_subscribers(issue, subscriber)
            issue.subscribers.append(subscriber.subscriber_id)
            subscriber.delivered_issues.append(issue.issue_id)
            # paper.subscribers.append(subscriber)
            # Issue.delivered_issue.append(issue.issue_id)
            return jsonify(f"issue {issue_id} was delivered to subscriber {subscriber_id}")


@newspaper_ns.route('/<int:paper_id>/stats')
class stats(Resource):
    @newspaper_ns.doc(description="Return information about the specific newspaper (number of subscribers, monthly and annual revenue)")
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        paper_subscribers = len(targeted_paper.subscribers)
        # if len(targeted_paper.price)>0:
        paper_revenue = targeted_paper.price * paper_subscribers
        annual_revenue = paper_revenue * 12
        return {'subscribers': paper_subscribers, 'revenue': paper_revenue, 'annual_revenue': annual_revenue}
