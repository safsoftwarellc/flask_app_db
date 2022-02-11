import pandas
import getpass
from main.service.sql_db_service import get_data_from_DB
from main.util.xml_util import split_xpath_full_string, get_namespace_info_from_xpaths
from jsonpath_ng import jsonpath, parse

def validate_database_info(test_case_name, row_ref, excel_file_data, 
                           file_sheets, file_sheet_table_mapping_json, db_name, test_data_json):
    
    file_sheets_list = None
    if file_sheets is not None:
        file_sheets_list = file_sheets.split(',')
    final_test_results = {}
    for sheet_name in file_sheets_list:
        table_results = []
        test_case_data = get_testcase_data_by_row_ref(excel_file_data, sheet_name.strip(), 
                                                      test_case_name, row_ref)
        if not test_case_data.empty:
            db_table_name = file_sheet_table_mapping_json[sheet_name.strip()]
            records_list = test_case_data.to_dict(orient='records')
            #print(rows_list)
            for record in records_list:
                record = replace_test_data_values(record, test_data_json)
                #Create Query for each record
                sqlQuery = None
                for k, v in record.items():
                    if not check_excel_field_ignored(k):
                        if sqlQuery is None:
                            sqlQuery = 'Select '+k
                        else:
                            sqlQuery = sqlQuery + ', '+k
                sqlQuery = sqlQuery + " from "+db_table_name+" where "+ record["AUTO_Where_Clause"]
                #print(sqlQuery)
                #Run in DB
                db_data = get_data_from_DB(db_name, sqlQuery)
                #print(db_data)
                
                #Validate DB data vs Excel Data
                if len(db_data)>1:
                    return "More records"
                db_record = db_data[0]
                for k, v in record.items():
                    if not check_excel_field_ignored(k):
                        if compare_data_as_string(v, db_record[k.lower()]):
                            table_results.append(f"(P) {k} column data - expected is [{v}] actual is [{db_record[k.lower()]}] Passed")
                        else:
                            table_results.append(f"(F) {k} column data - expected is [{v}] actual is [{db_record[k.lower()]}] failed")
        final_test_results[sheet_name] = table_results
    return final_test_results
                

def validate_xml_info(root, xpaths_dict, test_case_name, row_ref, 
                      excel_file_data, file_sheet_name, test_data_json):
    test_case_data = get_testcase_data_by_row_ref(excel_file_data, file_sheet_name.strip(), 
                                                  test_case_name, row_ref)
    final_test_results = {}
    xml_results = []
    records_list = test_case_data.to_dict(orient='records')
    record = replace_test_data_values(records_list[0], test_data_json)
    # get expected Data from excel 
    # replace data values with test data
    # Loop XPaths dict
    # find xpath in root
    # compare data
    ns_json = get_namespace_info_from_xpaths(xpaths_dict)
    all_xpaths = xpaths_dict['allXpaths']
    for xpath_full_string in all_xpaths:
        (xpath_name, xpath_string) = split_xpath_full_string(xpath_full_string)
        print(xpath_name)
        if xpath_name in record:
            xpath_value = record[xpath_name]
            if ns_json is None:
                for ele in root.xpath(xpath_string):
                    if compare_data_as_string(xpath_value, ele.text):
                        xml_results.append(f"(P) {xpath_string} data - expected is [{xpath_value}] actual is [{ele.text}] Passed")
                    else:
                        xml_results.append(f"(F) {xpath_string} data - expected is [{xpath_value}] actual is [{ele.text}] Failed")
            else:
                for ele in root.xpath(xpath_string, namespaces=ns_json):
                    if compare_data_as_string(xpath_value, ele.text):
                        xml_results.append(f"(P) {xpath_string} data - expected is [{xpath_value}] actual is [{ele.text}] Passed")
                    else:
                        xml_results.append(f"(F) {xpath_string} data - expected is [{xpath_value}] actual is [{ele.text}] Failed")
    
    final_test_results['xml_results'] = xml_results
    return final_test_results


