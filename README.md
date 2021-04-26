# REST-API service for processing database queries

---

### You are able to:

1. filter by time range (date_from+date_to), channels, countries, operating systems.
2. group by one or more columns: date, channel, country, operating system.
3. sort by any column in ascending or descending order.
4. see derived metric CPI (cost per install) for every row.


## About the database
The provided data was imported into a relational database (statistics.db) from the CSV file (dataset.csv) with this script (creating_db.py).\
The CPI column was added to the table during this process, so it's always there. If you don't want to see the CPI column in your query result, don't enter it in the columns argument in your url. 

---

## How to use it

There are four arguments. If you don't add any of them to the url (except columns) it won't be in the query.

1. **columns** 
- Enter columns you want to see, separated by **;**.\
*Example:    columns=os;impressions;clicks;cpi*
- If you want to see all the columns, you can type "all", leave it unfilled 
or don't add column argument to your url at all.\
*Example:    columns=all* \
*Example:    columns=* \
*Example:* 

2. **filter_by**
- Enter columns and filter, separating columns by **;** and column and filter by **:**\
*Example:    filter_by=date:2017-06-01;country:US*
- You don't have to write **=** or **""**. They will be added automatically. \
*Example:    filter_by=os:ios;date:2020-12-12*  **=**  *os = 'ios' AND date = '2020-12-12'*
- For the **>=** and **<=** signs use **>>** and **<<**.\
*Example:    filter_by=clicks:>>100;cpi:<<2*  **=**  *clicks >= 100 AND cpi <= 2*
- If you want the time range, use **date_from**(>= some_date) and **date_to**(< some_date).\
*Example:    filter_by=date_from:2017-05-02;date_to:2020-06-01*  **=**  *date >= '2017-05-02' AND date < '2020-06-01'*
- You can also use the **date** column, but only or comparison (**=** or **<>**).\
*Example:    filter_by=date:2020-06-09*  **=**  *date = '2020-06-09'*\
*Example:    filter_by=date:<>2020-06-09*  **=**  *date <> '2020-06-09'*


3. **group_by**
- Enter columns you want your query to be grouped by\
*Example:    group_by=os;country*
- You can do not enter your group_by columns to SELECT. They will be added automatically.\
*Example:    columns=cpi&group_by=os;country*  **=**  *columns=os;country;cpi&group_by=os;country*
- When you have a grouping, different functions are used for the SELECT columns.\
*Nothing*: the group_by columns\
*SUM*: impressions, installs, clicks, spend, revenue\
*COUNT*: date, id, os, country, channel\
*ROUND(AVG()), 4)*: cpi


4. **sort_by**
- Enter columns and order of sorting, separating columns by **;** and column and order by **:**.\
*Example:    sort_by=date:asc;spend:asc;cpi:desc*
- If you leave the order unfilled it will be ascending by default.\
*Example:    sort_by=date;spend;cpi:desc*  **=**  *sort_by=date:asc;spend:asc;cpi:desc*

---

## Example queries

1. Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order.\
``SELECT country, channel, SUM(impressions) as impressions, SUM(clicks) as clicks FROM Logs WHERE date < '2017-06-01' GROUP BY channel, country ORDER BY clicks DESC;``\
**url**:  http://127.0.0.1:5000/query?columns=impressions;clicks&filter_by=date_to:2017-06-01&group_by=channel;country&sort_by=clicks:desc

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.\
``SELECT date, SUM(installs) AS installs FROM Logs WHERE date > "2017-05-01" AND date < "2020-06-01" AND os="ios" GROUP BY date ORDER BY date ASC;``\
**url**:  http://127.0.0.1:5000/query?columns=installs&filter_by=date_from:2017-05-02;date_to:2020-06-01;os:ios&group_by=date&sort_by=date

3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.\
``SELECT os, SUM(revenue) AS revenue FROM Logs WHERE date = "2017-06-01" AND country = "US" GROUP BY os ORDER BY revenue DESC;``\
**url**:  http://127.0.0.1:5000/query?columns=revenue&filter_by=date:2017-06-01;country:US&group_by=os&sort_by=revenue:desc

4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order..\
``SELECT channel, ROUND(AVG(cpi), 4) AS cpi, SUM(spend) AS spend FROM logs WHERE country = "CA" GROUP BY channel ORDER BY cpi DESC;``\
**url**:  http://127.0.0.1:5000/query?columns=cpi;spend&filter_by=country:CA&group_by=channel&sort_by=cpi:desc

---

## Repository review

**app.py** - The main script which starts the server.\
**methods.py** - Contains the class Handler, which does the main job: creates a query and returns a response.\
**creating_db.py** - Script for putting the data from CSV file to the database.\
**data\dataset.csv** - The CSV file with data.\
**dtatistics.db** - The database.\
**errors.py** - Handles the exceptions and returns an appropriate response.\
**unit_tests.py** - Some unit-tests for the 'methods.py'\
**test_examples** - Stores some data for unit-testing.\
**README.md** - This README file.