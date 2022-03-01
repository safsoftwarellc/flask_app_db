from flask import Blueprint, request, jsonify
import pandas
import lxml.etree as ET
from io import BytesIO
from main.util.xml_util import (get_updated_xml)
from main.util.test_scripts_util import (prepare_xml, 
                                         post_to_mq, 
                                         validateTestInDatabase, 
                                         validateExcelDataWithXMLData,
                                         validateExcelDataWithJSONData)
from main.service.xml_db_service import (get_xml_data, get_all_xpaths_for_file)
from main.service.queue_db_service import (get_queue_info)
from main.service.excel_db_service import (get_excel_info)


test_scripts_app = Blueprint('test_scripts_app', __name__)

@test_scripts_app.route('/PostToMQAnXMLAndValidateInDB', methods=['POST'])
def PostToMQAnXMLAndValidateInDB():
    #Template Name  #Test Data  #MQ details
    #Cert Info      #DB Info    # Validation Excel
    #Prepare XML    #Submit MQ  # Validate in DB
    xmlfile_name=request.args.get('xmlfile_name')
    test_data_file_name=request.args.get('test_data_file_name')
    test_data_file_sheet_name=request.args.get('test_data_file_sheet_name')
    test_data_file_query=request.args.get('test_data_file_query')

    queue_name=request.args.get('queue_name')
    keystore_file_name=request.args.get('keystore_file_name')
    truststore_file_name=request.args.get('truststore_file_name')
    messageProperties=request.args.get('messageProperties')
    
    validation_excel_file_name=request.args.get('validation_excel_file_name')
    validation_excel_file_sheets=request.args.get('validation_excel_file_sheets')
    test_case_name=request.args.get('test_case_name')
    row_ref=request.args.get('row_ref')
    db_name=request.args.get('validation_db_name')
    validation_test_data=request.args.get('validation_test_data')
    
    #Prepare XML
    test_data_excel_file_info =  get_excel_info(test_data_file_name)
    df = pandas.read_excel(BytesIO(test_data_excel_file_info.excel_file_data), 
                           sheet_name = test_data_file_sheet_name, dtype='object')
    test_case_data = df.query(test_data_file_query)
    records_list = test_case_data.to_dict(orient='records')
    
    message_str = prepare_xml(xmlfile_name, records_list[0])
    
    #Post to MQ
    post_to_mq(message_str, queue_name, messageProperties, 
               keystore_file_name, truststore_file_name)


    #Validate in DB
    final_test_results = validateTestInDatabase(validation_excel_file_name, test_case_name, row_ref, 
                           validation_excel_file_sheets, db_name, validation_test_data)
    
    return jsonify(final_test_results)
    


@test_scripts_app.route('/PostMultipleToMQAnXMLAndValidateInDB', methods=['POST'])
def PostMultipleToMQAnXMLAndValidateInDB():
    xmlfile_name=request.args.get('xmlfile_name')
    test_data_file_name=request.args.get('test_data_file_name')
    test_data_file_sheet_name=request.args.get('test_data_file_sheet_name')
    test_data_file_query=request.args.get('test_data_file_query')

    queue_name=request.args.get('queue_name')
    keystore_file_name=request.args.get('keystore_file_name')
    truststore_file_name=request.args.get('truststore_file_name')
    messageProperties=request.args.get('messageProperties')
    
    validation_excel_file_name=request.args.get('validation_excel_file_name')
    validation_excel_file_sheets=request.args.get('validation_excel_file_sheets')
    #test_case_name=request.args.get('test_case_name')
    #row_ref=request.args.get('row_ref')
    db_name=request.args.get('validation_db_name')
    validation_test_data=request.args.get('validation_test_data')
    
    #Prepare XML
    test_data_excel_file_info =  get_excel_info(test_data_file_name)
    df = pandas.read_excel(BytesIO(test_data_excel_file_info.excel_file_data), 
                           sheet_name = test_data_file_sheet_name, dtype='object')
    test_case_data = df.query(test_data_file_query)
    records_list = test_case_data.to_dict(orient='records')
    
    all_TCs_final_test_results = {}
    
    for record in records_list:
        test_case_name = record['TestCaseName']
        row_ref = record['Validation_row_ref']
        
        #Prepare XML
        message_str = prepare_xml(xmlfile_name, record)
        
        #Post to MQ
        post_to_mq(message_str, queue_name, messageProperties, 
                keystore_file_name, truststore_file_name)
    
        #Validate in DB
        final_test_results = validateTestInDatabase(validation_excel_file_name, 
                                                    test_case_name, row_ref, 
                            validation_excel_file_sheets, db_name, validation_test_data)
        
        all_TCs_final_test_results[test_case_name]=final_test_results

    return jsonify(all_TCs_final_test_results)
    


