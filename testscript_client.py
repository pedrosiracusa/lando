from lando.client import Client



print("First request to endpoint")
cli = Client(api_endpoint='http://localhost:5000/')
print(cli.response)
print("")
        
print("Send input to q1")
inpt = "Pedro"
cli.send_input(inpt)
print(cli.response)
print("")

print("Request q2")
cli.get_next_question()




