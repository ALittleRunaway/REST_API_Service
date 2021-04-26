"""Unit-tests for the 'methods.py'"""
import unittest
from methods import Handler
from test_examples import ExamleQueries


class creating_answerTestCase(unittest.TestCase):
    """Test 'creating_answer' function"""

    def test_creating_answer(self):
        """Test returning answers"""
        self.assertEqual(Handler.creating_answer(
            ExamleQueries.arguments_1),
            ExamleQueries.result_1)
        self.assertEqual(Handler.creating_answer(
            ExamleQueries.arguments_2),
            ExamleQueries.result_2)
        self.assertEqual(Handler.creating_answer(
            ExamleQueries.arguments_3),
            ExamleQueries.result_3)
        self.assertEqual(Handler.creating_answer(
            ExamleQueries.arguments_4),
            ExamleQueries.result_4)
        self.assertEqual(Handler.creating_answer(
            ExamleQueries.arguments_5),
            ExamleQueries.result_5)


class ColumnOrderTestCase(unittest.TestCase):
    """Test 'column_order' function"""

    def test_column_order(self):
        """Test 'column_order' function"""
        self.assertEqual(Handler.column_order(
            {"columns": ["id", "date", "channel", "country", "os"]}),
            {"id": 0, "date": 1, "channel": 2, "country": 3, "os": 4})
        self.assertEqual(Handler.column_order(
            {"columns": ["id", "date", "channel", "country", "os", "impressions", "clicks"]}),
            {"id": 0, "date": 1, "channel": 2, "country": 3, "os": 4, "impressions": 5, "clicks": 6})
        self.assertEqual(Handler.column_order(
            {"columns": ["id"]}),
            {"id": 0})
        self.assertEqual(Handler.column_order(
            {"columns": []}),
            {})
        self.assertEqual(Handler.column_order(
            {"jjj": ["id", "date", "channel", "country", "os"], "columns": ["id", "date"]}),
            {"id": 0, "date": 1})


class FilterByReformArgumentsTestCase(unittest.TestCase):
    """Test 'filter_by_reform_arguments' function"""

    def test_filter_by_reform_arguments(self):
        """Test 'filter_by_reform_arguments' function with different arguments"""
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": "clicks:<100;cpi:50;os:android"}),
            {"filter_by": {"clicks": "<100", "cpi": "=50", "os": "='android'"}})
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": "impressions:<<100;cpi:>>50;country:CA;channel:<>google"}),
            {"filter_by": {"impressions": "<=100", "cpi": ">=50", "country": "='CA'", "channel": "<>'google'"}})
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": "date_from:2020-08-12;date_to:2020-08-12"}),
            {"filter_by": {"date_from": ">='2020-08-12'", "date_to": "<'2020-08-12'"}})
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": "date:2020-08-07"}),
            {"filter_by": {"date": "='2020-08-07'"}})
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": "date:<>2020-08-12"}),
            {"filter_by": {"date": "<>'2020-08-12'"}})
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": None}),
            {"filter_by": None})
        self.assertEqual(Handler.filter_by_reform_arguments(
            {"filter_by": []}),
            {"filter_by": []})


