import pandas as pd
import datetime as dt
from client_and_app_keys import client, account_app_keys


# Function to generate the WAU query
def weekly_query_start(day, month, year, query_size):
    weekly_start_day = dt.datetime(year, month, day) - dt.timedelta(query_size + 6)
    weekly_end_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(weekly_end_day), 'start': str(weekly_start_day)}
    return query


# Function to generate the MAU query
def monthly_query_start(day, month, year, query_size):
    monthly_start_day = dt.datetime(year, month, day) - dt.timedelta(query_size + 30)
    monthly_end_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(monthly_end_day), 'start': str(monthly_start_day)}
    return query


# Function to generate the YAU query
def yearly_query_start(day, month, year, query_size):
    yearly_start_day = dt.datetime(year, month, day) - dt.timedelta(query_size + 364)
    yearly_end_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(yearly_end_day), 'start': str(yearly_start_day)}
    return query


# Function that actually pulls the monthly data from Keen
def app_data_weekly_monthly_yearly(month, day, year, choice, weekend, account, query_size):
    # this query might be able to be modified
    # it takes the first day specified in the query, subtracts thirty and puts the monthly data for that date.
    # then goes on to the next day and does the same thing for a rolling thirty feel.
    x = 0
    day1 = day
    month1 = month
    year1 = year
    temp_df = pd.DataFrame  # empty dataframe to fill
    while x < query_size:
        if choice == 1:
            query = monthly_query_start(day1, month1, year1, query_size=query_size)
        elif choice == 2:
            query = weekly_query_start(day1, month1, year1, query_size=query_size)
        else:
            query = yearly_query_start(day1, month1, year1, query_size=query_size)

        # process to exclude weekends
        if not weekend:
            if (dt.datetime(year1, month1, day1) - dt.timedelta(query_size-1)).weekday() == 5 or \
               (dt.datetime(year1, month1, day1) - dt.timedelta(query_size-1)).weekday() == 6:
                new_date = (dt.datetime(year1, month1, day1) + dt.timedelta(1))
                day1 = int(new_date.strftime('%d'))
                month1 = int(new_date.strftime('%m'))
                year1 = int(new_date.strftime('%Y'))
                x += 1
                continue
            # if it isn't a weekend add it to temp_df
            else:
                if account != "":
                    app_data = client.count_unique('Page', 'user.pk',
                                                   timeframe=query,
                                                   timezone=5,
                                                   filters=[
                                                    {'operator': 'eq',
                                                     'property_name': 'app_key',
                                                     'property_value': account_app_keys[account]
                                                     }])
                else:
                    app_data = client.count_unique('Page', 'user.pk',
                                                   timeframe=query,
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

        # if user wants to include weekends, above process is skipped
        else:
            if account != "":
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=query,
                                               timezone=5,
                                               filters=[
                                                {'operator': 'eq',
                                                 'property_name': 'app_key',
                                                 'property_value': account_app_keys[account]
                                                 }])
            else:
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=query,
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
    if choice == 1:
        pull_type = 'MAU'
    elif choice == 2:
        pull_type = 'WAU'
    else:
        pull_type = 'YAU'
    temp_df.set_index('Date', inplace=True)
    temp_df.rename(columns={'value': pull_type}, inplace=True)
    temp_df.to_pickle(pull_type + '.pickle')
    print(temp_df)
