from main.model.model_app import (excel_data, db_table_excel_sheet_mapping, 
                                  json_path_data)
from main import db
import datetime

def save_excel_info(file_name, file):
    data = excel_data(excel_file_name=file_name, 
                    excel_file_data=file.read(), 
                    update_date=datetime.datetime.utcnow())
    db.session.add(data)
    db.session.commit()
    return {'status':'File Saved Successfull!'}

def update_excel_info(file_name, file):
    excel_info = get_excel_info(file_name)
    if excel_info is not None:
        excel_info.excel_file_data = file.read()
        excel_info.update_date=datetime.datetime.utcnow()
        db.session.commit()
        return {'status':'Existing File updated Successfull!'}
    return {'status':'File not found in system for update!'}

def get_excel_info(file_name):
    return excel_data.query.filter_by(excel_file_name=file_name).first()

def remove_excel_info(file_name):
    excel_info = get_excel_info(file_name)
    if excel_info is not None:
        db.session.delete(excel_info)
        db.session.commit()
        return {'status':'File deleted Successfull!'}
    return {'status':'File not found in system for delete!'}

def get_all_excel_info():
    return excel_data.query.all()

"""
    DB Table Mapping for Excel Sheets
"""

def save_db_table_excel_sheet_mapping_info(file_name, table_mapping):
    excel_info = get_excel_info(file_name)
    data = db_table_excel_sheet_mapping(excel_id=excel_info.data_id, 
                    table_mapping=str(table_mapping), 
                    update_date=datetime.datetime.utcnow())
    db.session.add(data)
    db.session.commit()
    return {'status':'Information Saved Successfull!'}

def update_db_table_excel_sheet_mapping_info(file_name, table_mapping):
    excel_info = get_excel_info(file_name)
    db_mapping_info = get_db_table_excel_sheet_mapping_info(excel_info.data_id)
    if db_mapping_info is not None:
        db_mapping_info.table_mapping = str(table_mapping)
        db_mapping_info.update_date=datetime.datetime.utcnow()
        db.session.commit()
        return {'status':'Existing File Information updated Successfull!'}
    return {'status':'File Information not found in system for update!'}

def get_db_table_excel_sheet_mapping_info(excel_id):
    return db_table_excel_sheet_mapping.query.filter_by(excel_id=excel_id).first()

def remove_db_table_excel_sheet_mapping_info(file_name):
    excel_info = get_excel_info(file_name)
    db_mapping_info = get_db_table_excel_sheet_mapping_info(excel_info.data_id)
    if db_mapping_info is not None:
        db.session.delete(db_mapping_info)
        db.session.commit()
        return {'status':'Information deleted Successfull!'}
    return {'status':'File not found in system for delete!'}

def get_all_db_table_excel_sheet_mapping_info():
    return db_table_excel_sheet_mapping.query.all()

"""
    JSON Path Data
"""


def save_json_path_data_info(file_name, json_path_mapping):

    json_path_data_from_table = get_json_path_data_info(file_name=file_name)
    if json_path_data_from_table is not None:
        delete_json_paths_into_db(json_path_data_from_table)
    add_json_paths_into_db(file_name, json_path_mapping)
    return {'status':'Information Saved Successfull!'}

def get_json_path_data_info(file_name):
    all_json_paths = json_path_data.query.filter_by(json_file_name=file_name)
    if (all_json_paths is None) or all_json_paths.count()==0:
        return None
    return all_json_paths

def get_json_path_data_all_file_names():
    all_json_files = db.session.query(json_path_data.json_file_name.distinct().label("json_file_name")).all()
    if (all_json_files is None) or len(all_json_files)==0:
        return None
    return all_json_files

def remove_json_path_data_info(file_name):
    json_path_data_from_table = get_json_path_data_info(file_name=file_name)
    if json_path_data_from_table is not None:
        delete_json_paths_into_db(json_path_data_from_table)
        return {'status':'Information deleted Successfull!'}
    return {'status':'File not found in system for delete!'}

def get_all_json_path_data_info():
    return json_path_data.query.all()

def add_json_paths_into_db(file_name, json_path_dict):
    if 'all_json_paths' not in json_path_dict:
        return False
    all_json_paths = json_path_dict['all_json_paths']
    if len(all_json_paths)>0:
        for json_path_full_string in all_json_paths:
            (json_path_name, json_path_string) = split_json_path_full_string(json_path_full_string)
            json_path_record = json_path_data(json_file_name=file_name, 
                                              json_path_name=json_path_name, 
                                              json_path_string=json_path_string,
                                              update_date=datetime.datetime.utcnow())
            db.session.add(json_path_record)
        db.session.commit()
    return True

def delete_json_paths_into_db(json_path_dict):
    if (json_path_dict is None) or json_path_dict.count()==0:
        return 0
    total_json_paths_count = json_path_dict.count()
    for json_path_record in json_path_dict:
        db.session.delete(json_path_record)
    db.session.commit()
    return total_json_paths_count

def split_json_path_full_string(json_path_full_string):
    lastIndex = json_path_full_string.rfind('-')
    xpath_name = json_path_full_string[lastIndex+1:].strip()
    xpath_string = json_path_full_string[:lastIndex].strip()
    return (xpath_name, xpath_string)