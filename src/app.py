from flask import Flask
from flask_restx import Api
from .api.newspaperNS import newspaper_ns
from .api.subscriberNS import subscribers_ns
from .model.agency import Agency
from .api.editorsNS import editors_ns


agency = Agency()
def create_app():
    paperroute_app = Flask(__name__)

    paperroute_api = Api(paperroute_app, title="PaperBack: An App for Newspaper Issue and Subscription Management")




    # add individual namespaces
    paperroute_api.add_namespace(newspaper_ns)
    paperroute_api.add_namespace(subscribers_ns)
    paperroute_api.add_namespace(editors_ns)





    return paperroute_app

if __name__ == '__main__':
    create_app().run(debug=False, port=7890)