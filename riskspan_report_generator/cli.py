# _*_ coding: utf-8 _*_

from riskspan_report_generator.generators.report_generators import LenderGenerator, LtvGenerator
from riskspan_report_generator.processors import DataLoader
from logging.config import fileConfig
import click
import sys

fileConfig('logging.ini')


@click.group()
def main(args=None):
    return 0


@main.command()
@click.argument('data_file')
@click.argument('data_sheet')
def lender_report(data_file, data_sheet):
    try:
        loader = DataLoader(data_file, data_sheet)
        df = loader.extract_df()
        lender_generator = LenderGenerator()
        lender_generator.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.argument('data_file')
@click.argument('data_sheet')
def ltv_report(data_file, data_sheet):
    try:
        loader = DataLoader(data_file, data_sheet)
        df = loader.extract_df()
        ltv_generator = LtvGenerator()
        ltv_generator.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
