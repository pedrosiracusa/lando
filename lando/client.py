from requests import put
from copy import deepcopy
import json

initial_question='q1'

class Client:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.current_question = initial_question
        self.response={}
        self.request={}

        self.request_questionnaire() # set initial response (first question)

    def request_questionnaire(self):
        """This method executes only once (during class initialization). Returns a dict"""
        data = {"current_question":initial_question}
        resp = put(self.api_endpoint, data=json.dumps(data))
        self.response=resp.json()

    def send_input(self, inpt):
        """Returns a dict"""
        self.request = deepcopy(self.response)
        self.request.update({'user_input':inpt})
        resp = put(self.api_endpoint, data=json.dumps( self.request ))   
        self.response=resp.json()

    def get_next_question(self):
        # TODO: from the last response (after user input), must get next question
        pass