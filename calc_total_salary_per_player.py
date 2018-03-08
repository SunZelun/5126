import csv
import os
from decimal import Decimal


def get_player_total_salaries():
    player_folders = [f[0] for f in os.walk("players")]
    player_folders.remove('players')
    player_salaries = {}

    for folder in player_folders:
        player_name = folder.split("\\")[1]
        print player_name
        with open(folder+"\salary.csv", 'r') as salary_file:
            salaries = [{k: v for k, v in row.items()} for row in csv.DictReader(salary_file, skipinitialspace=True)]

            if len(salaries) > 0:
                for salary in salaries:
                    salary['salary'] = 0 if salary['salary'] == '' or salary is None else salary['salary']
                    if player_name in player_salaries.keys():
                        player_salaries[player_name] += Decimal(salary['salary'])
                    else:
                        player_salaries[player_name] = Decimal(salary['salary'])

            print player_salaries

    stats_with_salary = []
    with open("players_total_stats.csv", 'r+') as salary_file:
        reader = csv.reader(salary_file)

        for row in reader:
            for name in player_salaries.keys():
                if name in row:
                    row.append(player_salaries[name])
            stats_with_salary.append(row)

    with open("players_total_stats_with_salary.csv", 'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(stats_with_salary)

    print "Finished"


# start calc
get_player_total_salaries()
