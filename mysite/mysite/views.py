from collections import Counter
import datetime
from itertools import takewhile, chain
from pprint import pprint
from random import randint

from django.shortcuts import render


# todo реализовать симуляцию игры камень ножницы бумага
# Правила камень бьет ножницы, ножницы бьют бумагу, бумага бьет камень.
# В иигре присутствуют 2 игрока:
# игрок в длинном плаще
# игрок в шляпе
# задача сгенерировать и вывести в шаблон dict cо следующим содержимым.
# {
#     'current_time': текущее время,
#     'winner': Кто победил в серии трех игр,
#     'games': Список строк, каждая из которых содержит информацию о ходе,
#           какой игрок, как ходил.
# }
# шаблон для view лежит тут
# mysite/templates/mysite.html


OPTIONS_LABELS = {
    'stone': 'Камень',
    'scissors': 'Ножницы',
    'paper': 'Бумага',

    'spock': 'Живи долго и процветай!',
    'lizard': 'Ящерица',
}

LOGIC_OF_WINNER = {
    'stone': ['scissors', 'lizard'],
    'scissors': ['paper', 'lizard'],
    'paper': ['stone', 'spock'],

    'spock': ['stone', 'scissors', 'paper'],

    'lizard': ['spock', 'paper'],
}




class BlackBox:

    def __init__(self, players):
        self.players = players

    def get_rand_player_turn(self):
        keys = list(LOGIC_OF_WINNER.keys())
        return keys[randint(0, len(keys) - 1)]

    def get_games(self, count=1):
        games = []
        for game_num in range(count):
            results = {}
            turns = [self.get_rand_player_turn() for x in self.players]
            for player_num, player in enumerate(self.players):
                logic = LOGIC_OF_WINNER[turns[player_num]]
                turns_ = turns[:]
                turns_[player_num] = None
                state = list(map(lambda x: True if x in logic else False, turns_))
                wincounter = Counter(filter(lambda x: x, state)).most_common(1)
                results[player] = {
                    'turn': turns[player_num],
                    'points': 0 if not len(wincounter) else wincounter[0][1]
                }

            games.append(results)

        return games

    def get_winner(self, game):
        tuple_list = [(key, value) for key, value in game.items()]
        tuple_list.sort(key=lambda x: x[1]['points'], reverse=True)
        max_point = tuple_list[0][1]['points']
        winners = list(takewhile(lambda x: max_point != 0 and
                                 x[1]['points'] == max_point, tuple_list))

        return winners


def running_with_scissors(request):
    players = ['игрок в длинном плаще', 'игрок в шляпе']
    gamebox = BlackBox(players)
    games = gamebox.get_games(3)
    winners = [x[0] for x in chain.from_iterable(map(gamebox.get_winner, games))]
    wincounter = Counter(filter(lambda x: x, winners)).most_common(1)

    games_turns = []
    for i, game in enumerate(games):
        cnt = i+1
        turnstr = f'Игра {cnt}: '
        for player in players:
            result = game[player]
            turn = OPTIONS_LABELS[result['turn']]
            turnstr += f' Игрок "{player}" походил "{turn}". '

        winers = gamebox.get_winner(game)
        player = winers[0][0] if len(winers) else 'Ничья'
        turnstr += f'Победил игрок "{player}".'

        games_turns.append(turnstr)

    return render(request, 'mysite.html', {
        'current_time': datetime.datetime.now(),
        'winner': wincounter[0][0] if len(wincounter) else 'Ничья',
        'games': games_turns,
    })

