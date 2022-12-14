import pandas as pd
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod
from dataclasses import dataclass
import abstract
import streamlit as st
import plotly.express as px


class GetCommonColumns(abstract.AbstractGetCommonColumns):

    def find_columns_intersection(
            self, data_frame: pd.DataFrame, 
            pre_selected_columns: list):
        return list(set(data_frame.columns.to_list()).intersection(
                        pre_selected_columns))


class BasicDataFrameTrans(abstract.AbstractDataFrameTrans):

    def data_transform(
            self, data_frame: pd.DataFrame, 
            common_columns: list):
        data_frame = pd.DataFrame(
            data_frame[common_columns]).set_index('Time (s)')
        df_statistics = data_frame.describe().round(decimals=2)
        df_correlations = data_frame.corr().round(decimals=2)
        return data_frame, df_statistics, df_correlations


class BasicDataFrameToFile(abstract.AbstractDataFrameToFile):

    def save_df_to_file(
            self, 
            data_frame: pd.DataFrame, 
            df_stats: pd.DataFrame, 
            df_corr: pd.DataFrame ,
            source_file: str):
        excelWriter = pd.ExcelWriter(f'{source_file[:-5]}_report.xlsx')
        data_frame.to_excel(excelWriter, sheet_name= 'Temperatures')
        df_stats.to_excel(excelWriter, sheet_name= 'Temp_statistics')
        df_corr.to_excel(excelWriter, sheet_name= 'Temp_correlations')
        excelWriter.save()
        excelWriter.close()


class BasicDataFramePlot(abstract.AbstractDataFramePlot):

    def plot_graph(
            self, 
            data_frame: pd.DataFrame, 
            common_columns: list, 
            source_file: str):
        common_columns.remove('Time (s)')
        for _ in common_columns:
            plt.plot(data_frame.index.values.tolist(), data_frame[_].tolist())
        plt.savefig(f'{source_file[:-5]}_plot.png')
        #plt.show()
        

class TemperatureReport(abstract.Report):

    def __init__(
            self, path: str, source_file: str, 
            pre_selected_columns: list, sheet_name_: str, 
            plot_obj_method: abstract.AbstractDataFramePlot, 
            file_save_method: abstract.AbstractDataFrameToFile, 
            data_trans: abstract.AbstractDataFrameTrans, 
            post_selected_columns: abstract.AbstractGetCommonColumns):

        super().__init__(
            path, source_file, pre_selected_columns, 
            sheet_name_)
        self.plot_obj_method = plot_obj_method
        self.file_save_method = file_save_method
        self.data_trans = data_trans
        self.post_selected_columns = post_selected_columns

    def generate_report(self):
        self.__raw_df = CreateDataFrame.get_raw_df(
            self.path, self.source_file, 
            self.sheet_name)
        fig = px.line(self.__raw_df, x='Time (s)', y='Furnace (??C)', hover_data=['Time (s)', 'Furnace (??C)'], title="Raw Data Plot")
        st.write(fig)
        fig_all = px.line(self.__raw_df, x='Time (s)', y= self.pre_selected_columns, title="Raw AllData Plot")
        st.write(fig_all)

        
        common_columns = self.post_selected_columns.find_columns_intersection(
            self.__raw_df, 
            self.pre_selected_columns)

        self.df, self.df_corr, self.df_stats = self.data_trans.data_transform(
            self.__raw_df, 
            common_columns)

        self.file_save_method.save_df_to_file(
            self.df, self.df_stats, 
            self.df_corr, self.source_file)
                
        self.plot_obj_method.plot_graph(
            self.df, common_columns, 
            self.source_file)
        

        st.write(self.__raw_df)
        st.write(self.df)
       

class FurnanceTempReport(TemperatureReport):
    def generate_report(self):
        return super().generate_report()


class CreateDataFrame:
    @staticmethod
    def get_raw_df(
            path, source_file, 
            sheet_name_):
        URL_ADRES = f'{path}/{source_file}'
        return pd.read_excel(URL_ADRES, sheet_name= sheet_name_)



