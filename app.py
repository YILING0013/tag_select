from flask import Flask,redirect, url_for, render_template, session
from tag_select import tag_select_blueprint
import threading
import yaml

app = Flask(__name__)

app.register_blueprint(tag_select_blueprint, url_prefix='/api_tag')

@app.route('/')
def tag_control_route():
    return render_template('tag_select.html')

if __name__ == '__main__':
    app.run(debug=True)
