import lxml.etree as ET
from io import BytesIO, StringIO
from main.util.xml_util import (get_updated_xml)
from main.service.xml_db_service import (get_xml_data, get_all_xpaths_for_file)
from main.service.queue_db_service import (get_certificate_info, get_queue_info)
import requests
import json
import ast
from main.service.excel_db_service import (get_excel_info, 
                                           get_db_table_excel_sheet_mapping_info, 
                                           get_json_path_data_info)
from main.service.message_db_service import (get_message_data_info)
from main.util.validation_util import (validate_database_info, validate_xml_info, 
                                       validate_json_info)

def prepare_xml(xmlfile_name, json_data):
    file_info = get_xml_data(xmlfile_name)
    all_xpaths_json = get_all_xpaths_for_file(xmlfile_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    
    root = get_updated_xml(root, all_xpaths_json, json_data)
    if root is None:
        return None
    str = ET.tostring(root, pretty_print=True)
    return str

def post_to_mq(message_str, queue_name, messageProperties, 
               keystore_file_name, truststore_file_name):
    queue_info = get_queue_info(queue_name)
    queue_info['messageProperties']=messageProperties
    
    keystore_file =  get_certificate_info(keystore_file_name)
    truststore_file =  get_certificate_info(truststore_file_name)
    
    queue_info['keyStorePwd']=keystore_file.file_password
    queue_info['trustStorePwd']=truststore_file.file_password
    queue_info['messageText']=message_str
    
    files={
        'keyStoreFile': keystore_file.file_data,
        'trustStoreFile': truststore_file.file_data
    }
    
    res = requests.post('http://localhost:8080/rest/mq/postTextMessage',
        data=queue_info, files=files)
    
    return {'Status':res.text}

def validateTestInDatabase(excel_file_name, test_case_name, row_ref, 
                           file_sheets, db_name, test_data):
    
    excel_file_info =  get_excel_info(excel_file_name)
    
    #file_sheet_table_mapping_json = json.loads(file_sheet_table_mapping)
    mapping_info =  get_db_table_excel_sheet_mapping_info(excel_file_info.data_id)
    file_sheet_table_mapping_json = ast.literal_eval(mapping_info.table_mapping)
    
    test_data_json = json.loads(test_data)

    final_test_results = validate_database_info(test_case_name, row_ref,
                           BytesIO(excel_file_info.excel_file_data),
                           file_sheets, file_sheet_table_mapping_json, db_name, test_data_json)
    
    return final_test_results

def validateExcelDataWithXMLData(excel_file_name, excel_file_sheet, 
                                 test_case_name, row_ref, xml_template_name,
                                 test_data, xml_data):
    
    root = ET.fromstring(xml_data)
    
    test_data_json = json.loads(test_data)
    
    excel_file_info =  get_excel_info(excel_file_name)
    xpaths_dict = get_all_xpaths_for_file(xml_template_name)
    
    final_test_results = validate_xml_info(root, xpaths_dict, 
                                           test_case_name, row_ref, 
                                           BytesIO(excel_file_info.excel_file_data),
                                           excel_file_sheet, test_data_json)
    return final_test_results

def validateExcelDataWithJSONData(json_file_name, excel_file_name, excel_file_sheet,
                                  test_case_name, row_ref, test_data, json_data):
    
    test_data_json = json.loads(test_data)
    
    excel_file_info =  get_excel_info(excel_file_name)
    
    json_path_data_info =  get_json_path_data_info(json_file_name)
    
    if (json_path_data_info is None) or json_path_data_info.count()==0:
        return {'status':'File not found in system!'}
    all_json_path_records = []
    for json_path_record in json_path_data_info:
        all_json_path_records.append(json_path_record.json_path_string + "-" +json_path_record.json_path_name)
        

    final_test_results = validate_json_info(json_data, all_json_path_records, 
                                            test_case_name, row_ref, 
                                            BytesIO(excel_file_info.excel_file_data), 
                                            excel_file_sheet, test_data_json)
    
    return final_test_results

def prepare_message_from_file(message_file_name, json_data):
    file_info = get_message_data_info(message_file_name)
    b = BytesIO(file_info.file_data)
    message_string = b.getvalue()
    for text_ele, text_val in json_data:
        message_string = message_string.replace('${'+text_ele+'}', text_val)
    return message_string