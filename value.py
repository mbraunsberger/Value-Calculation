import requests
import sys
from bs4 import BeautifulSoup


url_premiere_league_base = "https://www.weltfussball.at/spielplan/eng-premier-league-2019-2020-spieltag/"
seperator = "-----------------------------------------------------------" + "\n"
current_week = 25





# --------------------------------------------------
# downloads all games from a given week
# --------------------------------------------------
def url_download_game(url, week):
    week_url = get_url(url, week, 1)
    r = requests.get(week_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find('table', {"class": "standard_tabelle"})
    table_row = table.find_all('tr')

    for tr in table_row:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if row:
            print(row, len(row))
            write_in_game_file(row)



# --------------------------------------------------
# downloads the table
# --------------------------------------------------
def url_download_table(url, week, mode):
    week_url = get_url(url, week, mode)
    r = requests.get(week_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    if mode == 1:
        table_file.write("Tabelle\n")
        tables = soup.findAll('table', {"class": "standard_tabelle"})
        table_row = tables[1].find_all('tr')

    elif ((mode == 2) or (mode == 3)):
        if mode == 2:
            table_file.write("Heim\n")
        elif mode == 3:
            table_file.write("Auswaerts\n")

        table = soup.find('table', {"class": "standard_tabelle"})
        table_row = table.find_all('tr')

    for tr in table_row:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if row:
            print(row)
            write_in_table_file(row)



# --------------------------------------------------
# creates the url string for one week
# --------------------------------------------------
def get_url(base, number, mode):
    if mode == 1:
        hole_string = base + str(number) + "/"
    elif mode == 2:
        hole_string = base + str(number) + "/heim/"
    elif mode == 3:
        hole_string = base + str(number) + "/auswaerts/"
    return hole_string




# --------------------------------------------------
# writes every game into file
# --------------------------------------------------
def write_in_game_file(game_list):
    for element in game_list:
        if (element == ''):
            continue
        printable_element = element.strip() + " "
        game_file.write(printable_element)
    game_file.write('\n')




# --------------------------------------------------
# writes table into file
# --------------------------------------------------
def write_in_table_file(table_list):
    for element in table_list:
        if (element.strip() == ''):
            continue
        printable_element = element.strip() + " "
        table_file.write(printable_element)
    table_file.write('\n')



# --------------------------------------------------
# loads all games from first till current week
# --------------------------------------------------
def download_games():
    for index in range(1, current_week):
        game_file.write("week " + str(index) + "\n" + seperator)
        url_download_game(url_premiere_league_base, index)
        game_file.write(seperator)





# --------------------------------------------------
# loads the current table from a given league
# --------------------------------------------------
def download_league_table():
    url_download_table(url_premiere_league_base, (current_week-1), 1) # download of the current table
    url_download_table(url_premiere_league_base, (current_week-1), 2) # download of the current home table
    url_download_table(url_premiere_league_base, (current_week-1), 3) # download of the current visitor table






# --------------------------------------------------
# actual script
# --------------------------------------------------
print(len(sys.argv))
if (len(sys.argv) > 1):
    for argument in sys.argv:
        if (argument == "-g"):
            print("downloading Games")
            game_file = open("game_file.txt", "w")
            download_games()
            game_file.close()
        elif (argument == "-t"):
            print("downloading Table")
            table_file = open("table_file.txt", "w")
            download_league_table()
            table_file.close()
        elif (argument == "value.py"):
            continue
        else:
            print("unknown Argument")
else:
    print("no Arguments")
