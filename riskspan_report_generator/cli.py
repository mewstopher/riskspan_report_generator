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
@click.option('--data', type=click.Path(resolve_path=True, exists=True, dir_okay=False))
@click.option('--sheetname')
def lender_report(data, sheetname):
    try:
        loader = DataLoader(data, sheetname)
        df = loader.extract_df()
        lender = LenderGenerator()
        lender.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.option('--data', type=click.Path(resolve_path=True, exists=True, dir_okay=False))
@click.option('--sheetname')
def ltv_report(data, sheetname):
    try:
        loader = DataLoader(data, sheetname)
        df = loader.extract_df()
        ltv = LtvGenerator()
        ltv.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.option('--data', type=click.Path(resolve_path=True, exists=True, dir_okay=False))
@click.option('--sheetname')
def loan_age_report(data, sheetname):
    try:
        loader = DataLoader(data, sheetname)
        df = loader.extract_df()
        loan_age = LoanAgeGenerator()
        loan_age.create_report(df)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.option('--data', type=click.Path(resolve_path=True, exists=True, dir_okay=False))
@click.option('--sheetname')
def crosstab_report(data, sheetname):
    try:
        loader = DataLoader(data, sheetname)
        df = loader.extract_df()
        cross_tab = FicoLtvCreator()
        ct_report = cross_tab.create_crosstab(df)
        print(ct_report)
    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


@main.command()
@click.option('--data', type=click.Path(resolve_path=True, exists=True, dir_okay=False))
@click.option('--sheetname')
@click.option('--save_loc', type=click.Path(exists=False, dir_okay=False, resolve_path=True))
def plot_crosstab(data, sheetname, save_loc):
    try:
        loader = DataLoader(data, sheetname)
        df = loader.extract_df()
        cross_tab = FicoLtvCreator()
        bar_chart = cross_tab.plot_graph(df)
        bar_chart.savefig(save_loc)

    except Exception as exc:
        click.secho(str(exc), fg='red', err=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
