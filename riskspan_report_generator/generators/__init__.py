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
        lc_tot = 0
        ab_tot = 0
        max_bal_tot = 0
        min_bal_tot = 0
        for category in report.stratum_names:
            category_subset = report_strata[category]
            lc = self.loan_count(category_subset)
            lc_tot += lc
            ab = self.average_balance(category_subset)
            ab_tot += ab
            max_bal = self.max_balance(category_subset)
            max_bal_tot += max_bal
            min_bal = self.min_balance(category_subset)
            min_bal_tot += min_bal
            print(f'{category} \n '
                  f'Loan Count: {lc} Average Current Balance: {ab} Max Current Balance: {max_bal} '
                  f'Min Current Balance: {min_bal}')
        print(f'Totals \n Loan count: {lc_tot} average balance: {ab_tot} max balance: {max_bal_tot} '
              f'min balance: {min_bal_tot}')

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
        plt.legend(title='LTV')
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x(), p.get_height() + 20), rotation=90)
        return plt


class Report(ABC):
    @property
    @abstractmethod
    def stratum_names(self):
        pass

    @abstractmethod
    def get_strata(self, df):
        pass
