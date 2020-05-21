import functools

import numpy as np
import pandas as pd

from config.logger import get_logger
from util.util import Util


class CrawledResultAnalyzer:
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.config = Util().get_config()
        self.db = Util().get_db_connection()

    def start_analyze(self):
        self.logger.info('start analyzer')
        self.db = Util().get_db_connection()
        Util().dataframe_to_db(self.judge_game_data(), 'game_judgement')

        for group in self.get_prediction_groups():
            Util().dataframe_to_db(self.judge_prediction(group), 'prediction_judgement_{}'.format(group))

        self.logger.info('analyzer done')
        return

    def get_prediction_groups(self):
        self.logger.debug('getting prediction group')
        cursor = self.db.cursor()
        cursor.execute("""show tables like 'prediction_data%'""")
        return [group[0][16:] for group in cursor.fetchall()]

    @functools.lru_cache(maxsize=5)
    def get_data(self, table_name, begin_id):
        self.logger.debug('getting data, table name: {}, begin id: {}'.format(table_name, begin_id))
        return pd.read_sql('SELECT * FROM %s WHERE id > %d' % (table_name, begin_id), con=self.db, index_col='id')

    def judge_game_data(self):
        self.logger.debug('judging game result')

        latest_judgement = Util().last_index('game_judgement')

        game_data = self.get_data('game_data', latest_judgement)
        game_judgement = pd.DataFrame(index=game_data.index)
        game_judgement['game_date'] = game_data['game_date']
        game_judgement['gamble_id'] = game_data['gamble_id']
        game_judgement['game_type'] = game_data['game_type']

        game_judgement['host_win_original'] = game_data['guest_score'] < game_data['host_score']

        game_judgement['host_win_point_spread_national'] = game_data['guest_score'] < (
                game_data['host_score'] - game_data['national_host_point_spread'])

        game_judgement['host_win_point_spread_local'] = game_data['guest_score'] < (
                game_data['host_score'] - game_data['local_host_point_spread'])

        game_judgement['over_total_point_national'] = (game_data['guest_score'] + game_data['host_score']) > \
                                                      game_data['national_total_point_threshold']

        game_judgement['over_total_point_local'] = (game_data['guest_score'] + game_data[
            'host_score']) > game_data['local_total_point_threshold']

        self.logger.info('finished game judgement, total: {}'.format(len(game_judgement)))
        return game_judgement

    def judge_prediction(self, group):
        self.logger.info('start prediction judge, {}'.format(group))

        latest_judgement = Util().last_index('prediction_judgement_{}'.format(group))
        prediction_data = self.get_data('prediction_data_{}'.format(group), latest_judgement)
        game_judgement = self.get_data('game_judgement', latest_judgement)

        prediction_judgement = pd.DataFrame(index=prediction_data.index)
        prediction_judgement['game_date'] = prediction_data['game_date']
        prediction_judgement['gamble_id'] = prediction_data['gamble_id']
        prediction_judgement['game_type'] = prediction_data['game_type']

        self.logger.debug('start judge local original case')
        temp_target_prediction = (prediction_data['population_local_original_guest'] < prediction_data[
            'population_local_original_host']).astype(int)
        prediction_judgement['local_original_result'] = temp_target_prediction == game_judgement['host_win_original']
        prediction_judgement['local_original_percentage'] = np.where(
            game_judgement['host_win_original'],
            prediction_data['percentage_local_original_host'],
            prediction_data['percentage_local_original_guest'])
        prediction_judgement['local_original_population'] = np.where(
            game_judgement['host_win_original'],
            prediction_data['population_local_original_host'],
            prediction_data['population_local_original_guest'])

        self.logger.debug('start judge local total point')
        temp_target_prediction = prediction_data['population_local_total_point_over'] > prediction_data[
            'population_local_total_point_under']
        prediction_judgement['local_total_point_result'] = game_judgement[
                                                               'over_total_point_local'] == temp_target_prediction
        prediction_judgement['local_total_point_percentage'] = np.where(
            game_judgement['over_total_point_local'],
            prediction_data['percentage_local_total_point_over'],
            prediction_data['percentage_local_total_point_under'])
        prediction_judgement['local_total_point_population'] = np.where(
            game_judgement['over_total_point_local'],
            prediction_data['population_local_total_point_over'],
            prediction_data['population_local_total_point_under'])

        self.logger.debug('start judge local point spread')
        temp_target_prediction = prediction_data['population_local_point_spread_guest'] < prediction_data[
            'population_local_point_spread_host']
        prediction_judgement['local_point_spread_result'] = game_judgement[
                                                                'host_win_point_spread_local'] == temp_target_prediction
        prediction_judgement['local_point_spread_percentage'] = np.where(
            game_judgement['host_win_point_spread_local'],
            prediction_data['percentage_local_point_spread_host'],
            prediction_data['percentage_local_point_spread_guest'])
        prediction_judgement['local_point_spread_population'] = np.where(
            game_judgement['host_win_point_spread_local'],
            prediction_data['population_local_point_spread_host'],
            prediction_data['population_local_point_spread_guest'])

        self.logger.debug('start judge national total point')
        temp_target_prediction = prediction_data['population_national_total_point_over'] > prediction_data[
            'population_national_total_point_under']
        prediction_judgement['national_total_point_result'] = game_judgement[
                                                                  'over_total_point_national'] == temp_target_prediction
        prediction_judgement['national_total_point_percentage'] = np.where(
            game_judgement['over_total_point_national'],
            prediction_data['percentage_national_total_point_over'],
            prediction_data['percentage_national_total_point_under'])
        prediction_judgement['national_total_point_population'] = np.where(
            game_judgement['over_total_point_national'],
            prediction_data['population_national_total_point_over'],
            prediction_data['population_national_total_point_under'])

        self.logger.debug('start judge national point spread')
        temp_target_prediction = prediction_data['population_national_point_spread_guest'] < prediction_data[
            'population_national_point_spread_host']
        prediction_judgement['national_point_spread_result'] = game_judgement[
                                                                   'host_win_point_spread_national'] == temp_target_prediction
        prediction_judgement['national_point_spread_percentage'] = np.where(
            game_judgement['host_win_point_spread_national'],
            prediction_data['percentage_national_point_spread_host'],
            prediction_data['percentage_national_point_spread_guest'])
        prediction_judgement['national_point_spread_population'] = np.where(
            game_judgement['host_win_point_spread_national'],
            prediction_data['population_national_point_spread_host'],
            prediction_data['population_national_point_spread_guest'])

        self.logger.info('finished prediction judge, {}'.format(group))
        return prediction_judgement
