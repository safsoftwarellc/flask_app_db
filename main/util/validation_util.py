import pandas
from main.service.sql_db_service import get_data_from_DB

def validate_database_info(test_case_name, row_ref, excel_file_data, 
                           file_sheets, file_sheet_table_mapping_json, db_name):
    
    file_sheets_list = None
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
                db_data = get_data_from_DB(db_name, sqlQuery)
                
                #Validate DB data vs Excel Data
                if len(db_data)>1:
                    return "More records"
                db_record = db_data[0]
                for k, v in record.items():
                    if not check_excel_field_ignored(k):
                        if compare_data_as_string(v, db_record[k]):
                            print(f"{k} column data - {v} Passed")
                        else:
                            print(f"{k} column data - expected is {v} actual is {db_record[k]}")
                return "All are Tested"
                
                
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

def compare_data_as_string(expected, actual):
    if expected is actual:
        return True
    return False
    
