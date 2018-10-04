from requests import put, get
import json

print("Send initial data (ask for q1)")
data={
    'current_question':"q1",
    'responses':{ }
}
print( put('http://localhost:5000/', data=json.dumps(data)).json() )


print("\nAnswer q1")
data={
    'current_question': 'q1', 
    'responses': {'q1':"Pedro"}, 
    'message': 'Oi! Me chamo Lando! Sou um assistente de terras. Qual seu nome?', 
    'user_input': '', 
    'input_type': 'text'}
print( put('http://localhost:5000/', data=json.dumps(data)).json() )


print("\nAsk for next question (q2)")
data={'current_question': 'q2', 'responses': {'q1': 'Pedro'}, 'message': 'Prazer em conhecê-lo, Pedro', 'user_input': '', 'input_type': 'text'}
print( put('http://localhost:5000/', data=json.dumps(data)).json() )

print("\nAnswer q2")
data={'current_question': 'q2', 'responses': {'q1': 'Pedro', 'q2':28}, 'message': 'E sua idade?', 'user_input': '', 'input_type': 'number'}
print( put('http://localhost:5000/', data=json.dumps(data)).json() )


print("\nAsk for next question (q3)")
data={'current_question': 'q3', 'responses': {'q1': 'Pedro', 'q2':28}, 'message': 'E sua idade?', 'user_input': '', 'input_type': 'number'}
print( put('http://localhost:5000/', data=json.dumps(data)).json() )

print("\nAnswer q3")
data={'current_question': 'q3', 'responses': {'q1': 'Pedro', 'q2': 28, 'q3':1}, 'message': "Primeiro preciso saber sobre a situação do seu solo. Ele está degradado? {0: 'não', 1: 'sim'}", 'user_input': '', 'input_type': 'choice', 'input_options': [0, 1], 'input_options_text': ['não', 'sim']}
print( put('http://localhost:5000/', data=json.dumps(data)).json() )