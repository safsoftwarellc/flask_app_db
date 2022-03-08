from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.service.message_db_service import (save_message_data_info, update_message_data_info,
                                             remove_message_data_info, get_message_data_info,
                                             get_all_message_data_info,
                                             save_message_text_data_info,
                                             update_message_text_data_info,
                                             remove_message_text_data_info,
                                             get_message_text_data_info, get_all_message_text_data_info)
from io import BytesIO

message_app = Blueprint('message_app', __name__)

@message_app.route('/message_file', methods=['POST', 'PUT'])
def save_message_file_data_info():
    if 'message_file' not in request.files:
        return jsonify({'status':'"message_file" not found!'})
    message_file=request.files['message_file']
    if message_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif message_file:
        s_filename=secure_filename(message_file.filename)
        if request.method == 'PUT':
            return jsonify(update_message_data_info(s_filename, message_file))
        else:
            return jsonify(save_message_data_info(s_filename, message_file))
    else:
        return jsonify({'status':'unknown error!'})

@message_app.route('/message_file', methods=['GET'])
def get_message_file_data_file():
    file_name=request.args.get('message_file_name')
    file_info =  get_message_data_info(file_name)
    return send_file(BytesIO(file_info.file_data), 
                     attachment_filename=file_name, 
                     as_attachment=True)


@message_app.route('/message_file', methods=['DELETE'])
def remove_message_file_data():
    file_name=request.args.get('message_file_name')
    return jsonify(remove_message_data_info(file_name))

@message_app.route('/message_file_info', methods=['GET'])
def get_message_file_data_info():
    file_name=request.args.get('message_file_name')
    file_info =  get_message_data_info(file_name)

    return jsonify({
        'file_id':file_info.file_id,
        'file_name':file_info.file_name,
        'update_date':file_info.update_date
    })

@message_app.route('/get_all_message_file_info', methods=['GET'])
def get_all_message_file_data_info():
    all_files_info =  get_all_message_data_info()
    files_info = {}
    for file_data in all_files_info:
        files_info[file_data.file_id]={
        'file_id':file_data.file_id,
        'file_name':file_data.file_name,
        'update_date':file_data.update_date}

    return jsonify({'all files':files_info})


@message_app.route('/message_text', methods=['POST', 'PUT'])
def save_message_text_data_info():
    file_name=request.args.get('message_file_name')
    header_text=request.args.get('header_text')
    footer_text=request.args.get('footer_text')
    line_1=request.args.get('line_1')
    line_2=request.args.get('line_2')
    line_3=request.args.get('line_3')
    line_4=request.args.get('line_4')
    line_5=request.args.get('line_5')
    line_6=request.args.get('line_6')
    line_7=request.args.get('line_7')
    line_8=request.args.get('line_8')
    line_9=request.args.get('line_9')
    line_10=request.args.get('line_10')
    
    if request.method == 'PUT':
        return jsonify(update_message_text_data_info(file_name, header_text, footer_text, 
                                                     line_1, line_2, line_3, line_4, line_5,
                                                     line_6, line_7, line_8, line_9, line_10))
    else:
        return jsonify(save_message_text_data_info(file_name, header_text, footer_text, 
                                                     line_1, line_2, line_3, line_4, line_5,
                                                     line_6, line_7, line_8, line_9, line_10))

    
@message_app.route('/message_text', methods=['GET'])
def get_message_text_data():
    file_name=request.args.get('message_file_name')
    file_info =  get_message_text_data_info(file_name)

    return jsonify({
        'file_id':file_info.file_id,
        'file_name':file_info.file_name,
        'header_text':file_info.header_text,
        'footer_text':file_info.footer_text,
        'line_1':file_info.line_1,
        'line_2':file_info.line_2,
        'line_3':file_info.line_3,
        'line_4':file_info.line_4,
        'line_5':file_info.line_5,
        'line_6':file_info.line_6,
        'line_7':file_info.line_7,
        'line_8':file_info.line_8,
        'line_9':file_info.line_9,
        'line_10':file_info.line_10,
        'update_date':file_info.update_date
    })

@message_app.route('/message_text', methods=['DELETE'])
def remove_message_text_data():
    file_name=request.args.get('message_file_name')
    return jsonify(remove_message_text_data_info(file_name))

@message_app.route('/get_all_message_text_info', methods=['GET'])
def get_all_message_text_data():
    all_files_info =  get_all_message_text_data_info()
    files_info = {}
    for file_data in all_files_info:
        files_info[file_data.file_id]={
        'file_id':file_data.file_id,
        'file_name':file_data.file_name,
        'header_text':file_data.header_text,
        'footer_text':file_data.footer_text,
        'line_1':file_data.line_1,
        'line_2':file_data.line_2,
        'line_3':file_data.line_3,
        'line_4':file_data.line_4,
        'line_5':file_data.line_5,
        'line_6':file_data.line_6,
        'line_7':file_data.line_7,
        'line_8':file_data.line_8,
        'line_9':file_data.line_9,
        'line_10':file_data.line_10,
        'update_date':file_data.update_date}

    return jsonify({'all files':files_info})

