from riskspan_report_generator.generators import ReportGenerator, Report
import pandas as pd


class LenderReport(Report):

    @property
    def stratum_names(self):
        strata = ['Bank Owned Mortgage Company - National',
                  'Mortgage Banker - Bank Owned', 'Mortgage Banker - (Large)',
                  'Credit Unions', 'Community Banks']
        return strata

    def get_strata(self, df: pd.DataFrame) -> dict:
        strata = {}
        for stratum in self.stratum_names:
            strata[stratum] = df.loc[df['LENDER_INST_TYPE_DESCRIPTION'] == stratum]
        return strata


class LtvReport(Report):
    @property
    def stratum_names(self):
        strata = ['<= 85%', '>85% and <= 90%', '>90% and <= 95%', '>95%']
        return strata

    def get_strata(self, df):
        strata = {'<= 85%': df.loc[df['LTV'] <= 85],
                  '>85% and <= 90%': df.loc[(df['LTV'] > 85) & (df['LTV'] <= 90)],
                  '>90% and <= 95%': df.loc[(df['LTV'] > 90) & (df['LTV'] <= 95)],
                  '>95%': df.loc[df['LTV'] > 95]}
        return strata


class LenderGenerator(ReportGenerator):
    def report_factory(self):
        return LenderReport()


class LtvGenerator(ReportGenerator):
    def report_factory(self):
        return LtvReport()
