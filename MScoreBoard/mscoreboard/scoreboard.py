from . import sql
from . import config

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from llpy import *


sql.create_scoreboard_db()


def update_scoreboard(player, type_update=False):
    if type_update:
        online = len(mc.getOnlinePlayers()) - 1

    else:
        online = len(mc.getOnlinePlayers())

    name_server = config.name_server
    player_name = config.player_name + str(player.realName)

    online = config.online + str(online) + config.max_online

    kills = config.kills + str(sql.get_value(player.realName, 'kills'))
    deaths = config.deaths + str(sql.get_value(player.realName, 'deaths'))

    scoreboard = {player_name: 1, online: 2, kills: 3, deaths: 4}

    player.removeSidebar()
    player.setSidebar(name_server, scoreboard, 0)


@handle('onJoin')
def _(player: LLSE_Player):
    sql.adding_player(player.realName)
    
    online_players_links = mc.getOnlinePlayers()
    
    for online_player_link in online_players_links:
        update_scoreboard(online_player_link)


@handle('onLeft')
def _(player: LLSE_Player):
    online_players_links = mc.getOnlinePlayers()

    for online_player_link in online_players_links:
        update_scoreboard(online_player_link, True)


@handle('onPlayerDie')
def _(player: LLSE_Player, source: LLSE_Entity):
    sql.add_value(player.realName, 'deaths')

    update_scoreboard(player)


@handle('onMobDie')
def _(mob: LLSE_Entity, source: LLSE_Entity, cause: int):
    try:
        online_players_links = mc.getOnlinePlayers()
        online_players = [player.realName for player in online_players_links]

        if mob.name in online_players and source.name in online_players:
            player = mc.getPlayer(source.name)

            sql.add_value(player.realName, 'kills')
            update_scoreboard(player)

    except AttributeError:
        pass