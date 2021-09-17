from flask import Blueprint, request, jsonify
from main.service.sql_db_service import (create_db_connection_info,
                                read_db_connection_info, update_db_connection_info,
                                delete_db_connection_info, read_all_db_connection_info,
                                get_data_from_db_using_SQL)
import requests


sql_db_app = Blueprint('sql_db_app', __name__)

@sql_db_app.route('/db_connection', methods=['POST', 'PUT'])
def save_db_connection():
    db_info_dict = {
        'db_name': request.args.get('db_name'),
        'db_connection_string': request.args.get('db_connection_string'),
        'db_user_name': request.args.get('db_user_name'),
        'db_password': request.args.get('db_password')
    }

    if request.method == 'PUT':
        return update_db_connection_info(db_info_dict)
    else:
        return create_db_connection_info(db_info_dict)


@sql_db_app.route('/db_connection', methods=['GET'])
def get_db_connection():
    db_name=request.args.get('db_name')
    return read_db_connection_info(db_name)

@sql_db_app.route('/db_connection', methods=['DELETE'])
def delete_db_connection():
    db_name=request.args.get('db_name')
    return delete_db_connection_info(db_name)

@sql_db_app.route('/db_connection_all', methods=['GET'])
def get_all_db_connection_info():
    return read_all_db_connection_info()


'''
    Get SQL Data
'''
@sql_db_app.route('/runSQL', methods=['GET'])
def runSQL():
    db_name=request.args.get('db_name')
    sql_query=request.args.get('sql_query')
    db_connection_info = read_db_connection_info(db_name)
    return get_data_from_db_using_SQL(db_connection_info, sql_query)

