from flask import flask, Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.service.excel_db_service import (save_excel_info, update_excel_info, 
                                            get_excel_info, remove_excel_info,
                                            get_all_excel_info)
from io import BytesIO

excel_validations_app = Blueprint('queue_app', __name__)

@excel_validations_app.route('/validationExcelFile', methods=['POST', 'PUT'])
def saveValidationExcelFile():
    if 'excel_file' not in request.files:
        return jsonify({'status':'"excel_file" not found!'})
    excel_file=request.files['excel_file']
    if excel_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif excel_file:
        s_filename=secure_filename(excel_file.filename)
        if flask.request.method == 'PUT':
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
        files_info[file_data.file_id]={
        'file_id':file_data.data_id,
        'file_name':file_data.excel_file_name,
        'update_date':file_data.update_date}

    return jsonify({'all files':files_info})
