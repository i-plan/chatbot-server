from flask_restful import Resource
from flask import Flask, render_template, jsonify, make_response
class PingApi(Resource):
    def get(self):
        return jsonify({
            'code': 200,
            'data': "pong"
        })