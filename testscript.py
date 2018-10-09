# This script tests app.py
# A simple interaction using json-encoded data (ensuring ascii)

from requests import put, get
import json

print("Send initial data (ask for q1):")
data = {'current_question':"q1", 'responses':{} }
print(data)
print("Response:")
resp = put('http://localhost:5000/', data=json.dumps(data))
print(resp.json())
print("\n")


print("Answer q1:")
# set user input
data = {"current_question": "q1", "responses": {}, "message": "Olá! Me chamo Lando! Sou um assistente de terras. Qual seu nome?", "user_input": "Pédro", "input_type": "text"}
print(data)
print("Response:")
resp = put('http://localhost:5000/', data=json.dumps(data))
print(resp.json())
print("\n")


print("Ask for next question (q2):")
data = {"current_question": "q2", "responses": {"q1": "Pedro"}, "message": "Prazer em conhecê-lo, Pedro", "user_input": "", "input_type": "text"}
print(data, "type:", type(data))
print("Response:")
resp = put('http://localhost:5000/', data=json.dumps(data))
print(resp.json())
print("\n")


print("Answer q2:")
data = {"current_question": "q2", "responses": {"q1": "Pedro"}, "message": "E sua idade?", "user_input": "28", "input_type": "number"}
print(data, "type:", type(data))
print("Response:")
resp = put('http://localhost:5000/', data=json.dumps(data))
print(resp.json())
print("\n")


print("Ask for next question (q3):")
data = {"current_question": "q3", "responses": {"q1": "Pedro", "q2": 28.0}, "message": "É ótimo começar cedo!", "user_input": "", "input_type": "number"}
print(data, "type:", type(data))
print("Response:")
resp =  put('http://localhost:5000/', data=json.dumps(data))
print(resp.json())
print("\n")

print("Answer q3:")
data = {"current_question": "q3", "responses": {"q1": "Pedro", "q2": 28.0}, "message": "Primeiro preciso saber sobre a situação do seu solo. Ele está degradado? {0: 'não', 1: 'sim'}", "user_input": "1", "input_type": "choice", "input_options": [0, 1], "input_options_text": ["não", "sim"]}
print(data, "type:", type(data))
print("Response:")
resp = put('http://localhost:5000/', data=json.dumps(data))
print(resp.json())
print("\n")