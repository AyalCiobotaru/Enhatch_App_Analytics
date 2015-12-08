import pandas as pd
import pandas_datareader.io as web
import keen
from keen.client import KeenClient

client = KeenClient(
    project_id=open("project_id.txt", 'r').read(),
    master_key=open("master_key.txt", 'r').read(),
    write_key=open("write_key.txt", 'r').read(),
    read_key=open("read_key.txt", 'r').read()
)

temp_df = pd.DataFrame()
app_data = client.count_unique('Page', 'user.pk',
                               timeframe='last_7_days',
                               timezone=5,
                               interval='daily')

print(temp_df)
