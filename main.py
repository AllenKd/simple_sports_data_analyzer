import time

import click
import schedule

from analyzer.crawled_result_analyzer import CrawledResultAnalyzer
from util.util import Util


@click.group(chain=True)
def cli():
    pass


@click.command('analyze_crawled_result', help='Analyze crawled result')
@click.option('--period', '-p',
              type=int,
              default=24,
              show_default=True,
              help='Analysis period in hour')
def analyze_crawled_result(period):
    click.echo('do analyze_crawled_result')
    Util().load_environment_variable()
    schedule.every(period).hours.do(CrawledResultAnalyzer().start_analyze)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    cli.add_command(analyze_crawled_result)
    cli()
