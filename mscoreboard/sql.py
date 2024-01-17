import os
import sqlite3

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from llpy import logger


def create_scoreboard_db():
    if not os.path.exists('plugins/python/MScoreBoard/data/scoreboard.db'):
        conn = sqlite3.connect('plugins/python/MScoreBoard/data/scoreboard.db')

        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scoreboard (
                nickname TEXT PRIMARY KEY,        
                kills INTEGER,
                deaths INTEGER
            )
        ''')

        conn.commit()

        conn.close()

        logger.info('База данных успешно создана.')
    else:
        logger.info('База данных уже существует.')


def adding_player(nickname):
    conn = sqlite3.connect('plugins/python/MScoreBoard/data/scoreboard.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM scoreboard WHERE nickname=?', (nickname,))
    user = cursor.fetchone()

    conn.close()

    if user is None:
        conn = sqlite3.connect('plugins/python/MScoreBoard/data/scoreboard.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO scoreboard (nickname, kills, deaths) VALUES (?, ?, ?)', (nickname, 0, 0))

        conn.commit()

        conn.close()

        logger.info(f'Игрок {nickname} добавлен в базу данных MBanSystem.')


def add_value(nickname, type_value):
    conn = sqlite3.connect('plugins/python/MScoreBoard/data/scoreboard.db')

    cursor = conn.cursor()

    cursor.execute(f"UPDATE scoreboard SET {type_value} = {type_value} + 1 WHERE nickname = ?;", (nickname,))

    conn.commit()
    
    conn.close()


def get_value(nickname, type_value):
    conn = sqlite3.connect('plugins/python/MScoreBoard/data/scoreboard.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT {type_value} FROM scoreboard WHERE nickname = ?', (nickname,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None