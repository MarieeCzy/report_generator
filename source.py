import files_list, report, pandas as pd

sheet_name_ = 'Sec data'
path = 'source-files'
temp_pre_selected_columns = ['Time (s)', 'Furnace (ºC)', 'Tf0 (ºC)', 'Tf1 (ºC)', 'Tf2 (ºC)',
       'Tf3 (ºC)', 'Ambient (ºC)', 'Orifice (ºC)',
       'T1[max] (ºC)', 'T2[max] (ºC)', 'T3[max] (ºC)', 'T4[max] (ºC)',
       'T5[max] (ºC)', 'T6[max] (ºC)', 'T7[max] (ºC)', 'T8[max] (ºC)',
       'T9[max] (ºC)', 'T10[max] (ºC)', 'T11[max] (ºC)', 'T12[max] (ºC)',
       'T13[max][avg] (ºC)', 'T14[max][avg] (ºC)', 'T15[max][avg] (ºC)',
       'T16[max][avg] (ºC)']

temp_furnance_pre_selected_columns = ['Time (s)', 'Furnace (ºC)', 'Tf0 (ºC)', 'Tf1 (ºC)', 'Tf2 (ºC)',
       'Tf3 (ºC)']

def main():
       example = files_list.SourceFilesList(path)
       example.files_selector()
       for _ in example.xlsx_files:
              temp_report = report.TemperatureReport(path,
                                                     _, 
                                                     temp_pre_selected_columns, 
                                                     sheet_name_, report.BasicDataFramePlot(), 
                                                     report.BasicDataFrameToFile(), 
                                                     report.BasicDataFrameTrans(), 
                                                     report.GetCommonColumns())
              temp_report.generate_report()
       print(temp_report.__raw_df)
        #temp_furnance_rep = report.FurnanceTempReport(path, _, temp_furnance_pre_selected_columns)
        #temp_furnance_rep.generate_report()
        
main()
