from flask import Flask, jsonify


app = Flask(__name__)

hello_dict = {"Hello": "World!"}


@app.route("/")
def home():
    return "Hi"


@app.route("/api/v1.0/precipitation")
def normal():
    return hello_dict


@app.route("/api/v1.0/stations")
def jsonified():
    return jsonify(hello_dict)

@app.route("/api/v1.0/tobs")
def jsonified():
    return jsonify(hello_dict)

@app.route("/api/v1.0/<start>")
def jsonified():
    return jsonify(hello_dict)

@app.route("/api/v1.0/<start>/<end>")
def jsonified():
    return jsonify(hello_dict)

if __name__ == "__main__":
    app.run(debug=True)

