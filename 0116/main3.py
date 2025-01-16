from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'main3 (ver1)'

if __name__ == '__main__':
    app.run(debug=True)