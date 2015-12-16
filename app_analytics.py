import pandas as pd
from keen.client import KeenClient
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
from math import ceil
import plotly.plotly as py
import cufflinks as cl

# API Keys for EnhatchMarketingApp2.0
client = KeenClient(
    project_id=open("project_id.txt", 'r').read(),
    master_key=open("master_key.txt", 'r').read(),
    write_key=open("write_key.txt", 'r').read(),
    read_key=open("read_key.txt", 'r').read()
)


company_app_keys = {'enhatch': '118368274437335737698029276469999809095',
                    'rr Donnelly': '122169787206987846341383818731152558295',
                    'enhatch test': '129690986843314177890874392835790686791',
                    'ge transportation': '161299849888704839492897537232844536620',
                    'sonoma': '181479502579786137791904991511865109911',
                    'matt app': '187164587218548182461213257669257342645',
                    'paradigm spine': '224234185580937634736656715550056596303',
                    'allied building products': '253836980674808659119433391188831533066',
                    'ge ms&d': '285481600560299472311537967916336092115',
                    'medicrea': '28957996790114179931087019134108290920',
                    'seaspine': '293004830260428685669112292533809804613',
                    'centinel spine': '31544617854315997232220268879565974600',
                    'echo': '35431404049861511531147680883494651221',
                    'fh ortho': '71458724716185243148256933560969741161',
                    'wartsila': '95877466981632317159181119372243691526'}


# Function to acuire what the user wants to do
def user_wants():
    x = 1
    global decision1
    while x == 1:
        decision1 = input('What would you like to do today?\n'
                          '1) Find DAU\n'
                          '2) Find MAU\n'
                          '3) Find Both\n'
                          '4) Graph, or acquire information from previous pull\n')
        if decision1 == "1":  # if DAU is chosen, request the end date and then find DAU
            end_date_query()
            app_data_daily(month=end_month, day=end_day, year=end_year)
            x = 2

        elif decision1 == "2":  # if MAU is chosen, request the end date and then find MAU
            end_date_query()
            app_data_monthly(month=end_month, day=end_day, year=end_year)
            x = 2

        elif decision1 == "3":  # if both is chosen, request the end date and then find both
            end_date_query()
            app_data_daily(month=end_month, day=end_day, year=end_year)
            app_data_monthly(month=end_month, day=end_day, year=end_year)
            x = 2

        elif decision1 == "4":  # Use previous pull's data
            decision1 = input('\nWhat information did you use on the last pull?\n'
                              '1) DAU\n'
                              '2) MAU\n'
                              '3) Both\n')
            x = 2

        else:  # Error checking
            print("Wasn't a viable option, please pick again\n")
    python_graph()  # Creates the Python Graph
    data_end_use()  # Takes in a raw input of what the user wants to do with data acquried


# Function to acquire what the user wants to do with the new data acquired
def data_end_use():
    global decision1
    if decision1 == '1':
        print('Handling DAU\n'
              '____________________')
    elif decision1 == '2':
        print('Handling MAU\n'
              '____________________')
    else:
        print('Handling both DAU and MAU\n'
              '____________________________')
    x = 1
    while x == 1:  # error checking
        decision2 = input('What would you like to do with the information acquired?\n'
                          '1) Dump into a csv\n'
                          '2) Dump into a JSON\n'
                          '3) Create a Plotly graph\n'
                          '4) Nothing\n')
        if decision2 == '1':  # dumps into a csv
            # checks to see what information the user wanted
            if decision1 == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.to_csv('DAU.csv')
            elif decision1 == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.to_csv('MAU.csv')
            elif decision1 == '3':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                # creates the MAU/DAU column
                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.to_csv('MAU_DAU.csv')

            multiple_things = input('\nWould you like to do anything else with the data?\n'
                                    'Y = 1/N = 2:')
            if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                x = 1
            else:
                x = 2

        elif decision2 == '2':  # dumps into a JSON
            # checks to see what information the user wanted
            if decision1 == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.to_json('DAU.json')
            elif decision1 == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.to_json('MAU.json')
            elif decision1 == '3':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.to_json('MAU_DAU.json')
            multiple_things = input('\nWould you like to do anything else with the data?\n'
                                    'Y = 1/N = 2:')
            if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                x = 1
            else:
                x = 2

        elif decision2 == '3':  # creates a plotly graph
            graph_name = input('\nWhat would you like to name the graph?\n')
            graph_folder = input('\nWhat folder would you like to put the graph in?\n')
            # checks to see what information the user wanted
            if decision1 == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.iplot(kind='scatter', filename=graph_folder + graph_name)
            elif decision1 == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.iplot(kind='scatter', filename=graph_folder + graph_name)
            elif decision1 == '3':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name)
            multiple_things = input('\nWould you like to do anything else with the data?\n'
                                    'Y = 1/N = 2:')
            if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                x = 1
            else:
                x = 2

        elif decision2 == '4':
            break

        else:
            print("That wasn't a viable option, please try again")


