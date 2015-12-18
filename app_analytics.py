import datetime as dt
from client_and_app_keys import account_app_keys
from daily_pull import app_data_daily
from weekly_monthly_yearly import app_data_weekly_monthly_yearly
from end_use import data_end_use, python_graph
from total_app_opened import app_opened


# Function to acuire what the user wants to do
def user_wants():
    y = 1
    x = 1
    companies = False
    decision1 = ""
    while y == 1:
        # option to pull multiple companies
        company_pull = input("Which you like to pull for multiple accounts consecutively?\nY = 1/ N = 2?")
        if company_pull == "Y" or company_pull == "y" or company_pull == "1":
            companies = True
            x = 2
            y = 2
        elif company_pull == "N" or company_pull == "n" or company_pull == "2":
            x = 1
            y = 2
        else:
            print("Not a viable option, please try again")
    decision1_list = ["1", "2", "3", "4", "5", "6", "7"]
    while x == 1:
        decision1 = input('What would you like to do today?\n'
                          '1) Find DAU\n'
                          '2) Find MAU\n'
                          '3) Find WAU\n'
                          '4) Find YAU\n'
                          '5) Find DAU/MAU\n'
                          '6) Find WAU/YAU\n'
                          '7) Graph, or acquire information from previous pull\n')
        if decision1 not in decision1_list:
            print("That wasn't a viable option, please try again")
        else:
            x = 2

    end_date_query(pull_type=decision1, companies=companies)


# Function to generate the end date the user specified
def end_date_query(pull_type, companies):
    end_day = ""
    end_month = ""
    end_year = ""
    x = 1
    while x == 1:
        print('Specify query end date\n-------------------------')
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
    query_size = 0
    x = 1
    while x == 1:  # error checking
        question = input("\nWould you like to:\n"
                         "1)Go a set number of days back?\n"
                         "2)Pick a specific date in the past to start?\n"
                         "1 or 2?:")
        if question == '1':  # goes a set number of days back
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
    weekends = False
    x = 1
    while x == 1:
        # option to exclude weekends
        question2 = input("\nWould you like to exclude weekends?\nY = 1/N = 2?:")
        if question2 == "Y" or question2 == "y" or question2 == "1":
            weekends = False
            x = 2
        elif question2 == "N" or question2 == "n" or question2 == "2":
            weekends = True
            x = 2
        else:
            print("Not a viable option, please try again")
    if companies:
        multiple_companies(query_end_day=end_day, query_end_month=end_month, query_end_year=end_year,
                           weekend=weekends, query_size=query_size)
        return

    x = 1
    requested_account = ""
    account_invites = 0
    while x == 1:
        # option to filter by company
        question2 = input("\nWould you like to filter by one account?\nY = 1/N = 2?:")
        if question2 == "Y" or question2 == "y" or question2 == "1":
            requested_account = (input('\nWhat company would you like?').lower())
            if requested_account in account_app_keys:
                account_invites = input("Enter %s's total invites: " % requested_account)
                x = 2
            else:
                add_account = input("\nThat account isn't valid check the spelling.\n"
                                    "If the spelling is correct, would you like to add it?\n"
                                    "If it isn't select option 2 and restart\n"
                                    "Y = 1/ N = 2?:")
                if add_account == 'Y' or add_account == 'y' or add_account == '1':
                    account_name = input('What is the name of the account?')
                    account_key = input('What is the app key for the account?')
                    account_app_keys[account_name] = account_key
                    requested_account = account_name
                    x = 2
                if add_account == 'N' or add_account == 'n' or add_account == '2':
                    x = 1
        elif question2 == "N" or question2 == "n" or question2 == "2":
            x = 2
        else:
            print("Not a viable option, please try again")
    what_to_pull(account=requested_account, account_size=account_invites,
                 query_end_day=end_day, query_end_month=end_month, query_end_year=end_year,
                 weekend=weekends, pull_type=pull_type, query_size=query_size)


