from abc import ABC, abstractmethod
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

    def plot_graph(self):
        crosstab = self.crosstab_factory()
        return crosstab


class Report:
    @property
    @abstractmethod
    def stratum_names(self):
        pass

    @abstractmethod
    def get_strata(self, df: pd.DataFrame):
        """
        gets subset based on variables
        """
        pass
