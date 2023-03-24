import asyncio
import os
import time
import requests
from chessdotcom import get_player_game_archives

name = 'player'


def test(name):
    #month_games = requests.get(get_player_game_archives(name).json['archives'][-1]).json()
    data = get_player_game_archives(name).json
    url = data['archives'][-1]
    # month_games = requests.get(url).json()['games']
    # month_games = requests.get(url).json()
    #game = month_games['games'][-1]
    print(url)



def get_missing(name):
    missing_games = []
    with open('last_id.txt', 'r') as file:
        last_id = file.read()
    latest_games = (requests.get(get_player_game_archives(name).json['archives'][-1]).json())['games']
    for i in range(len(latest_games) - 1, 0, -1):
        if latest_games[i]['url'].split('/')[-1] == last_id:
            break
        missing_games.append(latest_games[i])
    last_id = latest_games[-1]['url'].split('/')[-1]
    with open('last_id.txt', 'w') as file:
        file.write(last_id)
    return missing_games


def shall_awake(missing):
    if len(missing) == 0:
        return 0
    return 1


def games_append(games, name):
    with open('games_to_comment.txt', 'w') as file:
        for game in games:
            if game['rules'] == 'chess' and game['rated']:
########################################  НИКИ   #######################################################################
                file.write(name + '\n')
                if game['white']['username'] != name:
                    file.write(game['white']['username'] + '\n')
                else:
                    file.write(game['black']['username'] + '\n')
###################################  Результат  ########################################################################
                if ((game['white']['result'] == 'insufficient') or (game['white']['result'] == 'repetition')) and game['white']['username'] == name:
                    file.write('draw\nwhite\n')
                elif ((game['white']['result'] == 'insufficient') or (game['white']['result'] == 'repetition')) and game['black']['username'] == name:
                    file.write('draw\nblack\n')
                elif game['white']['result'] == 'win' and game['white']['username'] == name:
                    file.write('win\nwhite\n')
                elif game['white']['result'] != 'win' and game['white']['username'] == name:
                    file.write('lose\nwhite\n')
                elif game['black']['result'] == 'win':
                    file.write('win\nblack\n')
                else:
                    file.write('lose\nblack\n')


#######################################################################################################################
                file.write(game['time_class'] + '\n')               #Тайм - контроль
#######################################################################################################################
                if game['white']['username'] == name:
                    file.write(str(game['white']['rating']) + '\n')     #Рейтинг
                    file.write(str(game['black']['rating']) + '\n')
                else:
                    file.write(str(game['black']['rating']) + '\n')
                    file.write(str(game['white']['rating']) + '\n')
                file.write(game['url'].split('/')[-1] + '\n')
                file.write('#' + '\n')


while True:
    games_to_comment = get_missing(name)
    if shall_awake(games_to_comment):
        games_append(games_to_comment, name)
        os.startfile(r'bot.py')
        time.sleep(300)
        continue
    time.sleep(30)





