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

    select_players_sql = ''' SELECT player_id, name FROM players '''
    cur = conn.cursor()
    cur.execute(select_players_sql)
    players = dict((y, x) for x, y in cur.fetchall())

    inserted_players = []
    with open("finished_players.txt", 'r') as index_file:
        inserted_players = index_file.read().replace(';', '').splitlines()

    for folder in player_folders:
        player_name = folder.split("\\")[1]
        player_name = player_name.replace(',', '')
        if player_name in inserted_players:
            continue
        player_id = players[player_name] if player_name in players else None

        with open(folder+"\college.csv", 'r') as college_file:
            colleges = [{k: v for k, v in row.items()} for row in csv.DictReader(college_file, skipinitialspace=True)]
            if len(colleges) > 0:
                for c in colleges:
                    season_id = college_seasons[c['season']] if c['season'] in college_seasons else None
                    college_id = colleges_list[c['college']] if c['college'] in colleges_list else None

                    sql = ''' INSERT INTO college_player_stats(college_id,player_id,season_id,age,game_played,minutes_played,
                                  points,field_goal,field_goal_total,assist,total_rb,steal,block,turnover)
                                                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
                    cur = conn.cursor()
                    cur.execute(sql, (college_id, player_id, season_id, c['age'], c['game_played'], c['minutes_played'], c['points'], c['field_goal'], c['field_goal_total'],c['assist'],c['total_rb'],c['steal'],c['block'],c['turn_over'],) )
                    conn.commit()
                    print 'committed'
                    print cur.lastrowid

        with open("finished_players.txt", "a") as text_file:
            text_file.write(player_name + ";")
            text_file.write("\n")

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
    with conn:
        #get_colleges()
        save_player()
