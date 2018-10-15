# Future: json context could look like { 'persistent_items': {...}, 'volatile_items': {...} }
# persistent_items: should be passed back and forth in all interactions. ex: user_responses
# volatile_items: Only make sense for a given, particular interaction. ex: current_question, next_question, message, input_type, input

class Question:
    def __init__(self, name, **attr):
        self.name=name
        self.attr=attr
        
        self.prompt = attr.get("prompt")
        self.options = attr.get("options")
        self.options_text = attr.get("options_text")
        self.next = attr.get("next")
        self.user_input_type = attr.get("input_type")
        
        
    def getOptions(self):
        """
        Returns a dictionary mapping choices (int) to their respective texts.
        """
        if self.options is None: return None
        return { o:t for o,t in zip(self.options, self.options_text) }
    
        
    def isFinalQuestion(self):
        return True if self.next is None else False
    
    def attachResponse(self, response):
        self.response=response
        
    def respond(self, context):
        """
        Returns the response message (associated to the respective Response object)
        """
        if not hasattr(self,'response'):
            return None
        
        user_input=context.data['responses'][self.name]
        return self.response.getResponse(user_input)

    
    def getNextQuestionName(self, user_input):
        """
        Checks user input to determine the next question in the graph.
        """
        if self.next is None:
            return None
        
        if len(self.next)>1:
            return self.next[ self.options.index(user_input) ]
        else:
            return self.next[0]
        
    def promptMessage(self):
        """
        Properly formats a message to be prompted to the user.
        """
        if self.user_input_type=='choice':
            return f"{self.prompt} {self.getOptions()}"
        else:
            return self.prompt

    def parseUserInput(self, user_input):
        return { 
            'text':str, 
            'number':float, 
            'choice':int }[self.user_input_type]( user_input )




class Response:
    def __init__(self, **attr):
        
        self.message=attr.get('message')
        self.condition=attr.get('condition')
        
        
    def getResponse(self, user_input):       
        if self.condition:
            return self.condition(user_input)
        else:
            return self.message



class Questionnaire:
    """
    Stores a graph of questions and runs it; keeps track of interactions using a context dictionary.
    """
    
    def __init__(self, questionnaire_dict=None):
        """
        Questionnaire dict to be used to build the instance
        """
        self.context = dict()
        
        if questionnaire_dict:
            self.questions = { qname: Question(qname,**qattrs) for qname, qattrs in questionnaire_dict.items() }
            
    
    def sendQuestion(self, context):
        """
        Sends current question (from context) to user
        """
        questionId = context.data['current_question']
        q = self.questions.get(questionId)
        context.data['message']=q.promptMessage()
        context.data['user_input']=''
        context.data['input_type']=q.user_input_type
        
        input_options = q.options
        if input_options:
            context.data['input_options']=input_options
            
        input_options_text = q.options_text
        if input_options_text:
            context.data['input_options_text']=input_options_text

        return context
    
    def saveUserInput(self, context):
        """
        Saves user response (input) to the context, using the question to parse it.
        Finally, clears user input
        input type: 'text','number','choice'
        """
        user_input = context.data.get('user_input','')
        questionId = context.data.get('current_question')
        q = self.questions.get(questionId)
        
        context.data['responses'][questionId] = q.parseUserInput(user_input)

        context.clear_user_input()
        return context
    
    def sendResponse(self, context):
        questionId = context.data.get('current_question')
        user_input = context.data['responses'].get(questionId)
        q = self.questions.get(questionId)
        response = q.respond(context)
        context.data['message'] = response
        context.data['next_question'] = q.getNextQuestionName(user_input)
        return context
    

    



class Context:
    # TODO: After receiving user input, should send next question in the response
    def __init__(self, **data):
        self.data=data
        if self.data.get('responses') is None:
            self.data['responses']={}

    @classmethod
    def from_json_data(cls, datadict):
        return cls(**datadict) 
    
    def get_current_question(self):
        return self.data.get('current_question')

    def get_user_input(self):
        return self.data.get('user_input','')

    def set_user_input(self,user_input):
        self.data['user_input']=user_input

    def clear_user_input(self):
        self.data['user_input']=''

    def update(self, data):
        self.data.update(data)

