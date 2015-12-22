import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import sys
import os
import plotly.plotly as py
import cufflinks as cl


# Functino to create the python graph after each pull of data
def python_graph(pull_type):
    style.use('bmh')
    # checks to see what information the user wanted
    if pull_type == '1':
        dau_df = pd.read_pickle('DAU.pickle')
        dau_df['DAU'].plot()
        plt.legend(loc='best')
        plt.title('DAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif pull_type == '2':
        mau_df = pd.read_pickle('MAU.pickle')
        mau_df['MAU'].plot()
        plt.legend(loc='best')
        plt.title('MAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif pull_type == '3':
        wau_df = pd.read_pickle('WAU.pickle')
        wau_df['WAU'].plot()
        plt.legend(loc='best')
        plt.title('WAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif pull_type == '4':
        yau_df = pd.read_pickle('YAU.pickle')
        yau_df['YAU'].plot()
        plt.legend(loc='best')
        plt.title('YAU')
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()
    elif pull_type == '5':
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
    elif pull_type == '6':
        wau_df = pd.read_pickle('WAU.pickle')
        yau_df = pd.read_pickle('YAU.pickle')
        wau_yau_df = wau_df.join(yau_df)

        division = ((wau_yau_df['WAU'] / wau_yau_df['YAU']) * 100)
        df = pd.DataFrame(division)
        df.rename(columns={0: 'WAU/YAU %'}, inplace=True)
        main_df = wau_yau_df.join(df)
        main_df.plot(secondary_y=['WAU/YAU %'])
        fig = plt.gcf()
        fig.set_size_inches(15, 10, forward=True)
        plt.show()


# Function to acquire what the user wants to do with the new data acquired
def data_end_use(pull_type, data_use, account):
    if data_use is None:
        if pull_type == '1':
            print('Handling DAU\n'
                  '____________________')
        elif pull_type == '2':
            print('Handling MAU\n'
                  '____________________')
        elif pull_type == '3':
            print('Handling WAU\n'
                  '____________________________')
        elif pull_type == '4':
            print('Handling YAU\n'
                  '____________________')
        elif pull_type == '5':
            print('Handling DAU/MAU\n'
                  '____________________')
        elif pull_type == '6':
            print('Handling WAU/YAU\n'
                  '____________________________')
        elif pull_type == '7':
            print('Handling Cohort Data\n'
                  '____________________________')
    x = 1
    while x == 1:  # error checking
        if data_use is None:
            decision2 = input('What would you like to do with the information acquired?\n'
                              '1) Dump into a csv\n'
                              '2) Dump into a JSON\n'
                              '3) Create a Plotly graph\n'
                              '4) Nothing\n')
        else:
            decision2 = data_use
        if decision2 == '1':  # dumps into a csv
            # checks to see what information the user wanted
            if pull_type == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                new_path = sys.path[0] + os.sep + 'DAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    dau_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                   'If the file name already exists it will overwrite the old file. ') +
                                  '.csv')
                else:
                    dau_df.to_csv(new_path + account + '_' + 'DAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.csv')

            elif pull_type == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                new_path = sys.path[0] + os.sep + 'MAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    mau_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                   'If the file name already exists it will overwrite the old file. ') +
                                  '.csv')
                else:
                    mau_df.to_csv(new_path + account + '_' + 'MAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.csv')
            elif pull_type == '3':
                wau_df = pd.read_pickle('WAU.pickle')
                new_path = sys.path[0] + os.sep + 'WAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    wau_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                   'If the file name already exists it will overwrite the old file. ') +
                                  '.csv')
                else:
                    wau_df.to_csv(new_path + account + '_' + 'WAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.csv')
            elif pull_type == '4':
                yau_df = pd.read_pickle('YAU.pickle')
                new_path = sys.path[0] + os.sep + 'YAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    yau_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                   'If the file name already exists it will overwrite the old file. ') +
                                  '.csv')
                else:
                    yau_df.to_csv(new_path + account + '_' + 'YAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.csv')
            elif pull_type == '5':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                # creates the MAU/DAU column
                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                new_path = sys.path[0] + os.sep + 'MAU_DAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    main_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                    'If the file name already exists it will overwrite the '
                                                    'old file. ') +
                                   '.csv')
                else:
                    main_df.to_csv(new_path + account + '_' + 'DAU_MAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                   '.csv')
            elif pull_type == '6':
                wau_df = pd.read_pickle('WAU.pickle')
                yau_df = pd.read_pickle('YAU.pickle')
                wau_yau_df = wau_df.join(yau_df)

                division = ((wau_yau_df['WAU'] / wau_yau_df['YAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'WAU/YAU %'}, inplace=True)
                main_df = wau_yau_df.join(df)
                new_path = sys.path[0] + os.sep + 'WAU_YAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    main_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                    'If the file name already exists it will overwrite the '
                                                    'old file. ') +
                                   '.csv')
                else:
                    main_df.to_csv(new_path + account + '_' + 'WAU/YAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                   '.csv')
            elif pull_type == '7':
                cohort_df = pd.read_pickle('user_retention.pickle')
                new_path = sys.path[0] + os.sep + 'Cohort' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    cohort_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                      'If the file name already exists it will overwrite the old file.'
                                                      ' ') + '.csv')
                else:
                    cohort_df.to_csv(new_path + account + '_' + 'cohort' + '_' + dt.datetime.now()
                                     .strftime('%m-%d-%Y') + '.csv')
            if data_use is None:
                multiple_things = input('\nWould you like to do anything else with the data?\n'
                                        'Y = 1/N = 2:')
                if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                    x = 1
                else:
                    x = 2
            else:
                x = 2

        elif decision2 == '2':  # dumps into a JSON
            # checks to see what information the user wanted
            if pull_type == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                new_path = sys.path[0] + os.sep + 'DAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    dau_df.to_json(new_path + input('What would you like to call this file?\n'
                                                    'If the file name already exists it will overwrite '
                                                    'the old file. ') +
                                   '.json')
                else:
                    dau_df.to_csv(new_path + account + '_' + 'DAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.json')

            elif pull_type == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                new_path = sys.path[0] + os.sep + 'MAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    mau_df.to_json(new_path + input('What would you like to call this file?\n'
                                                    'If the file name already exists it will overwrite the '
                                                    'old file. ') +
                                   '.json')
                else:
                    mau_df.to_csv(new_path + account + '_' + 'MAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.json')
            elif pull_type == '3':
                wau_df = pd.read_pickle('WAU.pickle')
                new_path = sys.path[0] + os.sep + 'WAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    wau_df.to_json(new_path + input('What would you like to call this file?\n'
                                                    'If the file name already exists it will overwrite the '
                                                    'old file. ') +
                                   '.json')
                else:
                    wau_df.to_csv(new_path + account + '_' + 'WAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.json')
            elif pull_type == '4':
                yau_df = pd.read_pickle('YAU.pickle')
                new_path = sys.path[0] + os.sep + 'YAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    yau_df.to_json(new_path + input('What would you like to call this file?\n'
                                                    'If the file name already exists it will overwrite the '
                                                    'old file. ') +
                                   '.json')
                else:
                    yau_df.to_csv(new_path + account + '_' + 'YAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                  '.json')
            elif pull_type == '5':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                # creates the MAU/DAU column
                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                new_path = sys.path[0] + os.sep + 'DAU_MAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    main_df.to_json(new_path + input('What would you like to call this file?\n'
                                                     'If the file name already exists it will overwrite the '
                                                     'old file. ') +
                                    '.json')
                else:
                    main_df.to_csv(new_path + account + '_' + 'MAU/DAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                   '.json')
            elif pull_type == '6':
                wau_df = pd.read_pickle('WAU.pickle')
                yau_df = pd.read_pickle('YAU.pickle')
                wau_yau_df = wau_df.join(yau_df)

                division = ((wau_yau_df['WAU'] / wau_yau_df['YAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'WAU/YAU %'}, inplace=True)
                main_df = wau_yau_df.join(df)
                new_path = sys.path[0] + os.sep + 'WAU_YAU' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    main_df.to_json(new_path + input('What would you like to call this file?\n'
                                                     'If the file name already exists it will overwrite the '
                                                     'old file. ') +
                                    '.json')
                else:
                    main_df.to_csv(new_path + account + '_' + 'WAU/YAU' + '_' + dt.datetime.now().strftime('%m-%d-%Y') +
                                   '.json')
            elif pull_type == '7':
                cohort_df = pd.read_pickle('user_retention.pickle')
                new_path = sys.path[0] + os.sep + 'Cohort' + os.sep
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                if data_use is None:
                    cohort_df.to_csv(new_path + input('What would you like to call this file?\n'
                                                      'If the file name already exists it will overwrite the old file.'
                                                      ' ') + '.json')
                else:
                    cohort_df.to_csv(new_path + account + '_' + 'cohort' + '_' + dt.datetime.now()
                                     .strftime('%m-%d-%Y') + '.json')
            if data_use is None:
                multiple_things = input('\nWould you like to do anything else with the data?\n'
                                        'Y = 1/N = 2:')
                if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                    x = 1
                else:
                    x = 2
            else:
                x = 2

        elif decision2 == '3':  # creates a plotly graph
            if data_use is None:
                graph_name = input('\nWhat would you like to name the graph?'
                                   '\nYou dont need to include the pull, it will do that automatically\n')
                graph_folder = input('\nWhat folder would you like to put the graph in?\n')
            else:
                graph_folder = dt.datetime.now().strftime('%m-%d-%Y')
                graph_name = account
            # checks to see what information the user wanted
            if pull_type == '1':
                dau_df = pd.read_pickle('DAU.pickle')
                dau_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name + ' DAU')
            elif pull_type == '2':
                mau_df = pd.read_pickle('MAU.pickle')
                mau_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name + ' MAU')
            elif pull_type == '3':
                wau_df = pd.read_pickle('WAU.pickle')
                wau_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name + ' WAU')
            elif pull_type == '4':
                yau_df = pd.read_pickle('YAU.pickle')
                yau_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name + ' YAU')
            elif pull_type == '5':
                mau_df = pd.read_pickle('MAU.pickle')
                dau_df = pd.read_pickle('DAU.pickle')
                mau_dau_df = dau_df.join(mau_df)

                division = ((mau_dau_df['DAU'] / mau_dau_df['MAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'DAU/MAU %'}, inplace=True)
                main_df = mau_dau_df.join(df)
                main_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name + ' DAU_MAU')
            elif pull_type == '6':
                wau_df = pd.read_pickle('WAU.pickle')
                yau_df = pd.read_pickle('YAU.pickle')
                wau_yau_df = wau_df.join(yau_df)

                division = ((wau_yau_df['WAU'] / wau_yau_df['YAU']) * 100)
                df = pd.DataFrame(division)
                df.rename(columns={0: 'WAU/YAU %'}, inplace=True)
                main_df = wau_yau_df.join(df)
                main_df.iplot(kind='scatter', filename=graph_folder + '/' + graph_name + ' WAU_YAU')

            if data_use is None:
                multiple_things = input('\nWould you like to do anything else with the data?\n'
                                        'Y = 1/N = 2:')
                if multiple_things == '1' or multiple_things == 'Y' or multiple_things == 'y':
                    x = 1
                else:
                    x = 2
            else:
                x = 2

        elif decision2 == '4':
            break

        else:
            print("That wasn't a viable option, please try again")
