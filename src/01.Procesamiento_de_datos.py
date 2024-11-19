# Libraries  
import numpy as np, pandas as pd
from scipy import stats as st 
from matplotlib import pyplot as plt

df_games = pd.read_csv('games.csv',sep=',')

# Change column names to lowercase and strip
df_games.columns = [col.lower().strip() for col in df_games.columns]

# Convert datatypes 
df_games.loc[df_games['user_score'] == 'tbd', 'user_score'] = np.nan
df_games['user_score'] = df_games['user_score'].astype(float)*10
df_games['year_of_release'] = df_games['year_of_release'].astype('Int64')

# Add total sales column 
df_games['total_sales'] = df_games[['na_sales','eu_sales','jp_sales','other_sales']].sum(axis=1)
df_games.fillna({'critic_score':df_games['critic_score'].median()},inplace=True)
df_games.fillna({'user_score':df_games['user_score'].median()}, inplace=True)

# standardize videogame name and remove duplicates 
df_games['name'] = df_games['name'].str.upper().str.strip().str.replace('.','').str.replace(',','').str.replace(':','').str.replace(';','')

df_games.dropna(subset='year_of_release',inplace=True)
df_games.loc[df_games['name'].isna(), 'name'] = 'NOT DEFINED'

df_games.drop_duplicates(subset=['name','platform']).reset_index(drop=True,inplace=True)

df_games.fillna({'genre':'Not Defined'},inplace=True)

#Group platforms by brand
def platform_group(x):
    if x in ['3DS','DS','GB','GBA','GC','N64','NES','SNES','Wii','WiiU']:
        return 'Nintendo'
    elif x in ['PC', 'PCFX']:
        return 'PC'
    elif x in ['X360','XB','XOne']:
        return 'Xbox' 
    elif x in ['PS3','PS2','PS4','PS','PSP','PSV',]:
        return 'Playstation'
    else: 
        return 'Other'
    
df_games['platform_group'] = df_games['platform'].apply(platform_group)

# Clean data 
df_games.to_csv('games_clean.csv',index=False)
