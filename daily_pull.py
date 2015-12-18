import pandas as pd
from math import ceil
import datetime as dt
from client_and_app_keys import client, account_app_keys


# Function to generate the DAU query
def daily_query_start(day, month, year, weekend, query_size):
    if not weekend:
        start_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
        num_weeks = ceil(query_size / 7)
        # adds one extra week if the remainder is 0 or the user will get one week short
        if query_size % 7 == 0:
            num_weeks += 1
        week_day = start_day.weekday()
        # checks to see if the start day is a weekend and if it is, makes the start day the following monday
        if week_day == 5:
            day_of_week = start_day + dt.timedelta(2)
        elif week_day == 6:
            day_of_week = start_day + dt.timedelta(1)
        else:
            day_of_week = start_day
        query = []

        # goes day by day until it hits Saturday then puts it into the query list in the Keen.io  correct format
        while num_weeks != 1:
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
            num_weeks -= 1

        # runs for the last week trying to find the end day and not go past it
        if day_of_week == dt.datetime(year, month, day):
            next_day1 = day_of_week + dt.timedelta(1)
            query_part = {'end': str(next_day1), 'start': str(day_of_week)}
        else:
            next_day1 = day_of_week + dt.timedelta(1)
            if next_day1 == dt.datetime(year, month, day):
                next_day2 = next_day1 + dt.timedelta(1)
                query_part = {'end': str(next_day2), 'start': str(day_of_week)}
            else:
                next_day2 = next_day1 + dt.timedelta(1)
                if next_day2 == dt.datetime(year, month, day):
                    next_day3 = next_day2 + dt.timedelta(1)
                    query_part = {'end': str(next_day3), 'start': str(day_of_week)}
                else:
                    next_day3 = next_day2 + dt.timedelta(1)
                    if next_day3 == dt.datetime(year, month, day):
                        next_day4 = next_day3 + dt.timedelta(1)
                        query_part = {'end': str(next_day4), 'start': str(day_of_week)}
                    else:
                        next_day4 = next_day3 + dt.timedelta(1)
                        next_day5 = next_day4 + dt.timedelta(1)
                        query_part = {'end': str(next_day5), 'start': str(day_of_week)}
        query.append(query_part)
        return query

    else:
        start_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
        query = {'end': str(dt.datetime(year, month, (day+1)).date()), 'start': str(start_day.date())}
        return query


# Function to generate the daily date from the Keen.io ISO date format
def extract_date_daily(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['start'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y')
        x += 1


# Function that actually pulls the daily data from Keen
def app_data_daily(month, day, year, weekend, account, query_size):
    # process that breaks up the daily query into a bunch of little queries that excludes weekends
    if not weekend:
        temp_df = pd.DataFrame()
        for item in daily_query_start(day=day, month=month, year=year, weekend=weekend, query_size=query_size):
            if account != "":
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=item,
                                               timezone=5,
                                               interval='daily',
                                               filters=[
                                                   {'operator': 'eq',
                                                    'property_name': 'app_key',
                                                    'property_value': account_app_keys[account]
                                                    }])
            else:
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

    # if the user wants to INCLUDE weekends, the above is skipped and this is run
    else:
        temp_df = pd.DataFrame()
        if account != "":
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=daily_query_start(day=day, month=month, year=year,
                                                                       weekend=weekend, query_size=query_size),
                                           timezone=5,
                                           interval='daily',
                                           filters=[
                                               {'operator': 'eq',
                                                'property_name': 'app_key',
                                                'property_value': account_app_keys[account]
                                                }])
        else:
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=daily_query_start(day=day, month=month, year=year,
                                                                       weekend=weekend, query_size=query_size),
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
    print(temp_df.head())