class SortGroupByFilterByReformArgumentsTestCase(unittest.TestCase):
    """Test 'sort_group_by_filter_by_reform_arguments' function"""

    def test_group_by_filter_by_reform_arguments(self):
        """Test 'filter_by_reform_arguments' function 'sort_by' case"""
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"sort_by": "clicks;cpi:desc;os", "group_by": None}),
            {"sort_by": {"clicks": "asc", "cpi": "desc", "os": "asc"}, "group_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"sort_by": "impressions;cpi;country;channel", "group_by": None}),
            {"sort_by": {"impressions": "asc", "cpi": "asc", "country": "asc", "channel": "asc"}, "group_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"sort_by": "impressions:desc;cpi:desc;country:;channel:jjj", "group_by": None}),
            {"sort_by": {"impressions": "desc", "cpi": "desc", "country": "", "channel": "jjj"}, "group_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"sort_by": None, "group_by": None}),
            {"sort_by": None, "group_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"sort_by": [], "group_by": None}),
            {"sort_by": [], "group_by": None})

    def test_sort_by_filter_by_reform_arguments(self):
        """Test 'filter_by_reform_arguments' function 'group_by' case"""
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"group_by": "clicks;cpi;os", "sort_by": None}),
            {"group_by": ["clicks", "cpi", "os"], "sort_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"group_by": "impressions;cpi;country;channel", "sort_by": None}),
            {"group_by": ["impressions", "cpi", "country", "channel"], "sort_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"group_by": "impressions; ;567;channel", "sort_by": None}),
            {"group_by": ["impressions", " ", "567", "channel"], "sort_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"group_by": None, "sort_by": None}),
            {"group_by": None, "sort_by": None})
        self.assertEqual(Handler.sort_group_by_filter_by_reform_arguments(
            {"group_by": [], "sort_by": None}),
            {"group_by": [], "sort_by": None})


class ColumnsReformArgumentsTestCase(unittest.TestCase):
    """Test 'columns_reform_arguments' function"""

    def test_columns_reform_arguments_without_group_by(self):
        """Test 'columns_reform_arguments' function without 'group_by'"""
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": "os;clicks;id;date", "group_by": None}),
            {"columns": ["os", "clicks", "id", "date"], "group_by": None})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": "os; ;555;.9-)", "group_by": None}),
            {"columns": ["os", " ", "555", ".9-)"], "group_by": None})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": "all", "group_by": None}),
            {"columns": [], "group_by": None})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": None, "group_by": None}),
            {"columns": [], "group_by": None})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": [], "group_by": None}),
            {"columns": [], "group_by": None})


    def test_columns_reform_arguments_with_group_by(self):
        """Test 'columns_reform_arguments' function with 'group_by'"""
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": "os;clicks;id;date", "group_by": ["os"]}),
            {"columns": ["os", "clicks", "id", "date"], "group_by": ["os"]})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": "os; ;555;.9-)", "group_by": ["os"]}),
            {"columns": ["os", " ", "555", ".9-)"], "group_by": ["os"]})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": "all", "group_by": ["os"]}),
            {"columns": ["id", "date", "channel", "country", "os", "impressions",
                         "clicks", "installs", "spend", "revenue", "cpi"], "group_by": ["os"]})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": None, "group_by": ["os"]}),
            {"columns": ["id", "date", "channel", "country", "os", "impressions",
                         "clicks", "installs", "spend", "revenue", "cpi"], "group_by": ["os"]})
        self.assertEqual(Handler.columns_reform_arguments(
            {"columns": [], "group_by": ["os"]}),
            {"columns": ["id", "date", "channel", "country", "os", "impressions",
                         "clicks", "installs", "spend", "revenue", "cpi"], "group_by": ["os"]})


class SelectMakingQueryTestCase(unittest.TestCase):
    """Test 'select_making_query' function"""

    def test_select_making_query(self):
        """Test 'select' part for the query"""
        self.assertEqual(Handler.select_making_query(
            {"columns": []}),
            ('SELECT * FROM Logs', []))
        self.assertEqual(Handler.select_making_query(
            {"columns": ["id", "date", "channel", "country", "os"], "group_by": None}),
            ('SELECT id, date, channel, country, os FROM Logs', ["id", "date", "channel", "country", "os"]))
        self.assertEqual(Handler.select_making_query(
            {"columns": [" ", "90=0-0-", "...", "888", "os"], "group_by": None}),
            ('SELECT  , 90=0-0-, ..., 888, os FROM Logs', [" ", "90=0-0-", "...", "888", "os"]))
        self.assertEqual(Handler.select_making_query(
            {"columns": ["os", "channel", "spend"], "group_by": ["os", "channel"]}),
            ('SELECT os, channel, SUM(spend) AS spend FROM Logs', ["os", "channel", "spend"]))
        self.assertEqual(Handler.select_making_query(
            {"columns": ["spend"], "group_by": ["os", "channel"]}),
            ('SELECT os, channel, SUM(spend) AS spend FROM Logs', ["os", "channel", "spend"]))
        self.assertEqual(Handler.select_making_query(
            {"columns": ["cpi", "id", "impressions", "date", "country"], "group_by": ["os", "channel"]}),
            ('SELECT os, channel, ROUND(AVG(cpi), 4) AS cpi, COUNT(id) AS id, SUM(impressions) AS impressions, '
             'COUNT(date) AS date, COUNT(country) AS country FROM Logs',
             ["os", "channel", "cpi", "id", "impressions", "date", "country"]))


