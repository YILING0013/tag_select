from flask import Flask,redirect, url_for, render_template, session
from tag_select import tag_select_blueprint
from tag_extractor import tag_extractorbp
from search import search_blueprint
import threading
import yaml

app = Flask(__name__)

app.register_blueprint(tag_select_blueprint, url_prefix='/api_tag')
app.register_blueprint(search_blueprint, url_prefix='/search')
app.register_blueprint(tag_extractorbp, url_prefix='/api')

@app.route('/')
def tag_control_route():
    return render_template('tag_select.html')

if __name__ == '__main__':
    app.run(debug=True)
