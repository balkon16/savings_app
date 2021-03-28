import pandas as pd
import json

class FileParser:

    def __init__(self):
        pass

    def parse_excel(self, file_path):
        """

        Parameters
        ----------
        file_path

        Returns
        -------
        list of
        """
        df = pd.read_excel(file_path)
        # TODO: dokończyć -> jeden wiersz jeden słownik
