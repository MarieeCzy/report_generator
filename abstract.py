import pandas as pd
from abc import ABC, abstractmethod
from dataclasses import dataclass


#abstract methods:
class AbstractGetCommonColumns(ABC):
    @abstractmethod
    def find_columns_intersection(
            self, data_frame: pd.DataFrame, 
            pre_selected_columns: list):
        pass


class AbstractDataFrameTrans(ABC):
    @abstractmethod
    def data_transform(
            self, data_frame: pd.DataFrame, 
            common_columns: list):
        pass


class AbstractDataFrameToFile(ABC):
    @abstractmethod
    def save_df_to_file(
            self, data_frame: pd.DataFrame, 
            df_stats: pd.DataFrame, 
            df_corr: pd.DataFrame ,
            source_file: str):
        pass


class AbstractDataFramePlot(ABC):
    @abstractmethod
    def plot_graph(
            self, data_frame: pd.DataFrame, 
            common_columns: list, 
            source_file: str):
        pass
    

class Report(ABC):
    def __init__(
            self, path: str, source_file: str, 
            pre_selected_columns: list, 
            sheet_name_= 'Sec data'):
        self.path = path
        self.source_file = source_file
        self.pre_selected_columns = pre_selected_columns
        self.sheet_name = sheet_name_

    @abstractmethod
    def generate_report(self):
            pass
