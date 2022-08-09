import pandas as pd
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod

class Report(ABC):
    def __init__(self, path, source_file, pre_selected_columns):
        self.URL_ADRES = ''
        self.path = path
        self.source_file = source_file
        self.raw_df = pd.DataFrame
        self.df = pd.DataFrame
        self.pre_selected_columns = pre_selected_columns
        self.post_selected_columns = []

        @abstractmethod
        def generate_report(self):
            pass


class TemperatureReport(Report):
    def __init__(self, path, source_file, pre_selected_columns):
        super().__init__(path, source_file, pre_selected_columns)

    def generate_report(self):
        data_frame = CreateDataFrame(self.path, self.source_file)
        self.raw_df = data_frame.get_raw_df()

        common_columns = GetCommonColumns(self.raw_df , self.pre_selected_columns)
        self.post_selected_columns = common_columns.find_columns_intersection()

        data_trans = DataFrameTrans(self.raw_df, self.post_selected_columns)
        data_trans.data_transform()
        self.df = data_trans.data_frame
        self.df_stats = data_trans.df_statistics
        self.df_corr = data_trans.df_correlations

        file_save = DataFrameToFile(self.df, self.df_stats, self.df_corr, self.source_file)
        file_save.save_df_to_file()
        
        plot_obj = DataFramePlot(self.df, self.post_selected_columns, self.source_file)
        plot_obj.plot_graph()

class FurnanceTempReport(TemperatureReport):
    def generate_report(self):
        return super().generate_report()


class CreateDataFrame():
    def __init__(self, path, source_file):
        self.path = path
        self.source_file = source_file
    
    def get_raw_df(self):
        self.URL_ADRES = f'{self.path}\{self.source_file}'
        return pd.read_excel(self.URL_ADRES, sheet_name= 'Sec data')
        

class GetCommonColumns:
    def __init__(self, data_frame, pre_selected_columns):
        self.data_frame = data_frame
        self.pre_selected_columns = pre_selected_columns

    def find_columns_intersection(self):
        return list(set(
            self.data_frame.columns.to_list()).intersection(
                self.pre_selected_columns))
 

class DataFrameTrans:
    def __init__(self, data_frame, common_columns):
        self.data_frame = data_frame
        self.common_columns = common_columns
    
    def data_transform(self):
        self.data_frame = pd.DataFrame(self.data_frame[self.common_columns]).set_index('Time (s)')
        self.df_statistics = self.data_frame.describe().round(decimals=2)
        self.df_correlations = self.data_frame.corr().round(decimals=2)


class DataFrameToFile:
    def __init__(self, data_frame, df_stats, df_corr ,source_file):
        self.df = data_frame
        self.df_statistics = df_stats
        self.df_correlations = df_corr
        self.source_file = source_file

    def save_df_to_file(self):
        excelWriter = pd.ExcelWriter(f'{self.source_file[:-5]}_report.xlsx')
        self.df.to_excel(excelWriter, sheet_name= 'Temperatures')
        self.df_statistics.to_excel(excelWriter, sheet_name= 'Temp_statistics')
        self.df_correlations.to_excel(excelWriter, sheet_name= 'Temp_correlations')
        excelWriter.save()
        excelWriter.close()

class DataFramePlot:
    def __init__(self, data_frame, common_columns, source_file):
        self.df = pd.DataFrame(data_frame)
        self.common_columns = common_columns
        self.source_file = source_file
    
    def plot_graph(self):
        self.common_columns.remove('Time (s)')
        for _ in self.common_columns:
            plt.plot(self.df.index.values.tolist(), self.df[_].tolist())
        plt.savefig(f'{self.source_file[:-5]}_plot.png')
        #plt.show()