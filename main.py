import click
from analyzer.crawled_result_analyzer import CrawledResultAnalyzer


@click.group(chain=True)
def cli():
    pass


@click.command('analyze_crawled_result', help='Analyze crawled result')
def analyze_crawled_result():
    click.echo('do analyze_crawled_result')
    CrawledResultAnalyzer().start_analyze()
    click.echo('finished analyze_crawled_result')


if __name__ == '__main__':
    cli.add_command(analyze_crawled_result)
    cli()
