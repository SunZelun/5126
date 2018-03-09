import csv
import os
import sqlite3
from decimal import Decimal


def get_colleges():
    player_folders = [f[0] for f in os.walk("players")]
    player_folders.remove('players')
    colleges = []

    for folder in player_folders:
        player_name = folder.split("\\")[1]

        # with open(folder+"\college.csv", 'r') as college_file:
        #     college = [{k: v for k, v in row.items()} for row in csv.DictReader(college_file, skipinitialspace=True)]
        #     if len(college) > 0:
        #         for c in college:
                    # save colleges to db
                    # if c['college'] not in colleges:
                    #     print c['college']
                    #     sql = ''' INSERT INTO colleges(name)
                    #                   VALUES(?) '''
                    #     cur = conn.cursor()
                    #     cur.execute(sql, (c['college'],))
                    #     conn.commit()
                    #     print cur.lastrowid
                    #     colleges.append(c['college'])


    exit()


def convert_to_team_id(short_team_name):
    team_ref_list = {
        'MIL': 17,
        'GSW': 10,
        'MIN': 18,
        'TOR': 28,
        'ATL': 1,
        'BOS': 2,
        'DET': 9,
        'TOT': None,
        'NJN': 32,
        'NYK': 20,
        'DEN': 8,
        'DAL': 7,
        'POR': 25,
        'OKC': 21,
        'MIA': 16,
        'SEA': 34,
        'CHI': 5,
        'SAS': 27,
        'CHA': 31,
        'UTA': 29,
        'CLE': 6,
        'CHO': 4,
        'HOU': 11,
        'NOH': 35,
        'WAS': 30,
        'LAL': 14,
        'PHI': 23,
        'PHO': 24,
        'MEM': 15,
        'LAC': 13,
        'SAC': 26,
        'ORL': 22,
        'BRK': 3,
        'IND': 12,
        'NOP': 19
    }

    return team_ref_list[short_team_name] if short_team_name in team_ref_list.keys() else None


