from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from main.service.queue_db_service import (save_certificate_info, get_certificate_info, 
                                        remove_certificate_info, get_all_queue_info,
                                        save_queue_info, get_queue_info, delete_queue_info,
                                        get_all_certificate_info)
from main.util.xml_util import (get_xpaths_for_xml_tree, get_xpath_names_with_sample_data, 
                                get_updated_xml)
from main.service.xml_db_service import (save_xml_data, get_xml_data,
                                        remove_xml_data, get_all_xml_data, save_xpaths_data, 
                                        get_all_xpaths_for_file, delete_all_xpaths_for_file)
from io import BytesIO
import requests
import lxml.etree as ET

queue_app = Blueprint('queue_app', __name__)


@queue_app.route('/certificate', methods=['POST', 'PUT'])
def saveCertificate():
    if 'cert_file' not in request.files:
        return jsonify({'status':'"cert_file" not found!'})
    cert_file=request.files['cert_file']
    if cert_file.filename=='':
        return jsonify({'status':'file not selected!'})
    elif cert_file:
        s_filename=secure_filename(cert_file.filename)
        return jsonify(save_certificate_info(s_filename, cert_file))
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

@queue_app.route('/getAllCertificateInfo', methods=['GET'])
def getAllCertificateInfo():
    all_files_info =  get_all_certificate_info()
    files_info = {}
    for file_data in all_files_info:
        files_info[file_data.file_id]={
        'file_id':file_data.file_id,
        'file_name':file_data.file_name,
        'update_date':file_data.update_date}

    return jsonify({'all files':files_info})
    


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

@queue_app.route('/getAllQueueNames', methods=['GET'])
def getAllQueueNames():
    return jsonify(get_all_queue_info())



@queue_app.route('/postMessageToMQ', methods=['POST'])
def postMessageToMQ():
    xmlfile_name=request.args.get('xmlfile_name')
    queue_name=request.args.get('queue_name')
    keystore_file_name=request.args.get('keystore_file_name')
    keystore_password=request.args.get('keystore_password')
    truststore_file_name=request.args.get('truststore_file_name')
    truststore_password=request.args.get('truststore_password')
    json_data = request.get_json()

    queue_info = get_queue_info(queue_name)
    queue_info['keyStorePwd']=keystore_password
    queue_info['trustStorePwd']=truststore_password
    queue_info['queueName']=queue_name
    queue_info['messageProperties']=''
    

    keystore_file =  get_certificate_info(keystore_file_name)
    truststore_file =  get_certificate_info(truststore_file_name)

    file_info = get_xml_data(xmlfile_name)
    all_xpaths_json = get_all_xpaths_for_file(xmlfile_name)
    root = ET.parse(BytesIO(file_info.file_data)).getroot()
    
    root = get_updated_xml(root, all_xpaths_json, json_data)
    if root is None:
        return jsonify({'Status':'Unknown error!'})
    str = ET.tostring(root, pretty_print=True)
    queue_info['messageText']=str

    files={
        'keyStoreFile': keystore_file.file_data,
        'trustStoreFile': truststore_file.file_data
    }

    res = requests.post('http://localhost:8080/rest/mq/postMessageTestMessage',
        data=queue_info, files=files)
    
    return jsonify({'Status':res.text})

    

@queue_app.route('/postMessageToSolaceQueue', methods=['POST'])
def postMessageToSolaceQueue():
    pass



