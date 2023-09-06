#!/usr/bin/env python3

from flask_restful import Api
from flask import Flask, render_template
import routes
from process import get_result

app = Flask(__name__)
api = Api()
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
routes.add_routes_to_resource(api)
api.init_app(app)


@app.route('/')
def RenderMainIndex():
    return render_template('index.html')

@app.route('/download')
def download_result():
    link = get_result()
    if link is None:
        link = render_template('index.html')

    return link


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5555)