# Functino to create the python graph after each pull of data
def python_graph():
    style.use('bmh')
    # checks to see what information the user wanted
    if decision1 == '1':
        dau_df = pd.read_pickle('DAU.pickle')
        dau_df['DAU'].plot()
        plt.legend(loc='best')
        plt.title('DAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif decision1 == '2':
        mau_df = pd.read_pickle('MAU.pickle')
        mau_df['MAU'].plot()
        plt.legend(loc='best')
        plt.title('MAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif decision1 == '3':
        mau_df = pd.read_pickle('MAU.pickle')
        dau_df = pd.read_pickle('DAU.pickle')
        mau_dau_df = dau_df.join(mau_df)

        division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
        df = pd.DataFrame(division)
        df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
        main_df = mau_dau_df.join(df)
        main_df.plot(secondary_y=['DAU/MAU %'])
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()


# Function to generate the end date the user specified
def end_date_query():
    x = 1
    while x == 1:
        print('Specify query end date\n-------------------------')
        global end_month
        global end_day
        global end_year
        try:
            end_date_raw = input("\nWhat date would you like the query to end?\n"
                                 "Please put it in format MM/DD/YYYY:\n")
            # breaks the date up into day month and year
            end_day = int(dt.datetime.strptime(end_date_raw, '%m/%d/%Y').strftime('%d'))
            end_month = int(dt.datetime.strptime(end_date_raw, '%m/%d/%Y').strftime('%m'))
            end_year = int(dt.datetime.strptime(end_date_raw, '%m/%d/%Y').strftime('%Y'))
            x = 2
        except ValueError:
            print("That was incorrect format, please try again\n")

    x = 1
    while x == 1:  # error checking
        question = input("\nWould you like to:\n"
                         "1)Go a set number of days back?\n"
                         "2)Pick a specific date in the past to start?\n"
                         "1 or 2?:")
        if question == '1':  # goes a set number of days back
            global query_size
            query_size = int(input("\nHow many days do you want in this query?")) + 1
            x = 2
        elif question == '2':  # finds a date in the past and then gets the query_size
            start_date_raw = input("\nWhat date would you like the query to start?\n"
                                   "Please put it in format MM/DD/YYYY:\n")
            try:
                start_day = int(dt.datetime.strptime(start_date_raw, '%m/%d/%Y').strftime('%d'))
                start_month = int(dt.datetime.strptime(start_date_raw, '%m/%d/%Y').strftime('%m'))
                start_year = int(dt.datetime.strptime(start_date_raw, '%m/%d/%Y').strftime('%Y'))
                d1 = dt.datetime(end_year, end_month, end_day)
                d2 = dt.datetime(start_year, start_month, start_day)
                query_size = abs((d1-d2).days + 1)
                x = 2
            except ValueError:
                print("that was incorrect format, please try again\n")
        else:
            print("That wasn't a viable option, please try again and pick 1 or 2")
    x = 1
    while x == 1:
        # option to exclude weekends
        question2 = input("\nWould you like to exclude weekends?\nY = 1/N = 2?:")
        global weekends
        if question2 == "Y" or question2 == "y" or question2 == "1":
            weekends = False
            x = 2
        elif question2 == "N" or question2 == "n" or question2 == "2":
            weekends = True
            x = 2
        else:
            print("Not a viable option, please try again")
    x = 1
    while x == 1:
        # option to filter by company
        question2 = input("\nWould you like to filter by company?\nY = 1/N = 2?:")
        global company_filter
        global requested_company
        if question2 == "Y" or question2 == "y" or question2 == "1":
            requested_company = (input('\nWhat company would you like?').lower())
            if requested_company in company_app_keys:
                company_filter = True
                x = 2
            else:
                add_company = input("\nThat company isn't valid check the spelling.\n"
                                    "If the spelling is correct, would you like to add it?\n"
                                    "If it isn't select option 2 and restart\n"
                                    "Y = 1/ N = 2?:")
                if add_company == 'Y' or add_company == 'y' or add_company == '1':
                    company_name = input('What is the name of the company?')
                    company_key = input('What is the app key for the company?')
                    company_app_keys[company_name] = company_key
                    requested_company = company_name
                    company_filter = True
                    x = 2
                if add_company == 'N' or add_company == 'n' or add_company == '2':
                    x = 1
        elif question2 == "N" or question2 == "n" or question2 == "2":
            company_filter = False
            x = 2
        else:
            print("Not a viable option, please try again")


# Function to generate the DAU query
def daily_query_start(day, month, year):
    start_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(dt.datetime(year, month, (day+1)).date()), 'start': str(start_day.date())}
    return query


# Function to generate the MAU query
def monthly_query_start(day, month, year):
    monthly_start_day = dt.datetime(year, month, day) - dt.timedelta(query_size + 30)
    monthly_end_day = dt.datetime(year, month, day) - dt.timedelta(query_size - 1)
    query = {'end': str(monthly_end_day), 'start': str(monthly_start_day)}
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


# Function to generate the monthly date from the Keen.io ISO date format
def extract_date_monthly(raw_data):
    x = 0
    while x < len(raw_data):

        get_first_column = raw_data[x]
        get_first_time = get_first_column['timeframe']
        get_first_column['Date'] = get_first_column.pop('timeframe')
        get_first_column['Date'] = dt.datetime.strptime(get_first_time['end'],
                                                        '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%m-%d-%Y')
        x += 1


# Function that actually pulls the daily data from Keen
def app_data_daily(month, day, year):
    # process that breaks up the daily query into a bunch of little queries that excludes weekends
    if not weekends:
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

        temp_df = pd.DataFrame()
        for item in query:
            global company_filter
            global requested_company
            if company_filter:
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=item,
                                               timezone=5,
                                               interval='daily',
                                               filters=[
                                                   {'operator': 'eq',
                                                    'property_name': 'app_key',
                                                    'property_value': company_app_keys[requested_company]
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
        if company_filter:
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=daily_query_start(day, month, year),
                                           timezone=5,
                                           interval='daily',
                                           filters=[
                                               {'operator': 'eq',
                                                'property_name': 'app_key',
                                                'property_value': company_app_keys[requested_company]
                                                }])
        else:
            app_data = client.count_unique('Page', 'user.pk',
                                           timeframe=daily_query_start(day, month, year),
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


# Function that actually pulls the monthly data from Keen
def app_data_monthly(month, day, year):
    # this query might be able to be modified
    # it takes the first day specified in the query, subtracts thirty and puts the monthly data for that date.
    # then goes on to the next day and does the same thing for a rolling thirty feel.
    x = 0
    day1 = day
    month1 = month
    year1 = year
    temp_df = pd.DataFrame  # empty dataframe to fill
    while x < query_size:
        # process to exclude weekends
        if not weekends:
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
                global company_filter
                global requested_company
                if company_filter:
                    app_data = client.count_unique('Page', 'user.pk',
                                                   timeframe=monthly_query_start(day1, month1, year1),
                                                   timezone=5,
                                                   filters=[
                                                    {'operator': 'eq',
                                                     'property_name': 'app_key',
                                                     'property_value': company_app_keys[requested_company]
                                                     }])
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

        # if use wants to include weekends, above process is skipped
        else:
            if company_filter:
                app_data = client.count_unique('Page', 'user.pk',
                                               timeframe=monthly_query_start(day1, month1, year1),
                                               timezone=5,
                                               filters=[
                                                {'operator': 'eq',
                                                 'property_name': 'app_key',
                                                 'property_value': company_app_keys[requested_company]
                                                 }])
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
    print(temp_df.head())

user_wants()