# Funtion to pull mutliple companies at the same time
def multiple_companies(query_end_day, query_end_month, query_end_year, weekend, query_size):
    account_amount = 0
    x = 1
    while x == 1:
        try:
            account_amount = int(input("\nHow many accounts would you like to pull?"))
            x = 2
        except ValueError:
            print("That wasn't a number, please enter a number\n")
    print()
    amount = 0
    account_list = []
    account_invites_list = []
    account_invites = 0
    while amount < account_amount:
        amount += 1
        account = input('Enter account %s: ' % amount)
        if account in account_app_keys:
            account_invites = input('Enter account %s total invites: ' % amount)
            account_list.append(account)
            account_invites_list.append(account_invites)
        else:
            print("That wasn't a viable account, please try again or add to the account dictionary\n")
            amount -= 1
    decision1 = input('\nWhat information did you want to pull?\n'
                      '1) DAU\n'
                      '2) MAU\n'
                      '3) WAU\n'
                      '4) YAU\n'
                      '5) Both DAU & MAU\n'
                      '6) Both WAU & YAU\n')

    decision2 = input('What would you like to do with the information acquired?\n'
                      '1) Dump into a csv\n'
                      '2) Dump into a JSON\n'
                      '3) Create a Plotly graph\n'
                      '4) Nothing\n')

    for account in account_list:
        x = 1
        while x == 1:
            if decision1 == "1":  # if DAU is chosen, request the end date and then find DAU
                app_data_daily(month=query_end_month, day=query_end_day, year=query_end_year, weekend=weekend,
                               account=account, query_size=query_size)
                data_end_use(pull_type=decision1, data_use=decision2, account=account)
                app_opened(account)
                print("Total Invites sent to date: %s" % account_invites)
                x = 2

            elif decision1 == "2":  # if MAU is chosen, request the end date and then find MAU
                app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                               choice=1, weekend=weekend, account=account, query_size=query_size)
                data_end_use(pull_type=decision1, data_use=decision2, account=account)
                app_opened(account)
                print("Total Invites sent to date: %s" % account_invites)
                x = 2

            elif decision1 == "3":  # if WAU is chosen, request the end date and then find MAU
                app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                               choice=2, weekend=weekend, account=account, query_size=query_size)
                data_end_use(pull_type=decision1, data_use=decision2, account=account)
                app_opened(account)
                print("Total Invites sent to date: %s" % account_invites)
                x = 2

            elif decision1 == "4":  # if YAU is chosen, request the end date and then find MAU
                app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                               choice=3, weekend=weekend, account=account, query_size=query_size)
                data_end_use(pull_type=decision1, data_use=decision2, account=account)
                app_opened(account)
                print("Total Invites sent to date: %s" % account_invites)
                x = 2

            elif decision1 == "5":  # if DAU/MAU is chosen, request the end date and then find both
                app_data_daily(month=query_end_month, day=query_end_day, year=query_end_year, weekend=weekend,
                               account=account, query_size=query_size)
                app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                               choice=1, weekend=weekend, account=account, query_size=query_size)
                data_end_use(pull_type=decision1, data_use=decision2, account=account)
                app_opened(account)
                print("Total Invites sent to date: %s" % account_invites)
                x = 2

            elif decision1 == "6":  # if WAU/YAU is chosen, request the end date and then find both
                app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                               choice=2, weekend=weekend, account=account, query_size=query_size)
                app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                               choice=3, weekend=weekend, account=account, query_size=query_size)
                data_end_use(pull_type=decision1, data_use=decision2, account=account)
                app_opened(account)
                print("Total Invites sent to date: %s" % account_invites)
                x = 2
            else:  # Error checking
                print("Wasn't a viable option, please pick again\n")


# Function to run the pulls
def what_to_pull(account, account_size, query_end_day, query_end_month, query_end_year, weekend, pull_type, query_size):
    x = 1
    while x == 1:
        if pull_type == "1":  # if DAU is chosen, request the end date and then find DAU
            app_data_daily(month=query_end_month, day=query_end_day, year=query_end_year, weekend=weekend,
                           account=account, query_size=query_size)
            app_opened(account)
            print("Total Invites sent to date: %s" % account_size)
            x = 2

        elif pull_type == "2":  # if MAU is chosen, request the end date and then find MAU
            app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                           choice=1, weekend=weekend, account=account, query_size=query_size)
            app_opened(account)
            print("Total Invites sent to date: %s" % account_size)
            x = 2

        elif pull_type == "3":  # if WAU is chosen, request the end date and then find MAU
            app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                           choice=2, weekend=weekend, account=account, query_size=query_size)
            app_opened(account)
            print("Total Invites sent to date: %s" % account_size)
            x = 2

        elif pull_type == "4":  # if YAU is chosen, request the end date and then find MAU
            app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                           choice=3, weekend=weekend, account=account, query_size=query_size)
            app_opened(account)
            print("Total Invites sent to date: %s" % account_size)
            x = 2

        elif pull_type == "5":  # if DAU/MAU is chosen, request the end date and then find both
            app_data_daily(month=query_end_month, day=query_end_day, year=query_end_year, weekend=weekend,
                           account=account, query_size=query_size)
            app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                           choice=1, weekend=weekend, account=account, query_size=query_size)
            app_opened(account)
            print("Total Invites sent to date: %s" % account_size)
            x = 2

        elif pull_type == "6":  # if WAU/YAU is chosen, request the end date and then find both
            app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                           choice=2, weekend=weekend, account=account, query_size=query_size)
            app_data_weekly_monthly_yearly(month=query_end_month, day=query_end_day, year=query_end_year,
                                           choice=3, weekend=weekend, account=account, query_size=query_size)
            app_opened(account)
            print("Total Invites sent to date: %s" % account_size)
            x = 2

        elif pull_type == "7":  # Use previous pull's data
            pull_type = input('\nWhat information did you use on the last pull?\n'
                              '1) DAU\n'
                              '2) MAU\n'
                              '3) WAU\n'
                              '4) YAU\n'
                              '5) Both DAU & MAU\n'
                              '6) Both WAU & YAU\n')
            x = 2
        else:  # Error checking
            print("Wasn't a viable option, please pick again\n")

        python_graph(pull_type=pull_type)  # Creates the Python Graph
        data_end_use(pull_type=pull_type, data_use=None, account=None)

user_wants()
