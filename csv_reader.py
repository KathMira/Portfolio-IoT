import pandas as pd
from sqlalchemy import create_engine

data = pd.read_csv('data.csv')
engine = create_engine('postgresql://postgres:6865@localhost:5432/postgres')

data.to_sql('temperaturas', engine, if_exists='append', index=False)

