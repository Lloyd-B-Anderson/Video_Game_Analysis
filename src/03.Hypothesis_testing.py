# Libraries  
import numpy as np, pandas as pd
from scipy import stats as st 
from matplotlib import pyplot as plt

# Read clean data
df_games = pd.read_csv('games_clean.csv',sep=',')

df_games_2013 = df_games.query('year_of_release >= 2013')

xbox_user_scores = df_games_2013[(df_games_2013['platform'] == 'XOne') & (~df_games_2013['user_score'].isna())]['user_score']
pc_user_scores = df_games_2013[(df_games_2013['platform'] == 'PC') & (~df_games_2013['user_score'].isna())]['user_score']

action_user_score = df_games_2013[(df_games_2013['genre'] == 'Action') & (~df_games_2013['user_score'].isna())]['user_score']
sport_user_score = df_games_2013[(df_games_2013['genre'] == 'Sports') & (~df_games_2013['user_score'].isna())]['user_score']

alpha = 0.05
lev_console = st.levene(xbox_user_scores,pc_user_scores)
lev_genre = st.levene(action_user_score,sport_user_score)


# PRUEBA LEVENE CONSOLAS

print('Prueba levene para determinar si la varianza es igual entre las consolas (Xbox vs. PC)\n')
if lev_console.pvalue < alpha: 
    print('- Rechazamos la hipotesis nula: La varianza entre ambos grupos es diferente\n')
    eq_var_consoles = False
else: 
    print('- No podemos rechazar la hipotesis nula: Las varianzas de ambos grupos son iguales\n')
    eq_var_consoles = True
    
#PRUEBA LEVENE GENEROS 

print('Prueba levene para determinar si la varianza es igual entre los generos (Action vs. Sports)\n')
if lev_console.pvalue < alpha: 
    print('- Rechazamos la hipotesis nula: La varianza entre ambos grupos es diferente\n')
    eq_var_genre = False
else: 
    print('- No podemos rechazar la hipotesis nula: Las varianzas de ambos grupos son iguales\n')
    eq_var_genre = True

user_score_console_hyp = st.ttest_ind(xbox_user_scores,pc_user_scores, equal_var = eq_var_consoles)
user_score_genre_hyp = st.ttest_ind(action_user_score, sport_user_score, equal_var = eq_var_genre)

alpha = 0.05

# T-TEST PARA CONSOLAS 

print('T-test para el user_score del Xbox y PC\n')
if user_score_console_hyp.pvalue < alpha: 
    print('- Rechazamos la hipotesis nula: No podemos aceptar la hipotesis nula debido a que hay una diferencia significativa entre el puntaje del usuario para XBox y PC')
else: 
    print('- No podemos rechaza la hipotesis nula: No existe suficiente evidencia para determinar una diferencia significatva entre el putaje del usuario para Xbox y PC')

# T-TEST PARA GENEROS 
print('\nT-test para el user_score de los generos action y sports \n')
if user_score_genre_hyp.pvalue < alpha: 
    print('- Rechazamos la hipotesis nula: Hay una diferencia significativa entre el promedio del puntaje del usuario para los generos accion y deportes')
else: 
    print('- No podemos rechazar la hipotesis nula: No existe suficiente evidencia para determinar una diferencia significativa entre el promedio del puntaje del usuario para los generos de accion y deportes')