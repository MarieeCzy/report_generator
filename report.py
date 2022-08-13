import pandas as pd
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
from dataclasses import dataclass


#abstract methods:
class AbstractGetCommonColumns(ABC):
    @abstractmethod
    def find_columns_intersection(self, data_frame: pd.DataFrame, pre_selected_columns: list):
        pass

class AbstractDataFrameTrans(ABC):
    @abstractmethod
    def data_transform(self, data_frame: pd.DataFrame, common_columns: list):
        pass

class AbstractDataFrameToFile(ABC):
    @abstractmethod
    def save_df_to_file(self, data_frame: pd.DataFrame, df_stats: pd.DataFrame, df_corr: pd.DataFrame ,source_file: str):
        pass

class AbstractDataFramePlot(ABC):
    @abstractmethod
    def plot_graph(self, data_frame: pd.DataFrame, common_columns: list, source_file: str):
        pass
    


class GetCommonColumns(AbstractGetCommonColumns):
    def find_columns_intersection(self, data_frame: pd.DataFrame, pre_selected_columns: list):
        return list(set(
            data_frame.columns.to_list()).intersection(
                pre_selected_columns))


class BasicDataFrameTrans(AbstractDataFrameTrans):
    def data_transform(self, data_frame: pd.DataFrame, common_columns: list):
        data_frame = pd.DataFrame(data_frame[common_columns]).set_index('Time (s)')
        df_statistics = data_frame.describe().round(decimals=2)
        df_correlations = data_frame.corr().round(decimals=2)
        return data_frame, df_statistics, df_correlations


class BasicDataFrameToFile(AbstractDataFrameToFile):
    def save_df_to_file(self, data_frame: pd.DataFrame, df_stats: pd.DataFrame, df_corr: pd.DataFrame ,source_file: str):
        excelWriter = pd.ExcelWriter(f'{source_file[:-5]}_report.xlsx')
        data_frame.to_excel(excelWriter, sheet_name= 'Temperatures')
        df_stats.to_excel(excelWriter, sheet_name= 'Temp_statistics')
        df_corr.to_excel(excelWriter, sheet_name= 'Temp_correlations')
        excelWriter.save()
        excelWriter.close()


class BasicDataFramePlot(AbstractDataFramePlot):
    def plot_graph(self, data_frame: pd.DataFrame, common_columns: list, source_file: str):
        common_columns.remove('Time (s)')
        for _ in common_columns:
            plt.plot(data_frame.index.values.tolist(), data_frame[_].tolist())
        plt.savefig(f'{source_file[:-5]}_plot.png')
        #plt.show()
        
        

  

class Report(ABC):
    def __init__(self, path, source_file, pre_selected_columns, sheet_name_= 'Sec data'):
        self.path = path
        self.source_file = source_file
        self.pre_selected_columns = pre_selected_columns
        self.sheet_name = sheet_name_

    @abstractmethod
    def generate_report(self):
            pass


class TemperatureReport(Report):
    def __init__(self, path, source_file, pre_selected_columns, sheet_name_, plot_obj_method: AbstractDataFramePlot, file_save_method: AbstractDataFrameToFile, data_trans: AbstractDataFrameTrans, post_selected_columns: AbstractGetCommonColumns):
        super().__init__(path, source_file, pre_selected_columns, sheet_name_)
        self.plot_obj_method = plot_obj_method
        self.file_save_method = file_save_method
        self.data_trans = data_trans
        self.post_selected_columns = post_selected_columns

    def generate_report(self):
        self.__raw_df = CreateDataFrame.get_raw_df(self.path, self.source_file, self.sheet_name)
        
        common_columns = self.post_selected_columns.find_columns_intersection(self.__raw_df, self.pre_selected_columns)

        self.df, self.df_corr, self.df_stats = self.data_trans.data_transform(self.__raw_df, common_columns)

        self.file_save_method.save_df_to_file(self.df, self.df_stats, self.df_corr, self.source_file)
                
        self.plot_obj_method.plot_graph(self.df, common_columns, self.source_file)

class FurnanceTempReport(TemperatureReport):
    def generate_report(self):
        return super().generate_report()


class CreateDataFrame:
    @staticmethod
    def get_raw_df(path, source_file, sheet_name_):
        URL_ADRES = f'{path}/{source_file}'
        return pd.read_excel(URL_ADRES, sheet_name= sheet_name_)





