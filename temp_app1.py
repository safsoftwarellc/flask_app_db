#import pandas

#df = pandas.read_excel('/Users/sunilduvvuru/Documents/git/flask_app_db/Upload_Files/Test_Data_Sample.xlsx',
#                       sheet_name='Data', dtype='object')
#print(df)

#records_list = df.to_dict(orient='records')
#print(records_list[0])


from email import message


line1_text = 'sfdfd'
line2_text = 'abcdddd'
line3_text = ''
line4_text = 'fhgjghjhg'
message_text = '' if not line1_text else (line1_text+'\n')
message_text = message_text+ ('' if not line2_text else (line2_text+'\n'))
message_text = message_text+ ('' if not line3_text else (line3_text+'\n'))
message_text = message_text+ ('' if not line4_text else (line4_text+'\n'))


print(message_text)