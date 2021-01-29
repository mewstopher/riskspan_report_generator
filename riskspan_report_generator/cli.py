# _*_ coding: utf-8 _*_

from riskspan_report_generator.generators.report_generators import LenderGenerator,\
    LtvGenerator, LoanAgeGenerator, FicoLtvCreator
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
        lender = LenderGenerator()
        lender.create_report(df)
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
        ltv = LtvGenerator()
        ltv.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.argument('data_file')
@click.argument('data_sheet')
def loan_age_report(data_file, data_sheet):
    try:
        loader = DataLoader(data_file, data_sheet)
        df = loader.extract_df()
        loan_age = LoanAgeGenerator()
        loan_age.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.argument('data_file')
@click.argument('data_sheet')
def crosstab_report(data_file, data_sheet):
    try:
        loader = DataLoader(data_file, data_sheet)
        df = loader.extract_df()
        cross_tab = FicoLtvCreator()
        cross_tab.create_crosstab(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0

@main.command()
@click.argument('data_file')
@click.argument('data_sheet')
def plot_crosstab(data_file, data_sheet):
    try:
        loader = DataLoader(data_file, data_sheet)
        df = loader.extract_df()
        cross_tab = FicoLtvCreator()
        cross_tab.plot_graph(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
