from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.service.queue_db_service import (save_certificate_info, get_certificate_info, 
                                        remove_certificate_info, update_certificate_info,
                                        save_queue_info, get_queue_info, delete_queue_info)
from io import BytesIO


queue_app = Blueprint('queue_app', __name__)


@queue_app.route('/certificate', methods=['POST'])
def saveCertificate():
    if 'cert_file' not in request.files:
        return jsonify({'status':'"cert_file" not found!'})
    cert_file=request.files['cert_file']
    if cert_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif cert_file:
        s_filename=secure_filename(cert_file.filename)
        save_certificate_info(s_filename, cert_file)
        return jsonify({'status':'File Saved Successfull!'})
    else:
        return jsonify({'status':'unknown error!'})

@queue_app.route('/certificate', methods=['PUT'])
def updateCertificate():
    if 'cert_file' not in request.files:
        return jsonify({'status':'"cert_file" not found!'})
    cert_file=request.files['cert_file']
    if cert_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif cert_file:
        s_filename=secure_filename(cert_file.filename)
        update_certificate_info(s_filename, cert_file)
        return jsonify({'status':'File Saved Successfull!'})
    else:
        return jsonify({'status':'unknown error!'})

@queue_app.route('/certificate', methods=['DELETE'])
def removeCertificate():
    file_name=request.args.get('cert_file_name')
    remove_certificate_info(file_name)
    return jsonify({'status':'{} Deleted'.format(file_name)})

@queue_app.route('/certificate', methods=['GET'])
def getCertificate():
    file_name=request.args.get('cert_file_name')
    file_info =  get_certificate_info(file_name)
    return send_file(BytesIO(file_info.file_data), attachment_filename=file_name, as_attachment=True)


@queue_app.route('/queueInformation', methods=['POST', 'PUT'])
def saveQueueInformation():
    config_data = request.get_json()
    queue_name=request.args.get('queue_name')
    return_stat = save_queue_info(queue_name, config_data)
    if return_stat:
        return jsonify({'status':'Information Saved for Queue - '+queue_name})
    return jsonify({'status':'Unknown issue for Queue '+queue_name})

@queue_app.route('/queueInformation', methods=['DELETE'])
def deleteQueueInformation():
    queue_name=request.args.get('queue_name')
    return_stat = delete_queue_info(queue_name)
    if return_stat:
        return jsonify({'status':'Information Deleted for Queue - '+queue_name})
    return jsonify({'status':'Unknown issue while deleting information for Queue '+queue_name})

@queue_app.route('/queueInformation', methods=['GET'])
def getQueueInformation():
    queue_name=request.args.get('queue_name')
    return jsonify(get_queue_info(queue_name))


