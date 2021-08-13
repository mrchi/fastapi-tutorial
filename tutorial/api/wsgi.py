# coding=utf-8

from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=["GET"])
def flask_index():
    return {"msg": "Flask index."}


@app.route("/hello", methods=["GET"])
def flask_hello():
    return jsonify({"foo": "bar"})


if __name__ == "__main__":
    app.run()
