"""Class for handling queries"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # To work with utf-8
app.config['JSON_SORT_KEYS'] = False # To save the right order in the dictionaries
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///statistics.db' # Connect to the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Handler():
    """The main class for handling queries"""

    @staticmethod
    def creating_answer(arguments):
        """This method handles all the other methods and returns the answer"""
        # Reformating arguments from the request
        arguments = Handler.columns_reform_arguments(Handler.sort_group_by_filter_by_reform_arguments(
                Handler.filter_by_reform_arguments(arguments)))
        # Making a query
        subquery, column_order = Handler.select_making_query(arguments)
        query = subquery + Handler.filter_making_query(arguments) + \
                Handler.group_making_query(arguments) + Handler.sort_making_query(arguments)
        # Execute the query
        logs = db.engine.execute(query)
        arguments["columns"] = column_order
        columns = Handler.column_order(arguments)
        return Handler.forming_a_response(query, logs, columns)

    @staticmethod
    def column_order(arguments):
        """Adds numbers to the columns and returns a dictionary"""
        i = 0
        columns = {}
        for column in arguments["columns"]:
            columns[column] = i
            i += 1
        return columns

    @staticmethod
    def filter_by_reform_arguments(arguments):
        """Reforms filter_by arguments so it's comfortable to work with them"""
        if arguments["filter_by"]:
            d = {}
            lst = arguments["filter_by"].split(";")
            # for every pair of arguments:
            for ls in lst:
                ls = ls.split(":")
                # for date_from and date_to
                if ls[0] == "date_from":
                    d["date_from"] = f">='{ls[1]}'"
                elif ls[0] == "date_to":
                    d["date_to"] = f"<'{ls[1]}'"
                # for >=(>>), <=(<<)
                elif ls[1].startswith("<<") or ls[1].startswith(">>"):
                    d[ls[0]] = ls[1][0] + "=" + ls[1][2:]
                # for <>
                elif ls[1].startswith("<>"):
                    try:
                        int(ls[1][2:])
                        d[ls[0]] = "<>" + ls[1][2:]
                    except ValueError:
                        d[ls[0]] = f"<>'{ls[1][2:]}'"
                # for >, <
                elif ls[1].startswith("<") or ls[1].startswith(">"):
                    d[ls[0]] = ls[1]
                # for =
                else:
                    try:
                        int(ls[1])
                        d[ls[0]] = "=" + ls[1]
                    except ValueError:
                        d[ls[0]] = f"='{ls[1]}'"
            arguments["filter_by"] = d
        return arguments

    @staticmethod
    def sort_group_by_filter_by_reform_arguments(arguments):
        """Reforms sort_by and group_by arguments so it's comfortable to work with them"""
        # the sort_by part
        if arguments["sort_by"]:
            d = {}
            lst = arguments["sort_by"].split(";")
            for ls in lst:
                if ":" in ls:
                    ls = ls.split(":")
                    d[ls[0]] = ls[1]
                else:
                    d[ls] = "asc"
            arguments["sort_by"] = d

        # the group_by part
        if arguments["group_by"]:
            arguments["group_by"] = arguments["group_by"].split(";")
        return arguments

    @staticmethod
    def columns_reform_arguments(arguments):
        """Reforms columns arguments so it's comfortable to work with them"""
        if arguments["columns"]:
            if arguments["columns"] == "all":
                arguments["columns"] = []
            else:
                arguments["columns"] = arguments["columns"].split(";")
        else:
            arguments["columns"] = []
        # if all of the columns should be selected with grouping
        if arguments["group_by"] and arguments["columns"] == []:
            arguments["columns"] = ["id", "date", "channel", "country", "os", "impressions",
                                    "clicks", "installs", "spend", "revenue", "cpi"]
        return arguments

    @staticmethod
    def select_making_query(arguments):
        """Creates the SELECT part of the query from the given columns"""
        column_order = [] # to place colimt in the right order later
        if arguments["columns"]: # if there are columns
            non_aggr_columns_buff = [] # for non aggregatable columns
            aggr_columns = [] # for group_by columns
            if arguments["group_by"]: # if there is a group_by
                # separate column to aggr_columns and non_aggr
                for column in arguments['columns']:
                    if column not in arguments["group_by"]:
                        non_aggr_columns_buff.append(column)
                    else:
                        aggr_columns.append(column)
                # add groping columns to SELECT if it's nedeed
                for column in arguments["group_by"]:
                    if column not in aggr_columns:
                        aggr_columns.append(column)
                        arguments["columns"].append(column)
                non_aggr_columns = [] # non_aggr_columns = non_aggr_columns_buff + SUM, ANG, COUNT etc.
                # preparing non_aggr_column for the query (clicks = SUM(clicks) etc.)
                for non_aggr_column in non_aggr_columns_buff:
                    if non_aggr_column == "cpi":
                        non_aggr_columns.append(f"ROUND(AVG({non_aggr_column}), 4) AS {non_aggr_column}")
                    elif non_aggr_column == "date" or non_aggr_column == "id" or non_aggr_column == "os"\
                            or non_aggr_column == "country" or non_aggr_column == "channel":
                        non_aggr_columns.append(f"COUNT({non_aggr_column}) AS {non_aggr_column}")
                    else:
                        non_aggr_columns.append(f"SUM({non_aggr_column}) AS {non_aggr_column}")
                # form a SELECT and column_order for the right display
                select_columns = aggr_columns + non_aggr_columns
                column_order = aggr_columns + non_aggr_columns_buff # becuse there are plain aggr_columns
                query = f"SELECT {(', '.join(select_columns))} FROM Logs"
            # if there is no grouping
            else:
                query = f"SELECT {(', '.join(arguments['columns']))} FROM Logs"
                column_order = arguments["columns"]
        # if there are no column => all of the columns should be selected
        else:
            query = "SELECT * FROM Logs"
        return query, column_order

    @staticmethod
    def filter_making_query(arguments):
        """Creates the WHERE part of the query from the given filters"""
        if arguments["filter_by"]:
            subquery = " WHERE "
            for key, value in arguments["filter_by"].items():
                if key == "date_from" or key == "date_to":
                    subquery += f"date {value} AND "
                else:
                    subquery += f"{key} {value} AND "
            subquery = subquery[:-5]
            return subquery
        return ""

    @staticmethod
    def group_making_query(arguments):
        """Creates the GROUP BY part of the query from the given group_by columns"""
        if arguments["group_by"]:
            subquery = " GROUP BY "
            for group in arguments["group_by"]:
                subquery += group + ", "
            subquery = subquery[:-2]
            return subquery
        return ""

    @staticmethod
    def sort_making_query(arguments):
        """Creates the ORDER BY part of the query from the given sort_by columns"""
        if arguments["sort_by"]:
            subquery = " ORDER BY "
            for key, value in arguments["sort_by"].items():
                subquery += f"{key} {value.upper()}, "
            subquery = subquery[:-2]
            return subquery
        return ""

    @staticmethod
    def forming_a_response(query, logs, columns):
        """Puts everything together to form an appropriate json dictionary answer"""
        # if all of the columns are selected
        rows, d, k = [], {}, 0
        if len(columns) == 0:
            for log in logs:
                k += 1
                d = {
                    "id": log.id, "date": datetime.strptime(log.date[:-16:], "%Y-%m-%d").strftime("%Y-%m-%d"),
                    "channel": log.channel, "country": log.country, "os": log.os, "impressions": log.impressions,
                    "clicks": log.clicks, "installs": log.installs, "spend": log.spend,"revenue": log.revenue,
                    "cpi": log.cpi
                }
                rows.append(d)
        # if selected only certain columns
        else:
            for log in logs:
                k += 1
                d = {}
                for column, column_id in columns.items():
                    if column == "date":
                        try:
                            d[column] = datetime.strptime(log[column_id][:-16:], "%Y-%m-%d").strftime("%Y-%m-%d")
                        # when it's COUNT(date)
                        except TypeError:
                            d[column] = log[column_id]
                    else:
                        d[column] = log[column_id]
                rows.append(d)
        # add the query info and return the answer
        final_dict = {"query_info": {"rows_returned": k, "sql_query": query},
                      "query_result": rows}
        return final_dict




