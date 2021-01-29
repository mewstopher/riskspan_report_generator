from riskspan_report_generator.generators import ReportGenerator, CrossTabGenerator, Report
import pandas as pd


class LenderGenerator(ReportGenerator):
    def report_factory(self):
        return LenderReport()


class LtvGenerator(ReportGenerator):
    def report_factory(self):
        return LtvReport()


class LoanAgeGenerator(ReportGenerator):
    def report_factory(self):
        return LoanAgeReport()


class FicoLtvCreator(CrossTabGenerator):
    def crosstab_factory(self):
        return CrossTabReport()


class LenderReport(Report):

    @property
    def stratum_names(self):
        categories = ['Bank Owned Mortgage Company - National',
                      'Mortgage Banker - Bank Owned', 'Mortgage Banker - (Large)',
                      'Credit Unions', 'Community Banks']
        return categories

    def get_strata(self, df: pd.DataFrame) -> dict:
        strata = {}
        for stratum in self.stratum_names:
            strata[stratum] = df.loc[df['LENDER_INST_TYPE_DESCRIPTION'] == stratum]
        return strata


class LtvReport(Report):
    @property
    def stratum_names(self):
        categories = ['<= 85%', '>85% and <= 90%', '>90% and <= 95%', '>95%']
        return categories

    def get_strata(self, df: pd.DataFrame) -> dict:
        strata = {'<= 85%': df.loc[df['LTV'] <= 85],
                  '>85% and <= 90%': df.loc[(df['LTV'] > 85) & (df['LTV'] <= 90)],
                  '>90% and <= 95%': df.loc[(df['LTV'] > 90) & (df['LTV'] <= 95)],
                  '>95%': df.loc[df['LTV'] > 95]}
        return strata


class LoanAgeReport(Report):
    @property
    def stratum_names(self):
        categories = ['Unknown', '0 - 9 months', '10 - 19 months', '20 - 29 months',
                      '30 - 39 months', '40 or more months']
        return categories

    def get_strata(self, df: pd.DataFrame) -> dict:
        df_null_date = df.loc[df['LOAN_ORIG_DATE'].isnull()]
        df['months_diff'] = list(map(calculate_month, df.LOAN_ORIG_DATE, df.START_DATE))
        strata = {
            '0 - 9 months': df.loc[df['months_diff'] <= 9],
            '10 - 19 months': df.loc[(df['months_diff'] >= 10) & (df['months_diff'] <= 19)],
            '20 - 29 months': df.loc[(df['months_diff'] >= 20) & (df['months_diff'] <= 29)],

            '30 - 39 months': df.loc[(df['months_diff'] >= 30) & (df['months_diff'] <= 39)],
            '40 or more months': df.loc[df['months_diff'] >= 40],
            'Unknown': df_null_date
        }
        return strata


def calculate_month(start_date, end_date) -> int:
    months_year = (end_date.year - start_date.year) * 12
    total_months = months_year + end_date.month - start_date.month
    return total_months


class CrossTabReport(Report):
    @property
    def stratum_names(self):
        categories = ['< 600', '600 - 699', '700-799', '>= 800']
        return categories

    def get_strata(self, df):
        strata = {
            '< 600': df.loc[df['FICO_SCORE'] < 600],
            '600 - 699': df.loc[(df['FICO_SCORE'] >= 600) & (df['FICO_SCORE'] < 700)],
            '700-799': df.loc[(df['FICO_SCORE'] >= 700) & (df['FICO_SCORE'] < 799)],
            '>= 800': df.loc[df['FICO_SCORE'] >= 800]
        }
        return strata

