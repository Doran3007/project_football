from pandas.core.indexes.base import Index
from pandas.core.reshape.pivot import pivot_table
from football_club.models import Club
from django.shortcuts import render
import pandas as pd
from football_club.models import *
from django.views.generic.detail import DetailView


# Create your views here.
def dashboardview(request):
    df = pd.read_csv('df.csv', index_col=False)
    games = df['table.playedGames'].max()

    df_max_g = df[(df['table.playedGames'] == games)]
    max_goal_for = max(df_max_g['table.goalsFor'])
    max_goal_against = max(df_max_g['table.goalsAgainst'])
    better_diference_goal = max(df_max_g['table.goalDifference'])
    df_max_g[['season.startDate', 'season.endDate' ]]= df_max_g[['season.startDate', 'season.endDate' ]].apply(pd.to_datetime)
    startSeason = min(df_max_g['season.startDate'].dt.year)
    endtSeason = min(df_max_g['season.endDate'].dt.year)


    mostvictory = max(df_max_g['table.won'])
    mostdeafet = max(df_max_g['table.lost'])
    mostdraw = max(df_max_g['table.draw'])

    goalforpermatch = (df_max_g['table.goalsFor'].sum() / 20) / games
    goalagainstpermatch = (df_max_g['table.goalsAgainst'].sum() / 20) / games
    allgoalfor = df_max_g['table.goalsFor'].sum()
    allgoalagainst = df_max_g['table.goalsAgainst'].sum()

    # champion = df_max_g.loc[df_max_g['table.position' == 1]]['table.team.name']
    champion = ", ".join(df_max_g['table.team.name'][df_max_g['table.position'] == 1])
    mostgoalforteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.goalsFor'] == max_goal_for])
    mostgoalagainstteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.goalsAgainst'] == max_goal_against])
    mostgoaldiffteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.goalDifference'] == better_diference_goal])
    mostvictoryteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.won'] == mostvictory])
    mostdeafetteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.lost'] == mostdeafet])
    mostdrawteam = ", ".join(df_max_g['table.team.name'].values[df_max_g['table.draw'] == mostdraw])
    
    df_max_g_1 = df_max_g.rename(
        columns={'table.position':'Pos','table.team.name':'Name','table.playedGames':'Games',	
            'table.form':'Form', 'table.won':'Won', 'table.draw':'Draw', 'table.lost':'Lost', 
            'table.points':'Points', 'table.goalsFor':'GFor', 'table.goalsAgainst':'GAgan',	
            'table.goalDifference': 'GDiff'})
    df_max_g_1.index = df_max_g_1.Pos
    df_max_g_1 = df_max_g_1.rename_axis(None)

    df_max_g_1 = df_max_g_1.drop(
        columns=['stage',	'type',	'group', 'season.id','season.currentMatchday','table.team.id',
        		'table.team.crestUrl', 'form', 'Unnamed: 0', 'season.startDate','season.endDate',
                'Pos'], axis=1)

    df_max_g_1 = df_max_g_1.to_html(classes='table table-hover text-center table-sm table-responsive align-middle my-table')

    context = {
        'goalpermatch':goalforpermatch,
        'goalagainstpermatch':goalagainstpermatch,
        'allgoalfor':allgoalfor,
        'allgoalagainst':allgoalagainst,
        'champion':champion,
        'max_goal_for':max_goal_for,
        'max_goal_against':max_goal_against,
        'mostgoalforteam':mostgoalforteam,
        'mostgoalagainstteam':mostgoalagainstteam,
        'better_diference_goal':better_diference_goal,
        'mostvictoryteam':mostvictoryteam,
        'mostdeafetteam':mostdeafetteam,
        'mostdrawteam':mostdrawteam,
        'mostvictory':mostvictory,
        'mostdeafet':mostdeafet,
        'mostdraw':mostdraw,
        'startSeason':startSeason,
        'endtSeason':endtSeason,
        'mostgoaldiffteam':mostgoaldiffteam,

        'club': Club.objects.order_by('name'),
        'table': df_max_g_1
    }
    return render(request, 'templates/dashboard.html', context=context)


