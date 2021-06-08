from football_club.models import Club
from django.shortcuts import render
import pandas as pd
from football_club.models import *

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

    df_max_g_1 = df_max_g_1.to_html(classes='table table-bordered border-danger table table-striped table-hover text-center table-sm table-responsive table align-middle')

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