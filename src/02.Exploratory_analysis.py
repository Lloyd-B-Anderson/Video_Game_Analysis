# Libraries  
import numpy as np, pandas as pd
from scipy import stats as st 
from matplotlib import pyplot as plt

# Read clean data
df_games = pd.read_csv('games_clean.csv',sep=',')

# Graph of games released per year since 1980
games_released_per_year = df_games.groupby('year_of_release')['name'].count()
plt.figure(figsize=(12, 6))
games_released_per_year.plot(kind='bar', color='skyblue')
plt.xlabel('Year of Release')
plt.ylabel('Number of Games Released')
plt.title('Number of Games Released Each Year')
plt.show()

# Top 10 Platform Sales and yearly sales distribution since 1980
top_sales_group = df_games.groupby('platform')['total_sales'].sum().sort_values(ascending=False)

top_sales_group.head(10).plot(kind='bar', color='skyblue')
plt.xlabel('Platform')
plt.ylabel('Total Sales (millions USD)')
plt.title('Top 10 Platforms by Total Sales')
plt.show()

top_platform_names = top_sales_group.head(10).index
top_platform_data = df_games[df_games['platform'].isin(top_platform_names)]
platform_year_sales = top_platform_data.groupby(['year_of_release', 'platform'])['total_sales'].sum().unstack(fill_value=0)

platform_year_sales.plot(kind='line')
plt.xlabel('Year of Release')
plt.ylabel('Total Sales (millions USD)')
plt.title('Yearly Sales Distribution for Top Platforms')
plt.legend(title='Platform')
plt.show()

# Shorten data from 2013 onwards 
df_games_2013 = df_games[(df_games['year_of_release'] >= 2013) ] 
df_games_2013.to_csv('games_clean_2013.csv',index=False)

top_sales_group_2013 = df_games_2013.groupby('platform')['total_sales'].sum().sort_values(ascending=False)
top_platforms_2013 = df_games_2013.groupby(['year_of_release','platform'])['total_sales'].sum().unstack(fill_value=0)

top_sales_group_2013.head(10).plot(kind='bar', color='skyblue')
plt.xlabel('Platform')
plt.ylabel('Total Sales (millions USD)')
plt.title('Top 10 Platforms by Total Sales Since 2013 ')
plt.show()

top_platforms_2013.plot()
plt.xlabel('Year of Release')
plt.ylabel('Total Sales (millions USD)')
plt.title('Yearly Sales Distribution for Top Platforms since 2013')
plt.legend(title='Platform')
plt.show()

# Boxplot for the 3 platforms with most sales since 2013
top_3_juego_plataforma = df_games_2013[df_games_2013['platform'].isin(['3DS','XOne','PS4'])]

top_3_ventas = top_3_juego_plataforma.groupby(['year_of_release','platform'])['total_sales'].sum().unstack(fill_value=0)

top_3_ventas.boxplot()
plt.title('Distribucion de de el total de ventas para las 3 plataformas con mayor ventas')
plt.ylabel('USD (millones)')
plt.xlabel('Plataforma')
plt.show()

# Scatter plot for user and critic scores vs total sales (PS4)
PS4_2013 = df_games_2013[df_games_2013['platform'] == 'PS4']

plt.figure(figsize = (8,5))
plt.subplot(1,2,1)
plt.scatter(PS4_2013['user_score'], PS4_2013['total_sales'])
plt.xlabel('User Score')
plt.ylabel('Total Sales (millions)')
plt.title('User Score vs. Total Sales (PS4)')

plt.subplot(1,2,2)
plt.scatter(PS4_2013['critic_score'], PS4_2013['total_sales'])
plt.xlabel('Critic Score')
plt.ylabel('Total Sales (millions)')
plt.title('Critic Score vs. Total Sales (PS4)')
plt.show()

cor = PS4_2013[['user_score','critic_score','total_sales']].dropna().corr()
print(cor)

# Scatter plot for user and critic scores vs total sales (~PS4)
same_games_wo_ps4 = df_games_2013[df_games_2013['name'].isin(PS4_2013['name']) & (df_games_2013['platform'] != 'PS4')]

print(same_games_wo_ps4['platform'].unique())

plt.figure(figsize = (11,5))
plt.subplot(1,2,1)
plt.scatter(same_games_wo_ps4['user_score'], same_games_wo_ps4['total_sales'])
plt.xlabel('User Score')
plt.ylabel('Total Sales (millions)')
plt.title('User Score vs. Total Sales (All consoles except PS4)')

