from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    name = "Hello"
    return name

@app.route('/api/v1/daikin')
def daikin():
    name = "daikin"
    return name

## おまじない
if __name__ == "__main__":
    app.run(debug=True)
