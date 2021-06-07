from django.shortcuts import render
import pandas as pd


# Create your views here.
def dashboardview(request):
    df = pd.read_csv('df.csv', header=0)
    games = df['table.playedGames'].max()

    df_max_g = df[(df['table.playedGames'] == games)]
    max_goal_for = max(df_max_g['table.goalsFor'])
    max_goal_against = max(df_max_g['table.goalsAgainst'])
    better_diference_goal = max(df_max_g['table.goalDifference'])

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
    mostvictoryteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.won'] == mostvictory])
    mostdeafetteam = ", ".join(df_max_g['table.team.name'][df_max_g['table.lost'] == mostdeafet])
    mostdrawteam = ", ".join(df_max_g['table.team.name'].values[df_max_g['table.draw'] == mostdraw])
    
    df_max_g_1 = df_max_g.rename(
        columns={'season.startDate':'StartSeason', 'season.endDate':'EndSeason', 'table.position':'Position',
        		'table.team.name':'Name','table.playedGames':'PlayedGames',	'table.form':'Last5Matches',
                	'table.won':'Won', 'table.draw':'Draw', 'table.lost':'Lost', 'table.points':'Points',
                    'table.goalsFor':'GoalFor', 'table.goalsAgainst':'GoalAgainst',	
                    'table.goalDifference': 'GoalDifference'})
    df_max_g_1.index = df_max_g_1.Position

    df_max_g_1 = df_max_g_1.drop(
        columns=['stage',	'type',	'group', 'season.id','season.currentMatchday','table.team.id',
        		'table.team.crestUrl', 'form', 'Unnamed: 0', 'Position'], axis=1)
    df_max_g_1 = df_max_g_1.to_html(classes='mystyle')

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
        'table': df_max_g_1
    }
    return render(request, 'templates/dashboard.html', context=context)