import pandas as pd
import pandas_datareader.io as web
import keen
from keen.client import KeenClient
import datetime as dt

client = KeenClient(
    project_id=open("project_id.txt", 'r').read(),
    master_key=open("master_key.txt", 'r').read(),
    write_key=open("write_key.txt", 'r').read(),
    read_key=open("read_key.txt", 'r').read()
)


def end_day():
    day = int(input("What day would you like the query to end?"))
    return day


def end_month():
    month = int(input("What month would you like the query to end?"))
    return month


def end_year():
    year = int(input("What year would you like the query to end?"))
    return year


def daily_query_start(day, month, year):
    start_day = dt.datetime(year, month, day) - dt.timedelta(30)
    query = {'end': str(dt.datetime(year, month, day).date()), 'start': str(start_day.date())}
    return query



def extract_date(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['end'],'%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%y')
        x += 1


def app_data_daily(month, day, year):
    temp_df = pd.DataFrame()
    app_data = client.count_unique('Page', 'user.pk',
                                   timeframe=daily_query_start(day, month, year),
                                   timezone=5,
                                   interval='daily')
    extract_date(app_data)
    if temp_df.empty:
        temp_df = pd.DataFrame(app_data)
    else:
        temp_df = temp_df.join(app_data)

    temp_df.set_index('Date',inplace=True)
    print(temp_df)

app_data_daily(end_month(), end_day(), end_year())
