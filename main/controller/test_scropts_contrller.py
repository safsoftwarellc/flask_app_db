from flask import Blueprint, request, jsonify

test_scripts_app = Blueprint('test_scripts_app', __name__)

@test_scripts_app.route('/PostToMQAnXMLAndValidateInDB', methods=['POST'])
def PostToMQAnXMLAndValidateInDB():
    #Template Name  #Test Data  #MQ details
    #Cert Info      #DB Info    # Validation Excel
    #Prepare XML    #Submit MQ  # Validate in DB
    pass

@test_scripts_app.route('/PostMultipleToMQAnXMLAndValidateInDB', methods=['POST'])
def PostMultipleToMQAnXMLAndValidateInDB():
    pass


