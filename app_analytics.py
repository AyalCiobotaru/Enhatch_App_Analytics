import pandas as pd
import pandas_datareader.io as web
import keen
from keen.client import KeenClient
import plotly.plotly as py
import cufflinks as cl
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
    start_day = dt.datetime(year, month, day) - dt.timedelta(query_size-1)
    query = {'end': str(dt.datetime(year, month, (day+1)).date()), 'start': str(start_day.date())}
    return query


def monthly_query_start(day, month, year):
    monthly_start_day = dt.datetime(year, month, day) - dt.timedelta(query_size+30)
    monthly_end_day = dt.datetime(year, month, day) - dt.timedelta(query_size-1)
    query = {'end': str(monthly_end_day), 'start': str(monthly_start_day)}
    return query


def extract_date_daily(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['start'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y')
        x += 1


def extract_date_monthly(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['end'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y')
        x += 1


def app_data_daily(month, day, year):
    temp_df = pd.DataFrame()
    app_data = client.count_unique('Page', 'user.pk',
                                   timeframe=daily_query_start(day, month, year),
                                   timezone=5,
                                   interval='daily')
    extract_date_daily(app_data)
    if temp_df.empty:
        temp_df = pd.DataFrame(app_data)
    else:
        app_data = pd.DataFrame(app_data)
        temp_df = temp_df.join(app_data)

    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': 'DAU'}, inplace=True)
    temp_df.to_pickle('DAU.pickle')
    print(temp_df.head())


def app_data_monthly(month, day, year):
    x = 0
    day1 = day
    temp_df = pd.DataFrame
    while x < query_size:
        app_data = client.count_unique('Page', 'user.pk',
                                       timeframe=monthly_query_start(day1, month, year),
                                       timezone=5,
                                       interval='yearly')
        extract_date_monthly(app_data)
        df = pd.DataFrame(app_data)

        if temp_df.empty:
            temp_df = df
        else:
            temp_df = temp_df.merge(df, how='outer')
        x += 1
        day1 = int((dt.datetime(year, month, day1) + dt.timedelta(1)).strftime('%d'))
    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': 'MAU'}, inplace=True)
    temp_df.to_pickle('MAU.pickle')
    print(temp_df.head())

app_data_daily(month=end_month, day=end_day, year=end_year)
app_data_monthly(day=end_day, month=end_month, year=end_year)

mau_df = pd.read_pickle('MAU.pickle')
dau_df = pd.read_pickle('DAU.pickle')
mau_dau_df = dau_df.join(mau_df)
mau_dau_df.to_pickle('MAU-DAU.pickle')

division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
df = pd.DataFrame(division)
df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
main_df = mau_dau_df.join(df)

df.iplot(kind='scatter', filename='cufflinks/cf-simple-line')
print(df)
