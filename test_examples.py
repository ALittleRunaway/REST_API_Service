"""Example queries for the tests"""

class ExamleQueries():
    """Class contains test queries, arguments and results"""

    query_1 = "http://127.0.0.1:5000/query?columns=impressions;clicks&filter_by=date_to:2017-06-01&" \
              "group_by=channel;country&sort_by=clicks:desc"
    query_2 = "http://127.0.0.1:5000/query?columns=installs&filter_by=date_from:2017-05-02;" \
              "date_to:2020-06-01;os:ios&group_by=date&sort_by=date"
    query_3 = "http://127.0.0.1:5000/query?columns=revenue&filter_by=date:2017-06-01;country:" \
              "US&group_by=os&sort_by=revenue:desc"
    query_4 = "http://127.0.0.1:5000/query?columns=cpi;spend&filter_by=country:CA&group_by=channel&sort_by=cpi:desc"
    query_5 = "http://127.0.0.1:5000/query?group_by=os&filter_by=os:%3C%3Eandroid"

    arguments_1 = {
        "columns": "impressions;clicks",
        "filter_by": "date_to:2017-06-01",
        "group_by": "channel;country",
        "sort_by": "clicks:desc",
        }
    arguments_2 = {
        "columns": "installs",
        "filter_by": "date_from:2017-05-02;date_to:2020-06-01;os:ios",
        "group_by": "date",
        "sort_by": "date",
        }
    arguments_3 = {
        "columns": "revenue",
        "filter_by": "date:2017-06-01;country:US",
        "group_by": "os",
        "sort_by": "revenue:desc",
        }
    arguments_4 = {
        "columns": "cpi;spend",
        "filter_by": "country:CA",
        "group_by": "channel",
        "sort_by": "cpi:desc",
        }
    arguments_5 = {
        "columns": None,
        "filter_by": "os:<>android",
        "group_by": "os",
        "sort_by": None,
        }

    result_1 = {
  "query_info": {
    "rows_returned": 25,
    "sql_query": "SELECT channel, country, SUM(impressions) AS impressions, SUM(clicks) AS clicks FROM Logs "
                 "WHERE date <'2017-06-01' GROUP BY channel, country ORDER BY clicks DESC"
  },
  "query_result": [
    {
      "country": "US",
      "channel": "adcolony",
      "impressions": 498861,
      "clicks": 12277
    },
    {
      "country": "US",
      "channel": "apple_search_ads",
      "impressions": 347554,
      "clicks": 10738
    },
    {
      "country": "GB",
      "channel": "vungle",
      "impressions": 249197,
      "clicks": 8831
    },
    {
      "country": "US",
      "channel": "vungle",
      "impressions": 249618,
      "clicks": 7440
    },
    {
      "country": "US",
      "channel": "unityads",
      "impressions": 201584,
      "clicks": 6888
    },
    {
      "country": "US",
      "channel": "google",
      "impressions": 198077,
      "clicks": 5884
    },
    {
      "country": "DE",
      "channel": "facebook",
      "impressions": 200901,
      "clicks": 5851
    },
    {
      "country": "US",
      "channel": "chartboost",
      "impressions": 149110,
      "clicks": 4437
    },
    {
      "country": "GB",
      "channel": "unityads",
      "impressions": 148999,
      "clicks": 4357
    },
    {
      "country": "GB",
      "channel": "chartboost",
      "impressions": 99655,
      "clicks": 3919
    },
    {
      "country": "GB",
      "channel": "google",
      "impressions": 100441,
      "clicks": 3876
    },
    {
      "country": "GB",
      "channel": "apple_search_ads",
      "impressions": 99892,
      "clicks": 3478
    },
    {
      "country": "CA",
      "channel": "unityads",
      "impressions": 98886,
      "clicks": 3402
    },
    {
      "country": "US",
      "channel": "facebook",
      "impressions": 99130,
      "clicks": 3342
    },
    {
      "country": "FR",
      "channel": "google",
      "impressions": 99532,
      "clicks": 3042
    },
    {
      "country": "FR",
      "channel": "chartboost",
      "impressions": 100149,
      "clicks": 2962
    },
    {
      "country": "GB",
      "channel": "facebook",
      "impressions": 99203,
      "clicks": 2888
    },
    {
      "country": "DE",
      "channel": "apple_search_ads",
      "impressions": 49468,
      "clicks": 1967
    },
    {
      "country": "DE",
      "channel": "chartboost",
      "impressions": 99431,
      "clicks": 1943
    },
    {
      "country": "DE",
      "channel": "unityads",
      "impressions": 50804,
      "clicks": 1541
    },
    {
      "country": "FR",
      "channel": "facebook",
      "impressions": 49803,
      "clicks": 1480
    },
    {
      "country": "CA",
      "channel": "chartboost",
      "impressions": 49316,
      "clicks": 1477
    },
    {
      "country": "CA",
      "channel": "google",
      "impressions": 49780,
      "clicks": 1459
    },
    {
      "country": "CA",
      "channel": "facebook",
      "impressions": 49974,
      "clicks": 1441
    },
    {
      "country": "DE",
      "channel": "google",
      "impressions": 47202,
      "clicks": 476
    }
  ]
}
    result_2 = {
  "query_info": {
    "rows_returned": 30,
    "sql_query": "SELECT date, SUM(installs) AS installs FROM Logs WHERE date >='2017-05-02' AND date <'2020-06-01' "
                 "AND os ='ios' GROUP BY date ORDER BY date ASC"
  },
  "query_result": [
    {
      "date": "2017-05-17",
      "installs": 755
    },
    {
      "date": "2017-05-18",
      "installs": 765
    },
    {
      "date": "2017-05-19",
      "installs": 745
    },
    {
      "date": "2017-05-20",
      "installs": 816
    },
    {
      "date": "2017-05-21",
      "installs": 751
    },
    {
      "date": "2017-05-22",
      "installs": 781
    },
    {
      "date": "2017-05-23",
      "installs": 813
    },
    {
      "date": "2017-05-24",
      "installs": 789
    },
    {
      "date": "2017-05-25",
      "installs": 875
    },
    {
      "date": "2017-05-26",
      "installs": 725
    },
    {
      "date": "2017-05-27",
      "installs": 712
    },
    {
      "date": "2017-05-28",
      "installs": 664
    },
    {
      "date": "2017-05-29",
      "installs": 752
    },
    {
      "date": "2017-05-30",
      "installs": 762
    },
    {
      "date": "2017-05-31",
      "installs": 685
    },
    {
      "date": "2017-06-01",
      "installs": 623
    },
    {
      "date": "2017-06-02",
      "installs": 771
    },
    {
      "date": "2017-06-03",
      "installs": 608
    },
    {
      "date": "2017-06-04",
      "installs": 766
    },
    {
      "date": "2017-06-05",
      "installs": 791
    },
    {
      "date": "2017-06-06",
      "installs": 677
    },
    {
      "date": "2017-06-07",
      "installs": 757
    },
    {
      "date": "2017-06-08",
      "installs": 708
    },
    {
      "date": "2017-06-09",
      "installs": 826
    },
    {
      "date": "2017-06-10",
      "installs": 804
    },
    {
      "date": "2017-06-11",
      "installs": 865
    },
    {
      "date": "2017-06-12",
      "installs": 686
    },
    {
      "date": "2017-06-13",
      "installs": 777
    },
    {
      "date": "2017-06-14",
      "installs": 867
    },
    {
      "date": "2017-06-15",
      "installs": 752
    }
  ]
}
    result_3 = {
  "query_info": {
    "rows_returned": 0,
    "sql_query": "SELECT os, SUM(revenue) AS revenue FROM Logs WHERE date ='2017-06-01' AND country ='US' "
                 "GROUP BY os ORDER BY revenue DESC"
  },
  "query_result": []
}
    result_4 = {
  "query_info": {
    "rows_returned": 4,
    "sql_query": "SELECT channel, ROUND(AVG(cpi), 4) AS cpi, SUM(spend) AS spend FROM Logs WHERE "
                 "country ='CA' GROUP BY channel ORDER BY cpi DESC"
  },
  "query_result": [
    {
      "channel": "facebook",
      "cpi": 2.1645,
      "spend": 1164.0
    },
    {
      "channel": "chartboost",
      "cpi": 2.0,
      "spend": 1274.0
    },
    {
      "channel": "unityads",
      "cpi": 2.0,
      "spend": 2642.0
    },
    {
      "channel": "google",
      "cpi": 1.87,
      "spend": 999.9000000000004
    }
  ]
}
    result_5 = {
  "query_info": {
    "rows_returned": 1,
    "sql_query": "SELECT os, COUNT(id) AS id, COUNT(date) AS date, COUNT(channel) AS channel, COUNT(country) "
                 "AS country, SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(installs) AS installs, "
                 "SUM(spend) AS spend, SUM(revenue) AS revenue, ROUND(AVG(cpi), 4) AS cpi FROM Logs WHERE os "
                 "<>'android' GROUP BY os"
  },
  "query_result": [
    {
      "os": "ios",
      "id": 590,
      "date": 590,
      "channel": 590,
      "country": 590,
      "impressions": 3875578,
      "clicks": 118314,
      "installs": 22668,
      "spend": 220083.98999999955,
      "revenue": 64743.35999999985,
      "cpi": 98.5824
    }
  ]
}
