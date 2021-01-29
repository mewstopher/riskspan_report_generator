from riskspan_report_generator.exceptions import DataShapeError,\
    FileExtensionError,\
    SheetNameError
from pathlib import Path
import pandas as pd
import logging


class DataLoader:
    def __init__(self, data_file: str, sheet_name: str):
        self.logger = logging.getLogger(__name__)
        self.logger.debug(f'{__name__} entered')
        self.data_file = data_file
        self.sheet_name = sheet_name

    def validate_shape(self, df: pd.DataFrame):
        """
        Check if the shape of the input data
        matches up to the expected number of
        rows and columns
        """
        self.logger.info("Checking shape of input data")
        num_rows = df.shape[0]
        num_cols = df.shape[1]
        if num_rows != 2000:
            self.logger.error(f'The number of rows is {num_rows}. Expecting 2000. '
                              'Check your data input file and try again.')
            raise DataShapeError
        elif num_cols != 30:
            self.logger.error(f'The number of columns is {num_cols}. Expecting 30. '
                              'Check your data input file and try again.')
            raise DataShapeError
        else:
            self.logger.info("Data File has correct number of rows and columns")
        return

    def check_file_exists(self):
        """
        check if file physically exists in specified location
        """
        self.logger.info("Checking if file exists.")
        file_path = Path(self.data_file).absolute().exists()
        if not file_path:
            self.logger.error('Data file not found. Check the path/file spelling and try again')
            raise FileNotFoundError
        return

    def check_ext(self):
        """
        check if the file extension matches to
        expected format of: .XLSX
        """
        self.logger.info('Checking file Extension')
        file_extension = Path(self.data_file).suffix.lower()
        if file_extension != '.xlsx':
            self.logger.error(f'Expected file of type: .XLSX, got: {file_extension}. '
                              'Change the file extension or select a different file')
            raise FileExtensionError
        return

    def extract_df(self) -> pd.DataFrame:
        """
        Extracts dataframe from XLSX file bundle.

        OUTPUT
        -------
        df: pd.DataFrame
            data frame containing loan data
        """
        self.check_file_exists()
        self.check_ext()
        excel_file = pd.ExcelFile(self.data_file)
        if self.sheet_name not in excel_file.sheet_names:
            self.logger.error('Sheet name not found in file.')
            raise SheetNameError
        df = excel_file.parse(self.sheet_name)
        self.validate_shape(df)
        return df
