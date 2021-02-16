from flask import Flask
app = Flask(__name__)

@app.route('/')
def check_working():
    return "Hello world"



if __name__ == '__main__':
    app.run(debug=True, port=5000) #run app in debug mode on port 5000