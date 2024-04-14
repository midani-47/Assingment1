from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from typing import List
from ..model.agency import Agency
from ..model.subscribers import Subscriber
from .newspaperNS import paper_model3

subscribers_ns = Namespace("subscriber", description="Subscriber related operations")

subscriber_model = subscribers_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=False,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='name'),
    'address': fields.String(required=True,
            help='address'),
        'list_of_newspapers': fields.List(fields.Integer, required=True,
                help='list_of_newspapers'),
    "list_of_issues": fields.List(fields.Integer, required=True,
            help='list_of_issues'),
    "delivered_issues": fields.List(fields.Integer, required=True,
            help='delivered_issues'),
    "special_issues": fields.List(fields.Integer, required=True,
            help='special_issues')
   })

#model 2 made for the body of post with marshal
subscriber_model2 = subscribers_ns.model('SubscriberModel2', {
    'name': fields.String(required=True,
            help='name'),
    'address': fields.String(required=True,
            help='address')
   })

@subscribers_ns.route('/')
class SubscriberAPI(Resource):
    @subscribers_ns.marshal_list_with(subscriber_model, envelope='subscriber')
    @subscribers_ns.doc(description="List all subscribers in the agency")
    def get(self):
        return Agency.get_instance().all_subscribers()

    @subscribers_ns.doc(description="Create a new subscriber")
    @subscribers_ns.expect(subscriber_model, validate=True)
    @subscribers_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        subscriber_id = max([0] + [s.subscriber_id for s in Agency.get_instance().subscribers], default=0) + 1
        new_subscriber = Subscriber(subscriber_id=subscriber_id,
                              name=subscribers_ns.payload['name'],
                              address=subscribers_ns.payload['address'],
                              list_of_newspapers=subscribers_ns.payload['list_of_newspapers'],
                              list_of_issues=subscribers_ns.payload['list_of_issues'])
        Agency.get_instance().add_subscriber(new_subscriber)
        return new_subscriber


@subscribers_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource):
    @subscribers_ns.marshal_list_with(subscriber_model, envelope='subscriber')
    @subscribers_ns.doc(description="Get a subscriber's information")
    def get(self,subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        return targeted_subscriber


    @subscribers_ns.doc(description="Delete a subscriber")
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        Agency.get_instance().remove_subscriber(targeted_subscriber)
        return jsonify(f"Subscriber with ID {subscriber_id} was removed")


    @subscribers_ns.doc(description="Update a subscriber")
    @subscribers_ns.expect(subscriber_model, validate=True)
    @subscribers_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        targeted_subscriber.name = subscribers_ns.payload['name']
        targeted_subscriber.address = subscribers_ns.payload['address']
        targeted_subscriber.list_of_newspapers = subscribers_ns.payload['list_of_newspapers']
        return targeted_subscriber


@subscribers_ns.route('/<int:subscriber_id>/subscribe')
class Subscribe(Resource):
    @subscribers_ns.doc(description="Subscribe a subscriber to a newspaper")
    @subscribers_ns.expect(paper_model3, validate=True)
    @subscribers_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if targeted_subscriber:
            paper_id = subscribers_ns.payload['paper_id']
            targeted_newspaper = Agency.get_instance().get_newspaper(paper_id)
            if targeted_newspaper:
                if targeted_newspaper not in targeted_subscriber.list_of_newspapers:
                    targeted_subscriber.list_of_newspapers.append(paper_id)
                    targeted_newspaper.subscribers.append(subscriber_id)
            return targeted_subscriber
        return "Subscriber not found"


@subscribers_ns.route('/<int:subscriber_id>/stats')
class Stats(Resource):
    @subscribers_ns.doc(description="Get the number of newspaper subscriptions and the monthly and annual cost, as well as the number of issues that the subscriber received for each paper(if the frequency is set to zero, the newspaper is issued weekly).")
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        subscriptions=len(targeted_subscriber.list_of_newspapers)
        cost = 0
        freq = []
        for paper_id in targeted_subscriber.list_of_newspapers:
            paper = Agency.get_instance().get_newspaper(paper_id)
            if paper.frequency == 0:
                paper.frequency = 7
            freq.append("Number of issues (per month): "+str(30//paper.frequency))
            cost+= paper.price
        annual_cost=cost*12
        return {'Subscriptions': subscriptions , 'Monthly cost': cost, 'Annual cost': annual_cost, 'Monthly number if issues': freq}




@subscribers_ns.route('/<int:subscriber_id>/missingissues')
class MissingIssues(Resource):
    @subscribers_ns.marshal_list_with(subscriber_model, envelope='subscriber')
    @subscribers_ns.doc(description="Check if there are any undelivered issues of the subscribed papers.")
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found")
        missing_issues = []
        for paper_id in targeted_subscriber.list_of_newspapers:
            paper = Agency.get_instance().get_newspaper(paper_id)
            if paper_id:
                for issue in paper.issues:
                    if issue not in targeted_subscriber.delivered_issues:
                        missing_issues.append(issue)
        return missing_issues
