import os
import random
from flask import Flask, render_template, jsonify, Response, request
from flask.ext.classy import FlaskView
import requests

app = Flask(__name__)

class AppView(FlaskView):
    route_base = '/'
    api_key = "dc6zaTOxFJmzC" # os.environ.get("GIPHY_API_KEY")

    def post(self):
        trigger = request.form["trigger_word"]
        term = request.form["text"][len(trigger):]

        if term == "":
            response = requests.get('http://api.giphy.com/v1/gifs/random?api_key={key}'.format(
                key=self.api_key
            )).json()

            return jsonify({
                "text": response["data"]["image_url"]
            })
        else:
            response = requests.get(
                'http://api.giphy.com/v1/gifs/search?q={term}&api_key={key}&limit=10&offset=0'.format(
                    term=term,
                    key=self.api_key
                )
            ).json()

            image = random.choice(response["data"])


            if image["images"]["original"]["width"] > image["images"]["original"]["height"]:
                url = image["images"]["fixed_height"]["url"]
            else:
                url = image["images"]["fixed_width"]["url"]


            return jsonify({
                "text": url
            })


AppView.register(app)

if __name__ == '__main__':
    app.debug = True
    app.run()
