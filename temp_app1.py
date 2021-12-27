"""
    Data Frames
"""

import pandas

df = pandas.read_excel('Upload_Files/Validations.xlsx')
print(df)
"""
dict_excel_data = df.to_dict(orient='records')
for row in dict_excel_data:
    print(row)
"""