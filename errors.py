"""Handling different types of errors"""
import re

class Errors():
    """Class handles errors and returns appropriate json dictionary"""

    @staticmethod
    def existing_errors(e):
        """For the sqlalchemy errors"""
        d = {'error_info': {}}
        pattern_name = r"(?<=sqlite3.).+(?=\) )"
        d['error_info']['error_code'] = e.code
        d['error_info']['error_name'] = re.findall(pattern_name, str(e.args))[0]
        d['error_info']['error_detail'] = str(e.orig)
        d['error_info']['sql_query'] = e.statement

        return d

    @staticmethod
    def created_errors(error_name):
        """For errors we handle ourselves"""
        d = {'error_info': {}}

        if error_name == "IndexError":
            d['error_info']['error_name'] = "FilterByPairError"
            d['error_info']['error_detail'] = "There must be ':' missing or there " \
                                              "is an unnecessary ';' in your 'filter_by' block"
            d['error_info']['error_hint'] = "Try ckecing all of the ':' and ';' in the 'filter_by'"

        return d
