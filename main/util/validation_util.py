import pandas

def validate_database_info(test_case_name, row_ref, excel_file_data, 
                           file_sheets, file_sheet_table_mapping_json, db_name):
    
    file_sheets_list = None
    file_sheet_table_mapping_list = None
    if file_sheets is not None:
        file_sheets_list = file_sheets.split(',')
        
    for sheet_name in file_sheets_list:
        test_case_data = get_testcase_data_by_row_ref(excel_file_data, sheet_name.strip(), test_case_name, row_ref)
        if not test_case_data.empty:
            db_table_name = file_sheet_table_mapping_json[sheet_name.strip()]
            records_list = test_case_data.to_dict(orient='records')
            #print(rows_list)
            for record in records_list:
                #Create Query for each record
                sqlQuery = None
                for k, v in record.items():
                    if not check_excel_field_ignored(k):
                        if sqlQuery is None:
                            sqlQuery = 'Select '+k
                        else:
                            sqlQuery = sqlQuery + ', '+k
                sqlQuery = sqlQuery + " from "+db_table_name+" where "+ record["AUTO_WhereCondition"]
                print(sqlQuery)
                #Run in DB
                
                #Validate DB data vs Excel Data
                """for k, v in row.items():
                    print(k, v)"""
                
def get_testcase_data_by_row_ref(excel_file_data, sheet_name, test_case_name, row_ref):
    df = pandas.read_excel(excel_file_data, sheet_name = sheet_name)
    return df.query("TestCaseName == '" + test_case_name +"' and AUTO_Row_Ref == '"+row_ref+"'")

def get_data_from_sheet(excel_file_data, sheet_name):
    return pandas.read_excel(excel_file_data, sheet_name = sheet_name)

def check_excel_field_ignored(excel_field_name):
    list_of_auto_fields = ['TestCaseName', 'AUTO_Module', 'AUTO_Row_Ref', 'AUTO_WhereCondition']
    if excel_field_name in list_of_auto_fields:
        return True
    return False
