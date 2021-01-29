from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd


class ReportGenerator(ABC):
    @abstractmethod
    def report_factory(self):
        pass

    def create_report(self, df: pd.DataFrame):
        report = self.report_factory()
        report_strata = report.get_strata(df)
        for category in report.stratum_names:
            category_subset = report_strata[category]
            lc = self.loan_count(category_subset)
            ab = self.average_balance(category_subset)
            max_bal = self.max_balance(category_subset)
            min_bal = self.min_balance(category_subset)
            print(f'{category} \n '
                  f'Loan Count: {lc} Average Current Balance: {ab} Max Current Balance: {max_bal} '
                  f'Min Current Balance: {min_bal}')

    def loan_count(self, df_subset):
        return df_subset.shape[0]

    def average_balance(self, df_subset):
        return df_subset.CURRENT_BALANCE.mean()

    def max_balance(self, df_subset):
        return df_subset.CURRENT_BALANCE.max()

    def min_balance(self, df_subset):
        return df_subset.CURRENT_BALANCE.min()


class CrossTabGenerator(ABC):
    @abstractmethod
    def crosstab_factory(self):
        pass

    def create_crosstab(self, df: pd.DataFrame):
        report = self.crosstab_factory()
        report_strata = report.get_strata(df)
        col_names = ['<=85%', '>85% and <=90%', '>90% and <=95%', '>95%']
        df2 = pd.DataFrame(index=report.stratum_names, columns=col_names)
        df2['<=85%'] = [report_strata[i].loc[df['LTV'] <= 85].shape[0] for i in report.stratum_names]
        df2['>85% and <=90%'] = [report_strata[i].loc[(df['LTV'] > 85) & (df['LTV'] <= 90)].shape[0] for i in
                                 report.stratum_names]
        df2['>90% and <=95%'] = [report_strata[i].loc[(df['LTV'] > 90) & (df['LTV'] <= 95)].shape[0] for i in
                                 report.stratum_names]
        df2['>95%'] = [report_strata[i].loc[df['LTV'] > 95].shape[0] for i in report.stratum_names]
        return df2

    def plot_graph(self, df: pd.DataFrame):
        style.use('fivethirtyeight')
        cross_tab: pd.DataFrame = self.create_crosstab(df)
        ax = cross_tab.plot.bar()
        ax.set_xlabel("FICO Score")
        ax.set_ylabel("Count")
        plt.legend('LTV')
        return cross_tab


class Report(ABC):
    @property
    @abstractmethod
    def stratum_names(self):
        pass

    @abstractmethod
    def get_strata(self, df):
        pass
