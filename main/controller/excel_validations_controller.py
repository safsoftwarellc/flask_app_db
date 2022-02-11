from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.service.excel_db_service import (save_excel_info, update_excel_info, 
                                            get_excel_info, remove_excel_info,
                                            get_all_excel_info, save_db_table_excel_sheet_mapping_info, 
                                            update_db_table_excel_sheet_mapping_info,
                                            get_db_table_excel_sheet_mapping_info, 
                                            remove_db_table_excel_sheet_mapping_info,
                                            get_all_db_table_excel_sheet_mapping_info,
                                            save_json_path_data_info,remove_json_path_data_info,
                                            get_json_path_data_info,get_all_json_path_data_info)
from main.service.xml_db_service import (get_all_xpaths_for_file)
from main.util.validation_util import (validate_database_info, get_data_from_sheet, validate_xml_info, validate_json_info)
from io import BytesIO, StringIO, TextIOWrapper
import json
import lxml.etree as ET

excel_validations_app = Blueprint('excel_validations_app', __name__)

@excel_validations_app.route('/validationExcelFile', methods=['POST', 'PUT'])
def saveValidationExcelFile():
    if 'excel_file' not in request.files:
        return jsonify({'status':'"excel_file" not found!'})
    excel_file=request.files['excel_file']
    if excel_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif excel_file:
        s_filename=secure_filename(excel_file.filename)
        if request.method == 'PUT':
            return jsonify(update_excel_info(s_filename, excel_file))
        else:
            return jsonify(save_excel_info(s_filename, excel_file))
    else:
        return jsonify({'status':'unknown error!'})

@excel_validations_app.route('/validationExcelFile', methods=['GET'])
def getValidationExcelFile():
    file_name=request.args.get('excel_file_name')
    file_info =  get_excel_info(file_name)
    return send_file(BytesIO(file_info.excel_file_data), attachment_filename=file_name, as_attachment=True)

@excel_validations_app.route('/validationExcelFile', methods=['DELETE'])
def removeValidationExcelFile():
    file_name=request.args.get('excel_file_name')
    return jsonify(remove_excel_info(file_name))

@excel_validations_app.route('/getValidationExcelFileInfo', methods=['GET'])
def getValidationExcelFileInfo():
    file_name=request.args.get('excel_file_name')
    file_info =  get_excel_info(file_name)

    return jsonify({
        'file_id':file_info.data_id,
        'file_name':file_info.excel_file_name,
        'update_date':file_info.update_date
    })

@excel_validations_app.route('/getAllValidationExcelFilesInfo', methods=['GET'])
def getAllValidationExcelFilesInfo():
    all_files_info =  get_all_excel_info()
    files_info = {}
    for file_data in all_files_info:
        files_info[file_data.data_id]={
        'file_id':file_data.data_id,
        'file_name':file_data.excel_file_name,
        'update_date':file_data.update_date}

    return jsonify({'all files':files_info})



@excel_validations_app.route('/excelSheetDBTableMappingInfo', methods=['POST', 'PUT'])
def saveExcelSheetDBTableMappingInfo():
    mapping_data = request.get_json()
    file_name=request.args.get('excel_file_name')
    
    if file_name=='':
        return jsonify({'status':'file info not provided!'})
    
    if request.method == 'PUT':
        return jsonify(update_db_table_excel_sheet_mapping_info(file_name, mapping_data))
    else:
        return jsonify(save_db_table_excel_sheet_mapping_info(file_name, mapping_data))
    
    
@excel_validations_app.route('/excelSheetDBTableMappingInfo', methods=['DELETE'])
def removeExcelSheetDBTableMappingInfo():
    file_name=request.args.get('excel_file_name')
    return jsonify(remove_db_table_excel_sheet_mapping_info(file_name))

@excel_validations_app.route('/excelSheetDBTableMappingInfo', methods=['GET'])
def getExcelSheetDBTableMappingInfo():
    file_name=request.args.get('excel_file_name')
    mapping_info =  get_db_table_excel_sheet_mapping_info(file_name)

    return jsonify({
        'id':mapping_info.id,
        'excel_id':mapping_info.excel_id,
        'table_mapping':mapping_info.table_mapping,
        'update_date':mapping_info.update_date
    })

@excel_validations_app.route('/getAllExcelSheetDBTableMappingInfo', methods=['GET'])
def getAllExcelSheetDBTableMappingInfo():
    all_mapping_info =  get_all_db_table_excel_sheet_mapping_info()
    mapping_info = {}
    for mapping_data in all_mapping_info:
        mapping_info[mapping_data.id]={
        'id':mapping_data.id,
        'excel_id':mapping_data.excel_id,
        'table_mapping':mapping_data.table_mapping,
        'update_date':mapping_data.update_date}

    return jsonify({'all data':mapping_info})

