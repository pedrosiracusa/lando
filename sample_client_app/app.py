import sys
sys.path.append('/mnt/c/Users/Pedro/DocumentsUbuntu/lando')

from flask import Flask, render_template, request
from lando.client import Client

app = Flask(__name__)

cli=Client(api_endpoint='http://localhost:5000/')

@app.route("/", methods=['GET','POST'])
def index():
    if request.method=='POST':
        user_input = request.form.get('input')
        cli.send_input(user_input) 
        answer = cli.getMessage()
        cli.requestNextQuestion()
        message = cli.getMessage()
        return render_template('test.html', message=message, answer=answer)

    
    elif request.method=='GET':
        cli.requestNextQuestion()
        message = cli.getMessage()

        return render_template('test.html',message=message)



if __name__ == '__main__':
    app.run(port=5001, debug=True)