def validate_json_info(json_data, json_data_column_mapping, test_case_name, row_ref, 
                       excel_file_data, file_sheet_name, test_data_json):
    test_case_data = get_testcase_data_by_row_ref(excel_file_data, file_sheet_name.strip(), 
                                                  test_case_name, row_ref)
    final_test_results = {}
    json_results = []
    records_list = test_case_data.to_dict(orient='records')
    record = replace_test_data_values(records_list[0], test_data_json)
    
    # Loop json_data_column_mapping
    # FInd JSON Path in json_data and get Value
    # compare
    for json_path_full_string in json_data_column_mapping:
        (json_path_name, json_path_string) = split_json_path_full_string(json_path_full_string)
        jsonpath_expr= parse(json_path_string)
        json_path_value_array = jsonpath_expr.find(json_data)
        json_path_value = json_path_value_array[0].value
        if json_path_name in record:
            json_path_excel_value = record[json_path_name]
            if compare_data_as_string(json_path_excel_value, json_path_value):
                json_results.append(f"(P) {json_path_string} data - expected is [{json_path_excel_value}] actual is [{json_path_value}] Passed")
            else:
                json_results.append(f"(F) {json_path_string} data - expected is [{json_path_excel_value}] actual is [{json_path_value}] Failed")

    final_test_results['json_results'] = json_results
    
    return final_test_results

                
def get_testcase_data_by_row_ref(excel_file_data, sheet_name, test_case_name, row_ref):
    df = pandas.read_excel(excel_file_data, sheet_name = sheet_name)
    return df.query("TestCaseName == '" + test_case_name +"' and AUTO_Row_Ref_Id == '"+row_ref+"'")

def get_data_from_sheet(excel_file_data, sheet_name):
    return pandas.read_excel(excel_file_data, sheet_name = sheet_name)

def check_excel_field_ignored(excel_field_name):
    list_of_auto_fields = ['TestCaseName', 'AUTO_Module_Name', 'AUTO_Row_Ref_Id', 'AUTO_Where_Clause']
    if excel_field_name in list_of_auto_fields:
        return True
    return False

def compare_data_as_string(expected, actual):
    if str(expected).upper().startswith('STARTS_WITH{') and str(actual).startswith(str(expected)[12:-1]):
        return True
    elif str(expected).upper().startswith('ENDS_WITH{') and str(actual).endswith(str(expected)[10:-1]):
        return True
    elif str(expected).upper().startswith('CONTAINS{') and str(actual).__contains__(str(expected)[9:-1]):
        return True
    elif str(expected).upper().startswith('OR{') and (str(actual) in [x.strip() for x in str(expected)[3:-1].split('|')]):
        return True
    elif str(expected).upper() == 'NOT_NULL' and check_string_is_null(actual) is False:
        return True
    elif str(expected).upper() == 'SYSTEM_USER' and str(actual).lower()==getpass.getuser().lower():
        return True
    elif str(expected).upper() == 'NOT_NULL_GREATER_THAN_ZERO':
        try:
            if int(actual)>0:
                return True
        except:
            return False
        return False
    elif check_string_is_null(expected) and check_string_is_null(actual):
        return True
    elif str(expected).upper() == 'NULL_VALUE' and str(actual).upper()=='NULL':
        return True
    elif str(expected).upper() == 'ANY_VALUE':
        return True
    elif str(expected) == str(actual):
        return True
    return False

def check_string_is_null(str_value):
    if str(str_value).lower().strip() == 'nan':
        return True
    elif str(str_value).lower().strip() == 'none':
        return True
    elif str(str_value).lower().strip() == 'null':
        return True
    elif str(str_value).lower().strip() == '':
        return True
    return False
        
def replace_test_data_values(test_case_data, test_data_json):
    for k, v in test_case_data.items():
        all_params_updated = False
        if v is not pandas.np.nan:
            string_value = str(v)
            startPostion = string_value.find('<')
            endPostion = -1
            while(all_params_updated==False):
                if startPostion>-1:
                    endPostion = string_value.find('>', startPostion+1)
                if startPostion>-1 and endPostion>startPostion:
                    parameter_name = string_value[startPostion+1:endPostion]
                    if parameter_name in test_data_json:
                        test_case_data[k]=string_value.replace(string_value[startPostion:endPostion+1], test_data_json[parameter_name])
                    startPostion = string_value.find('<', endPostion)                    
                else:
                    all_params_updated = True
    return test_case_data        
    
def split_json_path_full_string(json_path_full_string):
    lastIndex = json_path_full_string.rfind('-')
    xpath_name = json_path_full_string[lastIndex+1:].strip()
    xpath_string = json_path_full_string[:lastIndex].strip()
    return (xpath_name, xpath_string)