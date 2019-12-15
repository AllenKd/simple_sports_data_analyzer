import os

import pymysql
import yaml
from sqlalchemy import create_engine

from config.constant import global_constant
from config.logger import get_logger


class Util:
    def __init__(self):
        # TODO: make singleton
        self.logger = get_logger(self.__class__.__name__)
        with open('config/configuration.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.Loader)

    def load_environment_variable(self):
        self.logger.info('start load environment variables and overwrite config file')
        with open('config/configuration.yml') as config:
            config = yaml.load(config, Loader=yaml.FullLoader)

            config[global_constant.DB][global_constant.host] = os.environ.get('DB_HOST') if \
                os.environ.get('DB_HOST') else config[global_constant.DB][global_constant.host]

            config[global_constant.DB][global_constant.port] = int(os.environ.get('DB_PORT')) if \
                os.environ.get('DB_PORT') else config[global_constant.DB][global_constant.port]

            config[global_constant.DB][global_constant.user] = os.environ.get('DB_USERNAME') if \
                os.environ.get('DB_USERNAME') else config[global_constant.DB][global_constant.user]

            config[global_constant.DB][global_constant.password] = os.environ.get('DB_PASSWORD') if \
                os.environ.get('DB_PASSWORD') else config[global_constant.DB][global_constant.password]

        # overwrite config by environment variable
        with open('config/configuration.yml', 'w') as new_config:
            yaml.dump(config, new_config)

        self.logger.debug('finish update config file')
        return

    def get_config(self):
        self.logger.info('getting config')
        return self.config

    def get_db_connection(self):
        self.logger.info('getting db connection')
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        port = self.config[global_constant.DB][global_constant.port]
        return pymysql.connect(host=host, user=user, passwd=password, port=port,
                               db=self.config[global_constant.DB][global_constant.schema], charset='utf8')

    def get_db_engine(self):
        self.logger.info('getting db engine')
        user = self.config[global_constant.DB][global_constant.user]
        password = self.config[global_constant.DB][global_constant.password]
        host = self.config[global_constant.DB][global_constant.host]
        port = self.config[global_constant.DB][global_constant.port]
        return create_engine('mysql+pymysql://{}:{}@{}:{}'.format(user, password, host, port))

    def last_index(self, table_name):
        self.logger.debug('getting the last index of table: {}'.format(table_name))
        cursor = self.get_db_connection().cursor()
        cursor.execute('SELECT COUNT(*) FROM %s' % table_name)
        return cursor.fetchone()[0]

    def dataframe_to_db(self, df, table_name):
        self.logger.info('writing dataframe to db, table name: {}'.format(table_name))

        df.to_sql(con=self.get_db_engine(),
                  name=table_name,
                  index_label='id',
                  if_exists='append',
                  schema=self.config[global_constant.DB][global_constant.schema])
        self.logger.info('finished write game data to db')
        return