@excel_validations_app.route('/JSONPathInfo', methods=['POST', 'PUT'])
def saveJSONPathDataInfo():
    json_path_mapping = request.get_json()
    file_name=request.args.get('json_file_name')
    
    if file_name=='':
        return jsonify({'status':'file info not provided!'})
    
    return jsonify(save_json_path_data_info(file_name, json_path_mapping))
    
    
@excel_validations_app.route('/JSONPathInfo', methods=['DELETE'])
def removeJSONPathDataInfo():
    file_name=request.args.get('json_file_name')
    return jsonify(remove_json_path_data_info(file_name))

@excel_validations_app.route('/JSONPathInfo', methods=['GET'])
def getJSONPathDataInfo():
    file_name=request.args.get('json_file_name')
    all_json_paths =  get_json_path_data_info(file_name)
    
    if (all_json_paths is None) or all_json_paths.count()==0:
        return {'status':'File not found in system!'}
    all_json_recors = []
    for json_path_record in all_json_paths:
        all_json_recors.append(json_path_record.json_path_string, json_path_record.json_path_name)
        
    return jsonify({file_name:all_json_recors})


@excel_validations_app.route('/getValidationDataForTestCaseRowRef', methods=['GET'])
def getValidationDataForTestCaseRowRef():
    file_name=request.args.get('excel_file_name')
    file_info =  get_excel_info(file_name)
    df = get_data_from_sheet(BytesIO(file_info.excel_file_data), sheet_name = 'Sheet2')
    print(df)
    return jsonify({'all files':"Done"})

@excel_validations_app.route('/validateTestInDatabase', methods=['GET'])
def validateTestInDatabase():
    excel_file_name=request.args.get('excel_file_name')
    test_case_name=request.args.get('test_case_name')
    row_ref=request.args.get('row_ref')
    file_sheets=request.args.get('validation_sheets')
    db_name=request.args.get('db_name')
    test_data=request.args.get('test_data')
    
    excel_file_info =  get_excel_info(excel_file_name)
    
    #file_sheet_table_mapping_json = json.loads(file_sheet_table_mapping)
    mapping_info =  get_db_table_excel_sheet_mapping_info(excel_file_name)
    file_sheet_table_mapping_json = mapping_info.table_mapping
    
    test_data_json = json.loads(test_data)

    final_test_results = validate_database_info(test_case_name, row_ref,
                           BytesIO(excel_file_info.excel_file_data),
                           file_sheets, file_sheet_table_mapping_json, db_name, test_data_json)
    
    return jsonify(final_test_results)

@excel_validations_app.route('/validateExcelDataWithXMLData', methods=['GET'])
def validateExcelDataWithXMLData():
    excel_file_name=request.args.get('excel_file_name')
    excel_file_sheet=request.args.get('excel_file_sheet')
    test_case_name=request.args.get('test_case_name')
    row_ref=request.args.get('row_ref')
    xml_template_name=request.args.get('xml_template_name')
    test_data=request.args.get('test_data')
    xml_data = request.get_data()
    
    root = ET.fromstring(xml_data)
    
    test_data_json = json.loads(test_data)
    
    excel_file_info =  get_excel_info(excel_file_name)
    xpaths_dict = get_all_xpaths_for_file(xml_template_name)
    
    final_test_results = validate_xml_info(root, xpaths_dict, 
                                           test_case_name, row_ref, 
                                           BytesIO(excel_file_info.excel_file_data),
                                           excel_file_sheet, test_data_json)
    return jsonify(final_test_results)
    #return jsonify({'a':'aa'})

@excel_validations_app.route('/validateExcelDataWithJSONData', methods=['GET'])
def validateExcelDataWithJSONData():
    json_file_name=request.args.get('json_file_name')
    excel_file_name=request.args.get('excel_file_name')
    excel_file_sheet=request.args.get('excel_file_sheet')
    test_case_name=request.args.get('test_case_name')
    row_ref=request.args.get('row_ref')
    test_data=request.args.get('test_data')
    json_data = request.get_json()
    
    test_data_json = json.loads(test_data)
    
    excel_file_info =  get_excel_info(excel_file_name)
    
    json_path_data_info =  get_json_path_data_info(json_file_name)

    final_test_results = validate_json_info(json_data, json_path_data_info, 
                                            test_case_name, row_ref, 
                                            BytesIO(excel_file_info.excel_file_data), 
                                            excel_file_sheet, test_data_json)
    
    return jsonify(final_test_results)









