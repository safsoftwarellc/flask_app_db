import pandas

df = pandas.read_excel('/Users/sunilduvvuru/Documents/git/flask_app_db/Upload_Files/Test_Data_Sample.xlsx',
                       sheet_name='Data', dtype='object')
print(df)

records_list = df.to_dict(orient='records')
print(records_list[0])

