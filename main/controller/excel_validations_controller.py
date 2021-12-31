from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.service.excel_db_service import (save_excel_info, update_excel_info, 
                                            get_excel_info, remove_excel_info,
                                            get_all_excel_info)
from main.util.validation_util import validate_database_info, get_data_from_sheet
from io import BytesIO
import json

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
    file_sheet_table_mapping=request.args.get('validation_sheets_table_mapping')
    db_name=request.args.get('db_name')
    test_data=request.args.get('test_data')
    
    excel_file_info =  get_excel_info(excel_file_name)
    
    file_sheet_table_mapping_json = json.loads(file_sheet_table_mapping)
    test_data_json = json.loads(test_data)

    final_test_results = validate_database_info(test_case_name, row_ref,
                           BytesIO(excel_file_info.excel_file_data),
                           file_sheets, file_sheet_table_mapping_json, db_name, test_data_json)
    
    return jsonify(final_test_results)

