from flask import Flask, request
from flask_restful import Resource, Api

from lando.welcome_quest import setup_questionnaire
from lando.chat import Context

app = Flask(__name__)
api = Api(app)


q,c = setup_questionnaire()


class test(Resource):

    def put(self):
        context = Context(**request.get_json(force=True))
        currentQuestion = context.data.get('current_question')

        # if current question is already answered by user, reply to the user
        if context.data.get('responses').get(currentQuestion) is not None:
            q.sendResponse(context)
        
        # if current question is not answered yet, send question to the user
        else:
            q.sendQuestion(context)

        return context.data



        


api.add_resource(test, '/')

if __name__ == '__main__':
    app.run(debug=True)