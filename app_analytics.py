import pandas as pd
import pandas_datareader.io as web
import keen
from keen.client import KeenClient
import plotly.plotly as py
import cufflinks as cl
import datetime as dt
from math import ceil


client = KeenClient(
    project_id=open("project_id.txt", 'r').read(),
    master_key=open("master_key.txt", 'r').read(),
    write_key=open("write_key.txt", 'r').read(),
    read_key=open("read_key.txt", 'r').read()
)


def end_date_query():
    print('Specify query end date\n-------------------------')
    global end_month
    end_month = int(input("What month would you like the query to end?"))
    global end_day
    end_day = int(input("What day would you like the query to end?"))
    global end_year
    end_year = int(input("What year would you like the query to end?"))

    x = 1
    while x == 1:
        question = input("\nWould you like to:\n"
                         "1)Go a set number of days back?\n"
                         "2)Pick a specific date in the past to start?\n"
                         "1 or 2?:")
        if question == '1':
            global query_size
            query_size = int(input("How many days do you want in this query?"))
            x = 2
        elif question == '2':
            global start_date_day
            start_date_day = input("What month would you like the query to start?")
            global start_date_month
            start_date_month = int(input("What day would you like the query to start?"))
            global start_date_year
            start_date_year = int(input("What year would you like the query to start?"))
            x = 2
        else:
            print("That wasn't a viable option, please try again and pick 1 or 2")
    x = 1
    while x == 1:
        question2 = input("\nWould you like to include weekends?\nY/N?:")
        global weekends
        if question2 == "Y" or question2 == "y":
            weekends = True
            x = 2
        elif question2 == "N" or question2 == "n":
            weekends = False
            x = 2
        else:
            print("Not a viable option, please try again")


def daily_query_start(day, month, year):
    start_day = dt.datetime(year, month, day) - dt.timedelta(query_size-1)
    query = {'end': str(dt.datetime(year, month, (day+1)).date()), 'start': str(start_day.date())}
    # query = [{'end': '11/27/2015', 'start': '11/23/2015'}, {'end': '11/20/2015', 'start': '11/16/2015'}]
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
    start_day = dt.datetime(year, month, day) - dt.timedelta(query_size-1)
    num_weeks = ceil(query_size / 7)
    day_of_week = start_day.weekday()
    if day_of_week == 5:
        day_of_week = start_day + dt.timedelta(2)
    elif day_of_week == 6:
        day_of_week = start_day + dt.timedelta(1)
    else:
        day_of_week = start_day
    query = []
    for x in range(num_weeks, 0, -1):
        next_day1 = day_of_week + dt.timedelta(1)
        if next_day1.weekday() == 5:
            query_part = {'end': str(next_day1), 'start': str(day_of_week)}
            day_of_week = next_day1 + dt.timedelta(2)
        else:
            next_day2 = next_day1 + dt.timedelta(1)
            if next_day2.weekday() == 5:
                query_part = {'end': str(next_day2), 'start': str(day_of_week)}
                day_of_week = next_day2 + dt.timedelta(2)
            else:
                next_day3 = next_day2 + dt.timedelta(1)
                if next_day3.weekday() == 5:
                    query_part = {'end': str(next_day3), 'start': str(day_of_week)}
                    day_of_week = next_day3 + dt.timedelta(2)
                else:
                    next_day4 = next_day3 + dt.timedelta(1)
                    if next_day4.weekday() == 5:
                        query_part = {'end': str(next_day4), 'start': str(day_of_week)}
                        day_of_week = next_day4 + dt.timedelta(2)
                    else:
                        next_day5 = next_day4 + dt.timedelta(1)
                        query_part = {'end': str(next_day5), 'start': str(day_of_week)}
                        day_of_week = next_day5 + dt.timedelta(2)
        query.append(query_part)
    for item in query:
        app_data = client.count_unique('Page', 'user.pk',
                                       timeframe=item,
                                       timezone=5,
                                       interval='daily')
        extract_date_daily(app_data)
        df = pd.DataFrame(app_data)
        if temp_df.empty:
            temp_df = pd.DataFrame(app_data)
        else:
            temp_df = temp_df.merge(df, how='outer')

    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': 'DAU'}, inplace=True)
    temp_df.to_pickle('DAU.pickle')
    print(temp_df)


def app_data_monthly(month, day, year):
    x = 0
    day1 = day
    month1 = month
    year1 = year
    temp_df = pd.DataFrame
    while x < query_size:
        if not weekends:
            if (dt.datetime(year1, month1, day1) - dt.timedelta(query_size-1)).weekday() == 5 or \
               (dt.datetime(year1, month1, day1) - dt.timedelta(query_size-1)).weekday() == 6:
                new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
                day1 = int(new_date.strftime('%d'))
                month1 = int(new_date.strftime('%m'))
                year1 = int(new_date.strftime('%Y'))
                continue
            else:
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=monthly_query_start(day1, month1, year1),
                                               timezone=5)
                list_dict = [{'Date': str((dt.datetime(year1, month1, day1) -
                                           dt.timedelta(query_size-1)).strftime('%m-%d-%Y')),
                              'value': app_data}]
                df = pd.DataFrame(list_dict)

                if temp_df.empty:
                    temp_df = df
                else:
                    temp_df = temp_df.merge(df, how='outer')
                x += 1
                new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
                day1 = int(new_date.strftime('%d'))
                month1 = int(new_date.strftime('%m'))
                year1 = int(new_date.strftime('%Y'))
        else:
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=monthly_query_start(day1, month1, year1),
                                           timezone=5)
            list_dict = [{'Date': str((dt.datetime(year1, month1, day1) -
                                       dt.timedelta(query_size-1)).strftime('%m-%d-%Y')),
                          'value': app_data}]
            df = pd.DataFrame(list_dict)

            if temp_df.empty:
                temp_df = df
            else:
                temp_df = temp_df.merge(df, how='outer')
            x += 1
            new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
            day1 = int(new_date.strftime('%d'))
            month1 = int(new_date.strftime('%m'))
            year1 = int(new_date.strftime('%Y'))

    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': 'MAU'}, inplace=True)
    temp_df.to_pickle('MAU.pickle')
    print(temp_df)

end_date_query()
app_data_daily(month=end_month, day=end_day, year=end_year)
# app_data_monthly(month=end_month, day=end_day, year=end_year)
# mau_df = pd.read_pickle('MAU.pickle')
# dau_df = pd.read_pickle('DAU.pickle')
# mau_dau_df = dau_df.join(mau_df)
# mau_dau_df.to_pickle('MAU-DAU.pickle')
# division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
# df = pd.DataFrame(division)
# print(df.head())
# df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
# main_df = mau_dau_df.join(df)
#
# print(main_df.head())
#
# df.iplot(kind='scatter', filename='cufflinks/DAU_MAU')