class FilterMakingQueryTestCase(unittest.TestCase):
    """Test 'filter_making_query' function"""

    def test_filter_making_query(self):
        """Test 'where' part for the query"""
        self.assertEqual(Handler.filter_making_query(
            {"filter_by": {"clicks": "<100", "cpi": "=50", "os": "='android'"}}),
            " WHERE clicks <100 AND cpi =50 AND os ='android'")
        self.assertEqual(Handler.filter_making_query(
            {"filter_by": {"impressions": "<=100", "cpi": ">=50", "country": "='CA'", "channel": "<>'google'"}}),
            " WHERE impressions <=100 AND cpi >=50 AND country ='CA' AND channel <>'google'")
        self.assertEqual(Handler.filter_making_query(
            {"filter_by": {"date_from": ">='2020-08-12'", "date_to": "<'2020-08-12'", "date": "='2020-05-14'"}}),
            " WHERE date >='2020-08-12' AND date <'2020-08-12' AND date ='2020-05-14'")
        self.assertEqual(Handler.filter_making_query(
            {"filter_by": None}),
            "")
        self.assertEqual(Handler.filter_making_query(
            {"filter_by": []}),
            "")


class GroupMakingQueryTestCase(unittest.TestCase):
    """Test 'group_making_query' function"""

    def test_group_making_query(self):
        """Test 'group by' part for the query"""
        self.assertEqual(Handler.group_making_query(
            {"group_by": ["os", "country", "date"]}),
            " GROUP BY os, country, date")
        self.assertEqual(Handler.group_making_query(
            {"group_by": ["os", "country", "date", "impressions", "clicks", "cpi"]}),
            " GROUP BY os, country, date, impressions, clicks, cpi")
        self.assertEqual(Handler.group_making_query(
            {"group_by": ["", "444", "5 7"]}),
            " GROUP BY , 444, 5 7")
        self.assertEqual(Handler.group_making_query(
            {"group_by": None}),
            "")
        self.assertEqual(Handler.group_making_query(
            {"group_by": []}),
            "")


class SortMakingQueryTestCase(unittest.TestCase):
    """Test 'sort_making_query' function"""

    def test_sort_making_query(self):
        """Test 'order by' part for the query"""
        self.assertEqual(Handler.sort_making_query(
            {"sort_by": {"clcks": "asc", "spend": "asc", "date": "desc"}}),
            " ORDER BY clcks ASC, spend ASC, date DESC")
        self.assertEqual(Handler.sort_making_query(
            {"sort_by": {"country": "desc", "date": "asc", "impressions": "desc", "clicks": "asc", "cpi": "desc"}}),
            " ORDER BY country DESC, date ASC, impressions DESC, clicks ASC, cpi DESC")
        self.assertEqual(Handler.sort_making_query(
            {"sort_by": {"": "asc", "444": "asc", "5 7": "asc"}}),
            " ORDER BY  ASC, 444 ASC, 5 7 ASC")
        self.assertEqual(Handler.sort_making_query(
            {"sort_by": None}),
            "")
        self.assertEqual(Handler.sort_making_query(
            {"sort_by": []}),
            "")


if __name__ == '__main__':
    unittest.main()
