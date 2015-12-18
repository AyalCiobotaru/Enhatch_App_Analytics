import datetime as dt
from client_and_app_keys import client, account_app_keys


def app_opened(account):
    app_data = client.count_unique('Page', 'user.pk',
                                   timeframe={'start': '2014-10-01T00:00:00.000+00:00',
                                              'end': str(dt.datetime.now())},
                                   timezone=5,
                                   filters=[
                                       {'operator': 'eq',
                                        'property_name': 'app_key',
                                        'property_value': account_app_keys[account]
                                        }])
    print('Total Unique Users to date for %s: %s' % (account, app_data))