plt.subplot(1,2,2)
plt.scatter(same_games_wo_ps4['critic_score'], same_games_wo_ps4['total_sales'])
plt.xlabel('Critic Score')
plt.ylabel('Total Sales (millions)')
plt.title('Critic Score vs. Total Sales (All consoles except PS4)')
plt.show()

cor = same_games_wo_ps4[['user_score','critic_score','total_sales']].dropna().corr()
print(cor)

# Total sales by genre 
genre_sales = df_games.groupby('genre').agg(total_sales=('total_sales','sum'),game_count=('total_sales','count')).reset_index()
genre_sales.sort_values(by='total_sales', ascending=False, inplace=True)

plt.barh(genre_sales['genre'],genre_sales['total_sales'], color='purple')
plt.title('Total Sales by Genre')
plt.xlabel('Total Sales (millions USD)')
plt.ylabel('Genres')
plt.gca().invert_yaxis()
plt.show()

# Platform sales by region (NA, EU, JP)

individual_sales = df_games_2013.groupby('platform')[['na_sales','eu_sales','jp_sales']].sum().reset_index()

na_reg = individual_sales[['platform','na_sales']].sort_values(by='na_sales').tail(5)
eu_reg = individual_sales[['platform','eu_sales']].sort_values(by='eu_sales').tail(5)
jp_reg = individual_sales[['platform','jp_sales']].sort_values(by='jp_sales').tail(5)

plt.figure(figsize=(12,6))
plt.subplot(1,3,1)
plt.suptitle('Top 5 Videogame sales per Console by Region')
plt.barh(na_reg['platform'], na_reg['na_sales'],color='pink')
plt.title('North America')
plt.xlabel('Total Sales (USD)')

plt.subplot(1,3,2)
plt.barh(eu_reg['platform'],eu_reg['eu_sales'],color='yellow')
plt.title('Europe')
plt.xlabel('Total Sales (USD)')

plt.subplot(1,3,3)
plt.barh(jp_reg['platform'],jp_reg['jp_sales'],color='orange')
plt.title('Japan')
plt.xlabel('Total Sales (USD)')
plt.show()

# Genre sales by region (NA, EU, JP)
individual_sales_genre = df_games_2013.groupby('genre')[['na_sales','eu_sales','jp_sales']].sum().reset_index()

na_reg_genre = individual_sales_genre[['genre','na_sales']].sort_values(by='na_sales').tail(5)
eu_reg_genre = individual_sales_genre[['genre','eu_sales']].sort_values(by='eu_sales').tail(5)
jp_reg_genre = individual_sales_genre[['genre','jp_sales']].sort_values(by='jp_sales').tail(5)

plt.figure(figsize=(22,6))
plt.subplot(1,3,1)
plt.suptitle('Top 5 Videogame Sales by Genre by Region')
plt.barh(na_reg_genre['genre'], na_reg_genre['na_sales'],color='pink')
plt.title('North America')
plt.xlabel('Total Sales (USD)')

plt.subplot(1,3,2)
plt.barh(eu_reg_genre['genre'],eu_reg_genre['eu_sales'],color='yellow')
plt.title('Europe')
plt.xlabel('Total Sales (USD)')

plt.subplot(1,3,3)
plt.barh(jp_reg_genre['genre'],jp_reg_genre['jp_sales'],color='orange')
plt.title('Japan')
plt.xlabel('Total Sales (USD)')
plt.show()

# ESRB rating sales by region (NA, EU, JP)
sales_by_rating = df_games_2013.groupby('rating')[['na_sales','eu_sales','jp_sales']].sum().reset_index()

na_reg_rating = sales_by_rating[['rating','na_sales']].sort_values(by='na_sales')
eu_reg_rating = sales_by_rating[['rating','eu_sales']].sort_values(by='eu_sales')
jp_reg_rating = sales_by_rating[['rating','jp_sales']].sort_values(by='jp_sales')

plt.figure(figsize=(12,6))
plt.subplot(1,3,1)
plt.suptitle('Top 5 Videogame sales by Rating by Region')
plt.barh(na_reg_rating['rating'], na_reg_rating['na_sales'],color='pink')
plt.title('North America')
plt.xlabel('Total Sales (USD)')

plt.subplot(1,3,2)
plt.barh(eu_reg_rating['rating'],eu_reg_rating['eu_sales'],color='yellow')
plt.title('Europe')
plt.xlabel('Total Sales (USD)')

plt.subplot(1,3,3)
plt.barh(jp_reg_rating['rating'],jp_reg_rating['jp_sales'],color='orange')
plt.title('Japan')
plt.xlabel('Total Sales (USD)')

plt.show()