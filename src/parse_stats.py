import pandas as pd

pd.options.display.max_columns = 37
pd.set_option('display.width', None)

champ_ids = ['RU1', 'BE1', 'BRA1', 'ES1', 'FR1', 'GB1', 'IT1', 'L1', 'NL1', 'PO1']

for champ_id in champ_ids:
    html = open(f'txt_for_parsing/{champ_id}_24-25_shooting_stats.txt', errors='ignore').read()

    df = pd.read_html(html)
    df = df[0]
    print(df)

    #columns = list(df.iloc[0])
    #print(columns)
    df.columns = df.columns.droplevel(0)
    # print(df[df['Rk']=='Rk'])
    # pd.options.display.max_rows = 600
    print(df)
    for i in range(25, len(df), 25):
        if i < len(df):
            df = df.drop(i)
            df = df.reset_index(drop=True)

    df = df.set_index('Rk')
    df = df.drop(['Born', 'Matches'], axis=1)

    df['Nation'] = df['Nation'].str.replace(r'[^A-Z]', '', regex=True)
    df.to_csv(f'csv/stats/{champ_id}_shooting_24-25.csv', index=False)
    print(df)
