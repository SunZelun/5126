from urllib2 import urlopen, HTTPError, URLError
from bs4 import BeautifulSoup, Comment
import csv
import requests
import time
import os
from collections import defaultdict
from datetime import date
from datetime import datetime
import re
from selenium import webdriver

WEBSITE_BASEURL = "https://www.basketball-reference.com"
VALID_SEASON_LIST = ['2007-08', '2008-09', '2009-10', '2010-11', '2011-12',
                     '2012-13', '2013-14', '2014-15', '2015-16', '2016-17']
INTERNET_CONNECTION = True


def calculate_age(born):
    born = datetime.strptime(born, '%Y-%m-%d')
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def get_player_urls():
    player_urls = set([])
    # open csv file
    with open('players.csv', 'rb') as csvfile:

        # get number of columns
        for line in csvfile.readlines():
            array = line.split(',')

            url_item = array[len(array)-2]
            if url_item not in player_urls:
                player_urls.add(url_item)

    return player_urls


def get_page_content(url):
    try:
        webpage = urlopen(url).read()

        return webpage
    except HTTPError as e:
        print(e.code)
        return False
    except URLError as ue:
        print(ue.reason)
        return False


def get_player_detail(url):
    print url
    global INTERNET_CONNECTION
    # if skip_url(url):
    #     INTERNET_CONNECTION = False
    #     print "duplicate url: " + url
    #     return True

    global VALID_SEASON_LIST
    INTERNET_CONNECTION = True
    webpage = get_page_content(url)

    if webpage is False:
        print "Error on retrieving URL content"
        return False

    # store html content to offline file
    # player_profile_html = open("player_profile.html", "w")
    # player_profile_html.write(webpage)
    # player_profile_html.close()

    # use regex to retrieve player's basic profile
    # name = re.search(r'name">(.*?)</h1>', webpage).group(1)
    # height = re.search(r'(\d{3}?)cm', webpage).group(1)
    # weight = re.search(r'(\d{2,3}?)kg', webpage).group(1)
    # dob = re.search(r'data-birth="((\d{4})+(-(\d{2})+)+(-(\d{2})+))"', webpage).group(1)

    soup = BeautifulSoup(webpage, "html.parser")

    # get personal data
    player_profile = {}
    personal_detail = soup.find("div",attrs={"id": "meta"})
    player_profile['name'] = personal_detail.find("h1", attrs={"itemprop": "name"}).get_text()

    # get height and weight
    player_hw = personal_detail.find("span", attrs={"itemprop": "weight"}).next_sibling
    player_hw = player_hw.replace("(", "")
    player_hw = player_hw.replace(')', '')
    player_profile['height'] = float(player_hw.split(",")[0].replace("cm", "")) if len(player_hw.split(",")) == 2 else None
    player_profile['weight'] = float(player_hw.split(",")[1].replace("kg", "")) if len(player_hw.split(",")) == 2 else None

    # get dob and age
    player_dob = personal_detail.find("span", attrs={"itemprop": "birthDate"})
    player_profile['dob'] = player_dob.attrs['data-birth']
    player_profile['age'] = calculate_age(player_profile['dob'])

    # get college name
    player_college = personal_detail.find("strong", text=re.compile('College:'))
    player_profile['collage'] = personal_detail.find("strong", text=re.compile('College:')).parent.find("a").get_text() if player_college is not None else None

    # get play stats
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # get regular season stats
    total_per_regular_season = soup.find("table", {"id": "totals"}).find("tbody").findAll("tr")
    season_total_stats = []
    for record in total_per_regular_season:
        season_stat = {}
        season = record.find('th', {"data-stat": "season"}).find('a').string
        if season not in set(VALID_SEASON_LIST):
            continue
        print "Getting season " + season + " regular season data!"
        season_stat['season'] = set_default_value(season)
        season_stat['age'] = set_default_value(record.find("td", {"data-stat": "age"}).string)
        season_stat['team'] = set_default_value(record.find("td", {"data-stat": "team_id"}).string)
        season_stat['position'] = set_default_value(record.find("td", {"data-stat": "pos"}).string)
        season_stat['game_played'] = set_default_value(record.find("td", {"data-stat": "g"}).string)
        season_stat['minutes_played'] = set_default_value(record.find("td", {"data-stat": "mp"}).string)
        season_stat['field_goal'] = set_default_value(record.find("td", {"data-stat": "fg"}).string)
        season_stat['field_goal_total'] = set_default_value(record.find("td", {"data-stat": "fga"}).string)
        season_stat['effective_field_goal'] = set_default_value(record.find("td", {"data-stat": "efg_pct"}).string)
        season_stat['off_rb'] = set_default_value(record.find("td", {"data-stat": "orb"}).string)
        season_stat['def_rb'] = set_default_value(record.find("td", {"data-stat": "drb"}).string)
        season_stat['assist'] = set_default_value(record.find("td", {"data-stat": "ast"}).string)
        season_stat['steal'] = set_default_value(record.find("td", {"data-stat": "stl"}).string)
        season_stat['block'] = set_default_value(record.find("td", {"data-stat": "blk"}).string)
        season_stat['turn_over'] = set_default_value(record.find("td", {"data-stat": "tov"}).string)
        season_stat['points'] = set_default_value(record.find("td", {"data-stat": "pts"}).string)
        season_stat['stats_type'] = "regular"

        season_total_stats.append(season_stat)
        print "finished regular season data"

    # get playoffs stats if any
    total_per_playoffs = soup.find("table", {"id": "playoffs_totals"})
    if total_per_playoffs is not None:
        total_per_playoffs = total_per_playoffs.find("tbody").findAll("tr")

        for record in total_per_playoffs:
            season_stat = {}
            season = record.find('th', {"data-stat": "season"}).find('a').string
            print season
            if season not in set(VALID_SEASON_LIST):
                continue
            print "Getting season " + season + " playoffs data!"
            season_stat['season'] = set_default_value(season)
            season_stat['age'] = set_default_value(record.find("td", {"data-stat": "age"}).string)
            season_stat['team'] = set_default_value(record.find("td", {"data-stat": "team_id"}).string)
            season_stat['position'] = set_default_value(record.find("td", {"data-stat": "pos"}).string)
            season_stat['game_played'] = set_default_value(record.find("td", {"data-stat": "g"}).string)
            season_stat['minutes_played'] = set_default_value(record.find("td", {"data-stat": "mp"}).string)
            season_stat['field_goal'] = set_default_value(record.find("td", {"data-stat": "fg"}).string)
            season_stat['field_goal_total'] = set_default_value(record.find("td", {"data-stat": "fga"}).string)
            season_stat['effective_field_goal'] = set_default_value(record.find("td", {"data-stat": "efg_pct"}).string)
            season_stat['off_rb'] = set_default_value(record.find("td", {"data-stat": "orb"}).string)
            season_stat['def_rb'] = set_default_value(record.find("td", {"data-stat": "drb"}).string)
            season_stat['assist'] = set_default_value(record.find("td", {"data-stat": "ast"}).string)
            season_stat['steal'] = set_default_value(record.find("td", {"data-stat": "stl"}).string)
            season_stat['block'] = set_default_value(record.find("td", {"data-stat": "blk"}).string)
            season_stat['turn_over'] = set_default_value(record.find("td", {"data-stat": "tov"}).string)
            season_stat['points'] = set_default_value(record.find("td", {"data-stat": "pts"}).string)
            season_stat['stats_type'] = "playoffs"

            season_total_stats.append(season_stat)
            print "finished playoffs data"

    # get college stats if any
    college_total_stats = []
    total_per_college = soup.find("table", {"id": "all_college_stats"})
    if total_per_college is not None:
        total_per_college = total_per_college.find("tbody").findAll("tr")

        for record in total_per_college:
            college_stat = {}
            season = record.find('th', {"data-stat": "season"}).string
            print "Getting season " + season + " college data!"
            college_stat['season'] = season
            college_stat['age'] = set_default_value(record.find("td", {"data-stat": "age"}).string)
            college_stat['college'] = set_default_value(record.find("td", {"data-stat": "college_id"}).find('a').attrs['title'])
            college_stat['game_played'] = set_default_value(record.find("td", {"data-stat": "g"}).string)
            college_stat['minutes_played'] = set_default_value(record.find("td", {"data-stat": "mp"}).string)
            college_stat['field_goal'] = set_default_value(record.find("td", {"data-stat": "fg"}).string)
            college_stat['field_goal_total'] = set_default_value(record.find("td", {"data-stat": "fga"}).string)
            college_stat['total_rb'] = set_default_value(record.find("td", {"data-stat": "trb"}).string)
            college_stat['assist'] = set_default_value(record.find("td", {"data-stat": "ast"}).string)
            college_stat['steal'] = set_default_value(record.find("td", {"data-stat": "stl"}).string)
            college_stat['block'] = set_default_value(record.find("td", {"data-stat": "blk"}).string)
            college_stat['turn_over'] = set_default_value(record.find("td", {"data-stat": "tov"}).string)
            college_stat['points'] = set_default_value(record.find("td", {"data-stat": "pts"}).string)

            college_total_stats.append(college_stat)
            print "finished college data"

    # get salaries
    salary_per_season = []
    salary_per_season_table = soup.find("table", {"id": "all_salaries"})
    if salary_per_season_table is not None:
        salary_per_season_table = salary_per_season_table.find("tbody").findAll("tr")
        for record in salary_per_season_table:
            salary_data = {}
            season = record.find('th', {"data-stat": "season"}).string
            league = record.find("td", {"data-stat": "lg_id"}).find('a').string
            print season
            if season not in set(VALID_SEASON_LIST) or league != 'NBA':
                continue
            print "Getting season " + season + " salary data!"
            salary_data['season'] = season
            salary_data['team'] = record.find("td", {"data-stat": "team_name"}).string
            salary_data['salary'] = record.find("td", {"data-stat": "salary"}).attrs['csk'] if record.find("td", {"data-stat": "salary"}).has_attr('csk') else ""

            salary_per_season.append(salary_data)
            print "finished salary data"

    # output to csv file
    write_to_files(player_profile, season_total_stats, college_total_stats, salary_per_season)

    # update cursor
    write_finished_url_to_file(url)


