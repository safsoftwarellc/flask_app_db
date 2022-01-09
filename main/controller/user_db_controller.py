from flask import Blueprint, request, jsonify, send_file
from main.service.user_db_service import (save_user_info, update_user_info,
                                          get_user_info, remove_user_info, get_all_users_info)


user_info_app = Blueprint('user_info_app', __name__)

@user_info_app.route('/userInfo', methods=['POST', 'PUT'])
def saveUserInfo():
    user_name=request.args.get('user_name')
    user_password=request.args.get('user_password')
    if user_name is None:
        return jsonify({'Status':'user_name should have value'})
    if user_password is None:
        return jsonify({'Status':'user_password should have value'})
    if request.method == 'PUT':
        return jsonify(update_user_info(user_name=user_name, user_password=user_password))
    else:
        user_data = get_user_info(user_name)
        if user_data is not None:
            return jsonify({'Status':'user_name already exists'})
        return jsonify(save_user_info(user_name=user_name, user_password=user_password))

@user_info_app.route('/userInfo', methods=['GET'])
def getUserInfo():
    user_name=request.args.get('user_name')
    return jsonify(get_user_info(user_name))

@user_info_app.route('/userInfo', methods=['DELETE'])
def removeUserInfo():
    user_name=request.args.get('user_name')
    return jsonify(remove_user_info(user_name))

@user_info_app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    return jsonify(get_all_users_info())
