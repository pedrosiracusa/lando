from lando.client import Client

cli = Client(api_endpoint='http://localhost:5000/')

# Go to first question
# Print the message, and save input
cli.requestNextQuestion()

for answer in ["Pedro", #Nome
               "28", # Idade
               "0", # Solo degradado?
               "1", # Pecuária?
               "1", # Risco de incêndio?
               "0", # baixo/alto potencial de regeneração?
               "0", # plantar mudas ou semear? 
               "Não sei..." # Tipo de muda?
               ]:
    print(cli.getMessage())
    inpt = answer
    cli.send_input(inpt)
    print(inpt)
    print(cli.getMessage())
    print("")

    cli.requestNextQuestion()


print(cli.response.json())

