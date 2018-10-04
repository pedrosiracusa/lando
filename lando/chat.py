# coding: utf-8

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
    
    def saveUserInput(self, inpt):
        """
        Saves user response (input) to the question.
        input type: 'text','number','choice'
        """
        self.user_input = { 'text':str, 
                            'number':float, 
                            'choice':int }[self.user_input_type]( inpt )
        
    def isFinalQuestion(self):
        return True if self.next is None else False
    
    def attachResponse(self, response):
        self.response=response
        
    def respond(self, context=None):
        print(context.data)
        if not hasattr(self,'response'):
            return None
        
        if not hasattr(self,'user_input'):
            user_input=context.data['responses'][self.name]
            return self.response.getResponse(user_input)

        return self.response.getResponse(self.user_input)

    
    def checkUserInput(self):
        return self.user_input
    
    def getNextQuestionName(self):
        """
        Checks user input to determine the next question in the graph.
        """
        if self.next is None:
            return None
        
        if len(self.next)>1:
            return self.next[ self.options.index(self.checkUserInput()) ]
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
    
    def getUserInput(self, context):
        user_input = context.data['user_input']
        questionId = context.data['current_question']
        
        q = self.questions.get(questionId)
        q.saveUserInput(user_input)
        context.data['responses'][q.name]=q.checkUserInput()
        return context
    
    def sendResponse(self, context):
        questionId = context.data['current_question']
        q = self.questions.get(questionId)
        response = q.respond(context)
        context.data['message'] = response
        return context
    
    def getNextQuestion(self,context):
        currentQuestion = self.questions.get( context.data['current_question'] )
        nextQuestion = currentQuestion.getNextQuestionName()
        
            
        context.data['current_question'] = nextQuestion
        
        # clean non-relevant data from context
        context.data.pop('message',None)
        context.data.pop('user_input',None)
        context.data.pop('input_type',None)
        context.data.pop('input_options',None)
        context.data.pop('input_options_text',None)
        return context
    
    def run(self, context):
        finish=False
        
        while not finish:
            self.sendQuestion(context)
            user_input = input(context.data['message'])
            context.set_user_input(user_input)
            self.getUserInput(context)
            self.sendResponse(context)
            print(context.data['message'])
            self.getNextQuestion(context)
            
            next_q = context.data['current_question']
            if next_q is None:
                finish=True
        
        print("End of run")
        return context



class Context:
    def __init__(self, **data):
        self.data=data
        if self.data.get('responses') is None:
            self.data['responses']={}
        
    def set_user_input(self,user_input):
        self.data['user_input']=user_input

    def update(self, data):
        self.data.update(data)



