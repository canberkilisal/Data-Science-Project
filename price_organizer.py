from datetime import datetime, timedelta
import pandas as pd
import os
import numpy as np

MAIN_DIRECTORY = 'petrol_prices_nonorganized'
OUT_DIRECTORY = 'petrol_prices'

for directory in os.listdir(MAIN_DIRECTORY):
    # Create temp dataframe
    temp_df_columns = ['DATE', 'GASOLINE_PRICE', 'DIESEL_PRICE']
    temp_df = pd.DataFrame(columns=temp_df_columns)

    start_date = datetime.strptime("01.01.2020", "%d.%m.%Y")
    end_date = datetime.strptime("01.01.2023", "%d.%m.%Y")

    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime("%Y-%m-%d")
        temp_df.loc[len(temp_df)] = [formatted_date, np.nan, np.nan]
        current_date += timedelta(days=1)

    for filename in os.listdir(os.path.join(MAIN_DIRECTORY, directory)):
        file_path = os.path.join(MAIN_DIRECTORY, directory, filename)
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            real_index = (datetime.strptime(df.loc[index, 'Tarih'], "%d.%m.%Y") - start_date).days
            if df.loc[index, 'Yakıt Tipi'] == 'Motorin':
                temp_df.loc[real_index, 'DIESEL_PRICE'] = df.loc[index, 'Fiyat']
            else:
                temp_df.loc[real_index, 'GASOLINE_PRICE'] = df.loc[index, 'Fiyat']

    temp_df['DIESEL_PRICE'].fillna(method='bfill', inplace=True, limit=1)
    temp_df['DIESEL_PRICE'].fillna(method='ffill', inplace=True)
    temp_df['GASOLINE_PRICE'].fillna(method='bfill', inplace=True, limit=1)
    temp_df['GASOLINE_PRICE'].fillna(method='ffill', inplace=True)

    output_file = OUT_DIRECTORY + '\\' + directory + '.csv'
    temp_df.to_csv(output_file, index=False)