def save_player():
    player_folders = [f[0] for f in os.walk("players-new")]
    player_folders.remove('players-new')
    players = []

    select_colleges_sql = ''' SELECT * FROM colleges '''
    cur = conn.cursor()
    cur.execute(select_colleges_sql)
    colleges_list = dict((y, x) for x, y in cur.fetchall())

    select_college_seasons_sql = ''' SELECT season_id, name FROM seasons WHERE type="college" '''
    cur = conn.cursor()
    cur.execute(select_college_seasons_sql)
    college_seasons = dict((y, x) for x, y in cur.fetchall())

    select_nba_seasons_sql = ''' SELECT season_id, name FROM seasons WHERE type="nba" '''
    cur = conn.cursor()
    cur.execute(select_nba_seasons_sql)
    nba_seasons = dict((y, x) for x, y in cur.fetchall())

    select_players_sql = ''' SELECT player_id, name FROM players '''
    cur = conn.cursor()
    cur.execute(select_players_sql)
    players = dict((y, x) for x, y in cur.fetchall())

    select_teams_sql = ''' SELECT team_id, name FROM teams '''
    cur = conn.cursor()
    cur.execute(select_teams_sql)
    teams = dict((y, x) for x, y in cur.fetchall())

    inserted_players = []
    with open("finished_players.txt", 'r') as index_file:
        inserted_players = index_file.read().replace(';', '').splitlines()

    # for filename in os.listdir('team'):
    #     print filename
    #     with open('team/'+filename, 'r') as team_stats_file:
    #         team_stats = [{k: v for k, v in row.items()} for row in csv.DictReader(team_stats_file, skipinitialspace=True)]
    #         if team_stats[0]['Team'] in inserted_players:
    #             continue
    #
    #         if len(teams) > 0:
    #             for t in team_stats:
    #                 season_id = nba_seasons[t['Season']] if t['Season'] in nba_seasons else None
    #                 team_id = teams[t['Team']] if t['Team'] in teams else None
    #                 sql = ''' INSERT INTO team_stats(team_id,season_id,wins,losses,rank,srs,pace,rel_pace,
    #                         ortg,rel_ortg,drtg,rel_drtg,coaches,top_ws) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    #                 cur = conn.cursor()
    #                 cur.execute(sql, (team_id, season_id,t['W'], t['L'], t['Finish'], t['SRS'], t['Pace'], t['Rel_Pace'],t['ORtg'], t['Rel_ORtg'], t['DRtg'],t['Rel_DRtg'],t['Coaches'],t['Top WS'],))
    #                 conn.commit()
    #                 print 'committed'
    #                 print cur.lastrowid
    #
    #                 with open("finished_players.txt", "a") as text_file:
    #                     text_file.write(t['Team'] + ";")
    #                     text_file.write("\n")
    #
    # print "Finished"
    # exit()

    # with open("team_active.csv", 'r') as team_file:
    #     teams = [{k: v for k, v in row.items()} for row in csv.DictReader(team_file, skipinitialspace=True)]
    #     if len(teams) > 0:
    #         for t in teams:
    #             sql = ''' INSERT INTO teams(name,from,to,total_years,games_played,wins,losses,playoffs_appearances,champs) VALUES(?,?,?,?,?,?,?,?,?) '''
    #             cur = conn.cursor()
    #             cur.execute(sql, (t['Franchise'], t['From'], t['To'], t['Yrs'], t['G'], t['W'], t['L'], t['Plyfs'], t['Champ'],))
    #             conn.commit()
    #             print 'committed'
    #             print cur.lastrowid
    #
    #             with open("finished_players.txt", "a") as text_file:
    #                 text_file.write(t['Franchise'] + ";")
    #                 text_file.write("\n")

    # with open("team.csv", 'r') as team_stats_file:
    #     salaries = [{k: v for k, v in row.items()} for row in csv.DictReader(team_stats_file, skipinitialspace=True)]
    #     if len(salaries) > 0:
    #         for s in salaries:
    #             print s
    #             season_id = nba_seasons[s['season']] if s['season'] in nba_seasons else None
    #             team_id = teams[s['team']] if s['team'] in teams else None
    #
    #             sql = ''' INSERT INTO team_player_salary(player_id,team_id,season_id,salary)
    #                                               VALUES(?,?,?,?) '''
    #             cur = conn.cursor()
    #             cur.execute(sql, (player_id, team_id, season_id, s['salary'],))
    #             conn.commit()
    #             print 'committed'
    #             print cur.lastrowid
    #             with open("finished_players.txt", "a") as text_file:
    #                 text_file.write(player_name + ";")
    #                 text_file.write("\n")
    short_list = {}
    for folder in player_folders:
        player_name = folder.split("\\")[1]
        player_name = player_name.replace(',', '')
        if player_name in inserted_players:
            continue
        player_id = players[player_name] if player_name in players else None

        with open(folder+"\stats.csv", 'r') as stats_file:
            player_stats = [{k: v for k, v in row.items()} for row in csv.DictReader(stats_file, skipinitialspace=True)]

            if len(player_stats) > 0:
                for s in player_stats:
                    team_id = convert_to_team_id(s['team'])
                    season_id = nba_seasons[s['season']] if s['season'] in nba_seasons else None
                    if team_id is None:
                        continue
                    print team_id
                    print season_id
                    print player_id
                    print player_name
                    sql = ''' INSERT INTO nba_player_stats(player_id,season_id,team_id,age,position,minutes_played,game_played,
                              points,assist,field_goal,field_goal_total,effective_field_goal,off_rb,def_rb,steal,block,stats_type,turnover)
                                                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
                    cur = conn.cursor()
                    cur.execute(sql, (player_id, season_id, team_id, s['age'],s['position'],s['minutes_played'],s['game_played'],s['points'],s['assist'],s['field_goal'],
                                      s['field_goal_total'],s['effective_field_goal'],s['off_rb'],s['def_rb'],s['steal'],s['block'],s['stats_type'],s['turn_over'],) )
                    conn.commit()
                    print 'committed'
                    print cur.lastrowid
                    with open("finished_players.txt", "a") as text_file:
                        text_file.write(player_name + ";")
                        text_file.write("\n")
    print "Finished"
    exit()
        # with open(folder+"\salary.csv", 'r') as salary_file:
        #     salaries = [{k: v for k, v in row.items()} for row in csv.DictReader(salary_file, skipinitialspace=True)]
        #     if len(salaries) > 0:
        #         for s in salaries:
        #             print s
        #             season_id = nba_seasons[s['season']] if s['season'] in nba_seasons else None
        #             team_id = teams[s['team']] if s['team'] in teams else None
        #
        #             sql = ''' INSERT INTO team_player_salary(player_id,team_id,season_id,salary)
        #                                               VALUES(?,?,?,?) '''
        #             cur = conn.cursor()
        #             cur.execute(sql, (player_id, team_id, season_id, s['salary'],) )
        #             conn.commit()
        #             print 'committed'
        #             print cur.lastrowid
        #             with open("finished_players.txt", "a") as text_file:
        #                 text_file.write(player_name + ";")
        #                 text_file.write("\n")


        # with open(folder+"\college.csv", 'r') as college_file:
        #     colleges = [{k: v for k, v in row.items()} for row in csv.DictReader(college_file, skipinitialspace=True)]
        #     if len(colleges) > 0:
        #         for c in colleges:
        #             season_id = college_seasons[c['season']] if c['season'] in college_seasons else None
        #             college_id = colleges_list[c['college']] if c['college'] in colleges_list else None
        #
        #             sql = ''' INSERT INTO college_player_stats(college_id,player_id,season_id,age,game_played,minutes_played,
        #                           points,field_goal,field_goal_total,assist,total_rb,steal,block,turnover)
        #                                               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        #             cur = conn.cursor()
        #             cur.execute(sql, (college_id, player_id, season_id, c['age'], c['game_played'], c['minutes_played'], c['points'], c['field_goal'], c['field_goal_total'],c['assist'],c['total_rb'],c['steal'],c['block'],c['turn_over'],) )
        #             conn.commit()
        #             print 'committed'
        #             print cur.lastrowid



        # with open(folder+"\profile.csv", 'r') as profile_file:
        #     profiles = [{k: v for k, v in row.items()} for row in csv.DictReader(profile_file, skipinitialspace=True)]
        #     if len(profiles) > 0:
        #         for p in profiles:
        #             sql = ''' INSERT INTO players(age,name,weight,height,dob)
        #                                               VALUES(?,?,?,?,?) '''
        #             cur = conn.cursor()
        #             cur.execute(sql, (p['age'], p['name'], p['weight'], p['height'], p['dob'],))
        #             conn.commit()
        #             print p['name']
        #             print cur.lastrowid

    print "Finished"
    exit()


if __name__ == '__main__':
    conn = sqlite3.connect('nba.db')
    conn.text_factory = str
    with conn:
        #get_colleges()
        save_player()