def get_header(item_list):
    if len(item_list) > 0:
        return item_list[0].keys()

    return None


def write_to_files(player_profile, season_stats, college_stats, salaries):
    if not os.path.exists('players/'+player_profile['name']):
        os.makedirs('players/'+player_profile['name'])

    dir = 'players/'+player_profile['name']+'/'

    # write player profile
    profile_file = open(dir+"profile.csv", "w+")
    profile_header = get_header([player_profile])
    if profile_header is not None:
        profile_file.write(",".join(profile_header))
        profile_file.write("\n")

        for profile in player_profile:
            profile_file.write(str(player_profile[profile]) + ",")

    profile_file.close()

    # write stats data
    stats_file = open(dir+"stats.csv", "w+")
    season_stats_header = get_header(season_stats)
    if season_stats_header is not None:
        stats_file.write(",".join(season_stats_header))
        stats_file.write("\n")

        for stats in season_stats:
            stats_file.write(",".join(stats.values()))
            stats_file.write("\n")
    stats_file.close()

    # write salary data
    salary_file = open(dir+"salary.csv", "w+")
    salary_header = get_header(salaries)
    if salary_header is not None:
        salary_file.write(",".join(salary_header))
        salary_file.write("\n")

        for salary in salaries:
            salary_file.write(",".join(salary.values()))
            salary_file.write("\n")
    salary_file.close()

    # write college data
    college_file = open(dir+"college.csv", "w+")
    college_header = get_header(college_stats)
    if college_header is not None:
        college_file.write(",".join(college_header))
        college_file.write("\n")

        for college in college_stats:
            college_file.write(",".join(college.values()))
            college_file.write("\n")
    college_file.close()

    print "Finish writing player " + player_profile['name'] + " data."


def write_finished_url_to_file(url):
    finished_log = open("finished.txt", "a")
    finished_log.write(url+",")
    finished_log.close()

    print "Log updated."


def skip_url(url):
    with open('finished.txt', 'r') as open_file:
        data = open_file.read()
        data.split(",")
        if url in data:
            return True

        return False


def set_default_value(item):
    if item is None:
        return ""
    return item


# start crawling
player_urls = get_player_urls()

if len(player_urls) is 0:
    print "Empty player url"
    exit()

for url in player_urls:
    full_url = WEBSITE_BASEURL + url
    get_player_detail(full_url)
    if INTERNET_CONNECTION is True:
        time.sleep(1)
