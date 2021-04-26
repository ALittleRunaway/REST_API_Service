"""REST- API server"""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import *
from methods import Handler
from errors import Errors

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # To work with utf-8
app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db' # Connect to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def index():
    """Shows the empty main page"""
    return ""


@app.route("/query", methods=['GET'])
def query():
    """Processes 'query' method"""
    filter_by = request.args.get('filter_by')
    group_by = request.args.get('group_by')
    sort_by = request.args.get('sort_by')
    columns = request.args.get('columns')
    arguments = {"filter_by": filter_by,
                 "group_by": group_by,
                 "sort_by": sort_by,
                 "columns": columns,
                 }
    # returns the json dictionary
    try:
        return Handler.creating_answer(arguments)
    except OperationalError as e:
        return Errors.existing_errors(e)
    except IndexError:
        return Errors.created_errors("IndexError")


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)




























