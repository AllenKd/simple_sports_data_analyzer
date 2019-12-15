import pandas as pd

from config.constant import database as db_constant
from config.logger import get_logger
from util.util import Util


class BattleResultAnalyzer(object):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.config = Util().get_config()
        self.db = Util.get_db_connection()

    def start(self):
        for player in self.get_players():
            self.get_battle_result(player)
            self.get_strategy(player[7:])

    def get_players(self):
        self.logger.info('getting players')
        cursor = self.db.cursor()
        cursor.execute("""SHOW TABLES FROM gambling_simulation WHERE Tables_in_gambling_simulation LIKE 'player_%'""")
        return [player[0] for player in cursor.fetchall()]

    def get_battle_result(self, player_table):
        self.logger.info('getting battle result: {}'.format(player_table))
        return pd.read_sql('SELECT * FROM {}'.format(player_table),
                           con=self.db,
                           index_col=db_constant.row_id)

    def get_strategy(self, player_id):
        self.logger.info('getting strategy: {}'.format(player_id))
        cursor = self.db.cursor()
        cursor.execute('SELECT bet_strategy FROM battle_summarize WHERE player_id = %d' % player_id)
        return cursor.fetchall()[0]