def team_stat(request):
    df_match = pd.read_csv('match_data.csv', index_col=False)
    df_match = df_match.loc[:, ['Date', 'Time',	'HomeTeam',	'AwayTeam',	'FTHG',	'FTAG',	'FTR','HTHG','HTAG','HTR','Referee', 'HS',	'AS',
    	'HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]
    #  скороченные названия столбцов
    # FTHG and HG = Full Time Home Team Goals
    # FTAG and AG = Full Time Away Team Goals
    # FTR and Res = Full Time Result (H=Home Win, D=Draw, A=Away Win)
    # HTHG = Half Time Home Team Goals
    # HTAG = Half Time Away Team Goals
    # HTR = Half Time Result (H=Home Win, D=Draw, A=Away Win)
    # Match Statistics (where available)
    # Attendance = Crowd Attendance
    # Referee = Match Referee
    # HS = Home Team Shots
    # AS = Away Team Shots
    # HST = Home Team Shots on Target
    # AST = Away Team Shots on Target
    # HHW = Home Team Hit Woodwork
    # AHW = Away Team Hit Woodwork
    # HC = Home Team Corners
    # AC = Away Team Corners
    # HF = Home Team Fouls Committed
    # AF = Away Team Fouls Committed
    # HFKC = Home Team Free Kicks Conceded
    # AFKC = Away Team Free Kicks Conceded
    # HO = Home Team Offsides
    # AO = Away Team Offsides
    # HY = Home Team Yellow Cards
    # AY = Away Team Yellow Cards
    # HR = Home Team Red Cards
    # AR = Away Team Red Cards
    # HBP = Home Team Bookings Points (10 = yellow, 25 = red)
    # ABP = Away Team Bookings Points (10 = yellow, 25 = red)

    # 1.Статистика команды дома/навыезде/всего(кол-во голов за матч, кол-во ударов, конверсия ударов в голы, кол-во угловых, кол-во штрафных ударов,
    # влияния стандартных положений на кол-во голов, колво желтых карточек, кол-во красных карточек, кол-во офсайдов, кол-во очков, 
    # победы/ничьи/поражения)
    def home_pts(FTHG, FTAG):
        if FTHG > FTAG:
            return 3
        elif FTHG == FTAG:
            return 1
        elif FTHG < FTAG:
            return 0
    def away_pts(FTHG, FTAG):
        if FTHG < FTAG:
            return 3
        elif FTHG == FTAG:
            return 1
        elif FTHG > FTAG:
            return 0
    
    df_match['Hwin'] = df_match.apply(lambda x: home_pts(x['FTHG'], x['FTAG']), axis=1 )
    df_match['Awin'] = df_match.apply(lambda x: away_pts(x['FTHG'], x['FTHG']), axis=1 )
    # Голы
    goal_per_match_home = round((sum(df_match['FTHG']) / (df_match['HomeTeam'].count())),1)
    goal_per_match_away = round((sum(df_match['FTAG']) / (df_match['AwayTeam'].count())),1)
    goal_per_match_all = round(((sum(df_match['FTHG']) + sum(df_match['FTAG'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Удары
    kick_per_match_home = round((sum(df_match['HS']) / (df_match['HomeTeam'].count())),1)
    kick_per_match_away = round((sum(df_match['AS']) / (df_match['AwayTeam'].count())),1)
    kick_per_match_all = round(((sum(df_match['HS']) + sum(df_match['AS'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Удары в створ
    kick_on_target_per_match_home = round((sum(df_match['HST']) / (df_match['HomeTeam'].count())),1)
    kick_on_target_per_match_away = round((sum(df_match['AST']) / (df_match['AwayTeam'].count())),1)
    kick_on_target_per_match_all = round(((sum(df_match['HST']) + sum(df_match['AST'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # угловые
    corner_per_match_home = round((sum(df_match['HC']) / (df_match['HomeTeam'].count())),1)
    corner_per_match_away = round((sum(df_match['AC']) / (df_match['AwayTeam'].count())),1)
    corner_per_match_all = round(((sum(df_match['HC']) + sum(df_match['AC'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Штрафные
    free_kick_per_match_home = round((sum(df_match['AF']) / (df_match['HomeTeam'].count())),1)
    free_kick_per_match_away = round((sum(df_match['HF']) / (df_match['AwayTeam'].count())),1)
    free_kick_per_match_all = round(((sum(df_match['AF']) + sum(df_match['HF'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Желтые карточки
    yellow_per_match_home = round((sum(df_match['HY']) / (df_match['HomeTeam'].count())),1)
    yellow_per_match_away = round((sum(df_match['AY']) / (df_match['AwayTeam'].count())),1)
    yellow_per_match_all = round(((sum(df_match['HY']) + sum(df_match['AY'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Красные карточки
    red_per_match_home = round((sum(df_match['HR']) / (df_match['HomeTeam'].count())),1)
    red_per_match_away = round((sum(df_match['AR']) / (df_match['AwayTeam'].count())),1)
    red_per_match_all = round(((sum(df_match['HR']) + sum(df_match['AR'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # очки
    pts_per_match_home = sum(df_match['Hwin'])
    pts_per_match_away = sum(df_match['Awin'])
    # конверсия ударов в голы
    kick_conv_per_match_home = round((kick_per_match_home / goal_per_match_home ),0)
    kick_conv_per_match_away = round((kick_per_match_away / goal_per_match_away ),0)
    kick_conv_per_match_all = round((kick_per_match_all / goal_per_match_all),0)
    #  конверсия ударов в створ ворот в голы
    kick_on_target_conv_per_match_home = round(( kick_on_target_per_match_home / goal_per_match_home),0)
    kick_on_target_conv_per_match_away = round((kick_on_target_per_match_away / goal_per_match_away ),0)
    kick_on_target_conv_per_match_all = round((kick_on_target_per_match_all/ goal_per_match_all),0)
    # конверсия стандартных положений в голы
    free_kick_conv_per_match_home = round(((corner_per_match_home + free_kick_per_match_home) / goal_per_match_home ),0)
    free_kick_conv_per_match_away = round(((corner_per_match_away + free_kick_per_match_away) / goal_per_match_away ),0)
    free_kick_conv_per_match_all = round(((corner_per_match_all + free_kick_per_match_all) / goal_per_match_all ),0)
    # список команд

    df_goal_home = df_match.pivot_table(
        index='HomeTeam',
        values = ['FTHG','FTAG', 'HS', 'HST', 'HF', 'HC', 'HY', 'HR', 'AwayTeam'],
        aggfunc = {'FTHG':'sum', 'FTAG':'sum', 'HS':'sum', 'HST':'sum', 'HF':'sum', 'HC':'sum', 'HY':'sum', 'HR':'sum', 'AwayTeam':'count'},
        margins = False
    )
    df_goal_home.reset_index(inplace=True)

    df_goal_home['goal_per_match_home'] = round((df_goal_home['FTHG'] / df_goal_home['AwayTeam']),1)
    df_goal_home['goal_per_match_away'] = round((df_goal_home['FTAG'] / df_goal_home['AwayTeam']),1)
    df_goal_home['realiz_chance'] = round((df_goal_home['HS'] / df_goal_home['FTHG']),0)


    # df_goal_home['goal_per_match_away'] = round((df_goal_home['FTAG'] / df_goal_home['AwayTeam']),1)
    # df_goal_var = df_goal_home.drop(['FTHG','FTAG', 'HS', 'HST', 'HF', 'HC', 'HY', 'HR', 'AwayTeam'], axis='columns', inplace=True)
    df_goal_var = df_goal_home.loc[:, ['HomeTeam','goal_per_match_home', 'goal_per_match_away', 'realiz_chance']]
    df_goal_var = df_goal_var.sort_values(by='goal_per_match_home', ascending=False)
    goal_label = df_goal_var['HomeTeam'].values.tolist()
    goal_value = df_goal_var['goal_per_match_home'].values.tolist()
    goal_away_value = df_goal_var['goal_per_match_away'].values.tolist()
    realiz_chance = df_goal_var['realiz_chance'].values.tolist()


    
    
    df_goal_away = df_match.pivot_table(
        index='AwayTeam',
        values = ['FTAG','FTHG', 'AS', 'AST', 'AF', 'AC', 'AY', 'AR', 'HomeTeam'],
        aggfunc = {'FTAG':'sum', 'FTHG':'sum', 'AS':'sum', 'AST':'sum', 'AF':'sum', 'AC':'sum', 'AY':'sum', 'AR':'sum', 'HomeTeam':'count'},
        margins = False
    )
    df_goal_away.reset_index(inplace=True)
    df_goal_away['goal_per_match_home'] = round((df_goal_away['FTHG'] / df_goal_away['HomeTeam']),1)
    df_goal_away['goal_per_match_away'] = round((df_goal_away['FTAG'] / df_goal_away['HomeTeam']),1)
    df_goal_away['realiz_chance'] = round((df_goal_away['AS'] / df_goal_away['FTAG']),0)


    df_goalaway_var = df_goal_away.loc[:, ['AwayTeam','goal_per_match_home', 'goal_per_match_away', 'realiz_chance']]
    df_goalaway_var = df_goalaway_var.sort_values(by='goal_per_match_away', ascending=False)
    goalaway_label = df_goalaway_var['AwayTeam'].values.tolist()
    goalaway_value = df_goalaway_var['goal_per_match_home'].values.tolist()
    goalaway_away_value = df_goalaway_var['goal_per_match_away'].values.tolist()
    realizaway_chance = df_goalaway_var['realiz_chance'].values.tolist()
    showgeneral_stat = 'True'



    context = {
        'goal_per_match_home': goal_per_match_home,
        'goal_per_match_away': goal_per_match_away,
        'goal_per_match_all': goal_per_match_all,
        # Удары
        'kick_per_match_home': kick_per_match_home,
        'kick_per_match_away': kick_per_match_away,
        'kick_per_match_all': kick_per_match_all,
        # Удары в створ
        'kick_on_target_per_match_home': kick_on_target_per_match_home,
        'kick_on_target_per_match_away': kick_on_target_per_match_away,
        'kick_on_target_per_match_all': kick_on_target_per_match_all,
        # угловые
        'corner_per_match_home': corner_per_match_home,
        'corner_per_match_away': corner_per_match_away,
        'corner_per_match_all': corner_per_match_all,
        # Штрафные
        'free_kick_per_match_home': free_kick_per_match_home,
        'free_kick_per_match_away': free_kick_per_match_away,
        'free_kick_per_match_all': free_kick_per_match_all,
        # Желтые карточки
        'yellow_per_match_home': yellow_per_match_home,
        'yellow_per_match_away': yellow_per_match_away,
        'yellow_per_match_all': yellow_per_match_all,
        # Красные карточки
        'red_per_match_home': red_per_match_home,
        'red_per_match_away': red_per_match_away,
        'red_per_match_all': red_per_match_all,
        # очки
        'pts_per_match_home': pts_per_match_home,
        'pts_per_match_away': pts_per_match_away,
        # конверсия ударов в голы
        'kick_conv_per_match_home': kick_conv_per_match_home,
        'kick_conv_per_match_away': kick_conv_per_match_away,
        'kick_conv_per_match_all': kick_conv_per_match_all,
        #  конверсия ударов в створ ворот в голы
        'kick_on_target_conv_per_match_home': kick_on_target_conv_per_match_home,
        'kick_on_target_conv_per_match_away': kick_on_target_conv_per_match_away,
        'kick_on_target_conv_per_match_all': kick_on_target_conv_per_match_all,
        # конверсия стандартных положений в голы
        'free_kick_conv_per_match_home': free_kick_conv_per_match_home,
        'free_kick_conv_per_match_away': free_kick_conv_per_match_away,
        'free_kick_conv_per_match_all': free_kick_conv_per_match_all,
        # список команд
        # данные модели клубы
        'club': Club.objects.order_by('name'),
        # график для забито/пропущено дома
        'goal_label': goal_label,
        'goal_value':goal_value,
        'goal_away_value':goal_away_value,
        # график для реализация моментов дома
        'realiz_chance':realiz_chance,
        # графики на выезде
        'goalaway_label':goalaway_label,
        'goalaway_value' :goalaway_value,
        'goalaway_away_value':goalaway_away_value,
        'realizaway_chance':realizaway_chance,
        # метка для функции если при переключении инфы про одну команду
        'showgeneral_stat':showgeneral_stat
    }
    return render(request, 'templates/team.html', context=context)

def individualTeamData(request):
    var_select_team = request.POST.get('Team')
    df_match = pd.read_csv('match_data.csv', index_col=False)
    df_match = df_match.loc[:, ['Date', 'Time',	'HomeTeam',	'AwayTeam',	'FTHG',	'FTAG',	'FTR','HTHG','HTAG','HTR','Referee', 'HS',	'AS',
    	'HST','AST','HF','AF','HC','AC','HY','AY','HR','AR']]

    # 1.Статистика команды дома/навыезде/всего(кол-во голов за матч, кол-во ударов, конверсия ударов в голы, кол-во угловых, кол-во штрафных ударов,
    # влияния стандартных положений на кол-во голов, колво желтых карточек, кол-во красных карточек, кол-во офсайдов, кол-во очков, 
    # победы/ничьи/поражения)
    def home_pts(FTHG, FTAG):
        if FTHG > FTAG:
            return 3
        elif FTHG == FTAG:
            return 1
        elif FTHG < FTAG:
            return 0
    def away_pts(FTHG, FTAG):
        if FTHG < FTAG:
            return 3
        elif FTHG == FTAG:
            return 1
        elif FTHG > FTAG:
            return 0
    
    df_match['Hwin'] = df_match.apply(lambda x: home_pts(x['FTHG'], x['FTAG']), axis=1 )
    df_match['Awin'] = df_match.apply(lambda x: away_pts(x['FTHG'], x['FTAG']), axis=1 )
    # Голы
    goal_per_match_home = round((sum(df_match['FTHG']) / (df_match['HomeTeam'].count())),1)
    goal_per_match_away = round((sum(df_match['FTAG']) / (df_match['AwayTeam'].count())),1)
    goal_per_match_all = round(((sum(df_match['FTHG']) + sum(df_match['FTAG'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Удары
    kick_per_match_home = round((sum(df_match['HS']) / (df_match['HomeTeam'].count())),1)
    kick_per_match_away = round((sum(df_match['AS']) / (df_match['AwayTeam'].count())),1)
    kick_per_match_all = round(((sum(df_match['HS']) + sum(df_match['AS'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Удары в створ
    kick_on_target_per_match_home = round((sum(df_match['HST']) / (df_match['HomeTeam'].count())),1)
    kick_on_target_per_match_away = round((sum(df_match['AST']) / (df_match['AwayTeam'].count())),1)
    kick_on_target_per_match_all = round(((sum(df_match['HST']) + sum(df_match['AST'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # угловые
    corner_per_match_home = round((sum(df_match['HC']) / (df_match['HomeTeam'].count())),1)
    corner_per_match_away = round((sum(df_match['AC']) / (df_match['AwayTeam'].count())),1)
    corner_per_match_all = round(((sum(df_match['HC']) + sum(df_match['AC'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Штрафные
    free_kick_per_match_home = round((sum(df_match['AF']) / (df_match['HomeTeam'].count())),1)
    free_kick_per_match_away = round((sum(df_match['HF']) / (df_match['AwayTeam'].count())),1)
    free_kick_per_match_all = round(((sum(df_match['AF']) + sum(df_match['HF'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Желтые карточки
    yellow_per_match_home = round((sum(df_match['HY']) / (df_match['HomeTeam'].count())),1)
    yellow_per_match_away = round((sum(df_match['AY']) / (df_match['AwayTeam'].count())),1)
    yellow_per_match_all = round(((sum(df_match['HY']) + sum(df_match['AY'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # Красные карточки
    red_per_match_home = round((sum(df_match['HR']) / (df_match['HomeTeam'].count())),1)
    red_per_match_away = round((sum(df_match['AR']) / (df_match['AwayTeam'].count())),1)
    red_per_match_all = round(((sum(df_match['HR']) + sum(df_match['AR'])) / ((df_match['HomeTeam'].count())+ (df_match['AwayTeam'].count()))),1)
    # очки
    pts_per_match_home = sum(df_match['Hwin'])
    pts_per_match_away = sum(df_match['Awin'])
    # конверсия ударов в голы
    kick_conv_per_match_home = round((kick_per_match_home / goal_per_match_home ),0)
    kick_conv_per_match_away = round((kick_per_match_away / goal_per_match_away ),0)
    kick_conv_per_match_all = round((kick_per_match_all / goal_per_match_all),0)
    #  конверсия ударов в створ ворот в голы
    kick_on_target_conv_per_match_home = round(( kick_on_target_per_match_home / goal_per_match_home),0)
    kick_on_target_conv_per_match_away = round((kick_on_target_per_match_away / goal_per_match_away ),0)
    kick_on_target_conv_per_match_all = round((kick_on_target_per_match_all/ goal_per_match_all),0)
    # конверсия стандартных положений в голы
    free_kick_conv_per_match_home = round(((corner_per_match_home + free_kick_per_match_home) / goal_per_match_home ),0)
    free_kick_conv_per_match_away = round(((corner_per_match_away + free_kick_per_match_away) / goal_per_match_away ),0)
    free_kick_conv_per_match_all = round(((corner_per_match_all + free_kick_per_match_all) / goal_per_match_all ),0)
    # список команд

    df_goal_home = df_match.pivot_table(
        index='HomeTeam',
        values = ['FTHG','FTAG', 'HS', 'HST', 'HF', 'HC', 'HY', 'HR', 'AwayTeam', 'AF'],
        aggfunc = {'FTHG':'sum', 'FTAG':'sum', 'HS':'sum', 'HST':'sum', 'HF':'sum', 'HC':'sum', 'HY':'sum', 'HR':'sum', 'AwayTeam':'count',  'AF':'sum'},
        margins = False
    )
    df_goal_home.reset_index(inplace=True)

    df_goal_home['goal_per_match_home'] = round((df_goal_home['FTHG'] / df_goal_home['AwayTeam']),1)
    df_goal_home['goal_per_match_away'] = round((df_goal_home['FTAG'] / df_goal_home['AwayTeam']),1)
    df_goal_home['realiz_chance'] = round((df_goal_home['HS'] / df_goal_home['FTHG']),0)


    # df_goal_home['goal_per_match_away'] = round((df_goal_home['FTAG'] / df_goal_home['AwayTeam']),1)
    # df_goal_var = df_goal_home.drop(['FTHG','FTAG', 'HS', 'HST', 'HF', 'HC', 'HY', 'HR', 'AwayTeam'], axis='columns', inplace=True)
    df_goal_var = df_goal_home.loc[:, ['HomeTeam','goal_per_match_home', 'goal_per_match_away', 'realiz_chance']]
    df_goal_var = df_goal_var.sort_values(by='goal_per_match_home', ascending=False)
    goal_label = df_goal_var['HomeTeam'].values.tolist()
    goal_value = df_goal_var['goal_per_match_home'].values.tolist()
    goal_away_value = df_goal_var['goal_per_match_away'].values.tolist()
    realiz_chance = df_goal_var['realiz_chance'].values.tolist()
    
    df_goal_away = df_match.pivot_table(
        index='AwayTeam',
        values = ['FTAG','FTHG', 'AS', 'AST', 'AF', 'AC', 'AY', 'AR', 'HomeTeam', 'HF'],
        aggfunc = {'FTAG':'sum', 'FTHG':'sum', 'AS':'sum', 'AST':'sum', 'AF':'sum', 'AC':'sum', 'AY':'sum', 'AR':'sum', 'HomeTeam':'count','HF':'sum'},
        margins = False
    )
    df_goal_away.reset_index(inplace=True)
    df_goal_away['goal_per_match_home'] = round((df_goal_away['FTHG'] / df_goal_away['HomeTeam']),1)
    df_goal_away['goal_per_match_away'] = round((df_goal_away['FTAG'] / df_goal_away['HomeTeam']),1)
    df_goal_away['realiz_chance'] = round((df_goal_away['AS'] / df_goal_away['FTAG']),0)


    df_goalaway_var = df_goal_away.loc[:, ['AwayTeam','goal_per_match_home', 'goal_per_match_away', 'realiz_chance']]
    df_goalaway_var = df_goalaway_var.sort_values(by='goal_per_match_away', ascending=False)
    goalaway_label = df_goalaway_var['AwayTeam'].values.tolist()
    goalaway_value = df_goalaway_var['goal_per_match_home'].values.tolist()
    goalaway_away_value = df_goalaway_var['goal_per_match_away'].values.tolist()
    realizaway_chance = df_goalaway_var['realiz_chance'].values.tolist()
    showgeneral_stat = 'False'


    # Данные для индивидульного графика статистики команды
    # Информация домашних матчей
    df_ind_home = df_goal_home[df_goal_home['HomeTeam'] == var_select_team]

    ind_stat_list_label = ['Забито', 'Пропущено', 'Угловые', 'Штрафные', 'Удары', 'Удары в створ', 'Нарушения', 'Желтые карточки']
    ind_stat_list_value = [df_ind_home['FTHG'].sum(),df_ind_home['FTAG'].sum(),df_ind_home['HC'].sum(),df_ind_home['AF'].sum(),df_ind_home['HS'].sum(),
    df_ind_home['HST'].sum(), df_ind_home['HF'].sum(),df_ind_home['HY'].sum(),]
    
    # Информация выездных матчей

    # df_ind_home = df_ind_home[df_ind_home['HomeTeam'].isin(var_select_team)]
    df_ind_away = df_goal_away[df_goal_away['AwayTeam'] == var_select_team]

    ind_stat_list_label_a = ['Забито', 'Пропущено', 'Угловые', 'Штрафные', 'Удары', 'Удары в створ', 'Нарушения', 'Желтые карточки']
    ind_stat_list_value_a = [df_ind_away['FTAG'].sum(),df_ind_away['FTHG'].sum(),df_ind_away['AC'].sum(),df_ind_away['HF'].sum(),df_ind_away['AS'].sum(),
    df_ind_away['AST'].sum(), df_ind_away['AF'].sum(),df_ind_away['AY'].sum(),]
    
    # Инфа о кол-ве набранных очков по месяцам
    df_match['Date'] = df_match['Date'].apply(pd.to_datetime)
    df_match['month'] = df_match['Date'].dt.to_period('M')
    df_match[['Hwin', 'Awin']] = df_match[['Hwin', 'Awin']].apply(pd.to_numeric)

    # df_match['month'] = pd.to_datetime(df_match['Date'].dt.strftime('%Y-%m'))
    pts_h = df_match[df_match['HomeTeam'] == var_select_team]
    pts_h.to_csv('pts_h.csv')
    pts_h_pivot = pts_h.pivot_table(
        index = 'month',
        values='Hwin',
        aggfunc={'Hwin':'sum'},
        margins=False
    )

    pts_h_pivot.reset_index(inplace=True)
    pts_h_pivot.sort_values(by='month', ascending=True)
    
    pts_h_pivot.to_csv('pts_h_pivot.csv')

    pts_h_pivot['month'] = pts_h_pivot['month'].apply(str)

    pts_label = pts_h_pivot['month'].values.tolist()
    pts_home = pts_h_pivot['Hwin'].values.tolist()

    pts_a = df_match[df_match['AwayTeam'] == var_select_team]

    pts_a_pivot = pts_a.pivot_table(
        index = 'month',
        values='Awin',
        aggfunc={'Awin':'sum'},
        margins=False
    )
    pts_a_pivot.reset_index(inplace=True)
    pts_a_pivot.sort_values(by='month', ascending=True)
    pts_a_pivot['month'] = pts_a_pivot['month'].apply(str)
    
    pts_away = pts_a_pivot['Awin'].values.tolist()

    # Индивидульнные карточки со статистикой для команд
    df_indicator = df_match[(df_match['AwayTeam'] == var_select_team) | (df_match['HomeTeam'] == var_select_team)]
    df_indicator.to_csv('df_indicator.csv')
    home_goal = round(sum(df_indicator['FTHG']),1)
    away_goal = round(sum(df_indicator['FTAG']),1)

    home_kick_on_target_converse = round((sum(df_indicator['HST']) / home_goal),1)
    away_kick_on_target_converse = round((sum(df_indicator['AST']) / away_goal),1)
    home_corner_converse = round((sum(df_indicator['HC']) / home_goal),1)
    away_corner_converse = round((sum(df_indicator['AC']) / away_goal),1)

    context = {
        'goal_per_match_home': goal_per_match_home,
        'goal_per_match_away': goal_per_match_away,
        'goal_per_match_all': goal_per_match_all,
        # Удары
        'kick_per_match_home': kick_per_match_home,
        'kick_per_match_away': kick_per_match_away,
        'kick_per_match_all': kick_per_match_all,
        # Удары в створ
        'kick_on_target_per_match_home': kick_on_target_per_match_home,
        'kick_on_target_per_match_away': kick_on_target_per_match_away,
        'kick_on_target_per_match_all': kick_on_target_per_match_all,
        # угловые
        'corner_per_match_home': corner_per_match_home,
        'corner_per_match_away': corner_per_match_away,
        'corner_per_match_all': corner_per_match_all,
        # Штрафные
        'free_kick_per_match_home': free_kick_per_match_home,
        'free_kick_per_match_away': free_kick_per_match_away,
        'free_kick_per_match_all': free_kick_per_match_all,
        # Желтые карточки
        'yellow_per_match_home': yellow_per_match_home,
        'yellow_per_match_away': yellow_per_match_away,
        'yellow_per_match_all': yellow_per_match_all,
        # Красные карточки
        'red_per_match_home': red_per_match_home,
        'red_per_match_away': red_per_match_away,
        'red_per_match_all': red_per_match_all,
        # очки
        'pts_per_match_home': pts_per_match_home,
        'pts_per_match_away': pts_per_match_away,
        # конверсия ударов в голы
        'kick_conv_per_match_home': kick_conv_per_match_home,
        'kick_conv_per_match_away': kick_conv_per_match_away,
        'kick_conv_per_match_all': kick_conv_per_match_all,
        #  конверсия ударов в створ ворот в голы
        'kick_on_target_conv_per_match_home': kick_on_target_conv_per_match_home,
        'kick_on_target_conv_per_match_away': kick_on_target_conv_per_match_away,
        'kick_on_target_conv_per_match_all': kick_on_target_conv_per_match_all,
        # конверсия стандартных положений в голы
        'free_kick_conv_per_match_home': free_kick_conv_per_match_home,
        'free_kick_conv_per_match_away': free_kick_conv_per_match_away,
        'free_kick_conv_per_match_all': free_kick_conv_per_match_all,
        # список команд
        # данные модели клубы
        'club': Club.objects.order_by('name'),
        # график для забито/пропущено дома
        'goal_label': goal_label,
        'goal_value':goal_value,
        'goal_away_value':goal_away_value,
        # график для реализация моментов дома
        'realiz_chance':realiz_chance,
        # графики на выезде
        'goalaway_label':goalaway_label,
        'goalaway_value' :goalaway_value,
        'goalaway_away_value':goalaway_away_value,
        'realizaway_chance':realizaway_chance,
        # метка для функции если при переключении инфы про одну команду
        'showgeneral_stat':showgeneral_stat,
        # данные для индивидульной статки домашних матчей команды
        'ind_stat_list_label': ind_stat_list_label,
        'ind_stat_list_value': ind_stat_list_value,
        # данные для индивидульной статки выездных матчей команды
        'ind_stat_list_label_a':ind_stat_list_label_a,
        'ind_stat_list_value_a':ind_stat_list_value_a,
        # данные для графика с набранными очками по месяцам
        'pts_label':pts_label,
        'pts_away':pts_away,
        'pts_home':pts_home,
        # выбранная команда
        'var_select_team':var_select_team,
        # Данные для индивидульных карточек со статистикой команды
        'home_kick_on_target_converse':home_kick_on_target_converse,
        'away_kick_on_target_converse':away_kick_on_target_converse,
        'home_corner_converse':home_corner_converse,
        'away_corner_converse':away_corner_converse,
    }
    return render(request, 'templates/team.html', context=context)