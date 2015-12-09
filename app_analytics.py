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

end_month = int(input("What month would you like the query to end?"))
end_day = int(input("What day would you like the query to end?"))
end_year = int(input("What year would you like the query to end?"))
query_size = int(input("How many days do you want in this query?"))


def daily_query_start(day, month, year):
    start_day = dt.datetime(year, month, day) - dt.timedelta(30)
    query = {'end': str(dt.datetime(year, month, day).date()), 'start': str(start_day.date())}
    return query


def monthly_query_start(day, month, year):
    monthly_start_day = dt.datetime(year, month, day) - dt.timedelta(60)
    monthly_end_day = dt.datetime(year, month, day) - dt.timedelta(30)
    query = {'end': str(monthly_end_day), 'start': str(monthly_start_day)}
    return query


def extract_date(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['end'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m/%d/%Y')
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
        app_data = pd.DataFrame(app_data)
        temp_df = temp_df.join(app_data)

    temp_df.set_index('Date', inplace=True)
    print(temp_df)


def app_data_monthly(month, day, year):
    x = 0
    day1 = day
    temp_df = pd.DataFrame
    while x < query_size:
        app_data = client.count_unique('Page', 'user.pk',
                                       timeframe=monthly_query_start(day1, month, year),
                                       timezone=5,
                                       interval='yearly')
        extract_date(app_data)
        df = pd.DataFrame(app_data)
        # df.set_index('Date',inplace=True)
        if temp_df.empty:
            temp_df = df
        else:
            temp_df = temp_df.merge(df, how='outer')
        x += 1
        day1 = int((dt.datetime(year, month, day1) + dt.timedelta(1)).strftime('%d'))

    print(temp_df)

# app_data_daily(end_month, end_day, end_year)
app_data_monthly(day=end_day, month=end_month, year=end_year)
