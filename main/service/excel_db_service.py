from main.model.model_app import excel_data, db_table_excel_sheet_mapping
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
                    table_mapping=table_mapping, 
                    update_date=datetime.datetime.utcnow())
    db.session.add(data)
    db.session.commit()
    return {'status':'Information Saved Successfull!'}

def update_db_table_excel_sheet_mapping_info(file_name, table_mapping):
    excel_info = get_excel_info(file_name)
    db_mapping_info = get_db_table_excel_sheet_mapping_info(excel_info.data_id)
    if db_mapping_info is not None:
        db_mapping_info.table_mapping = table_mapping
        db_mapping_info.update_date=datetime.datetime.utcnow()
        db.session.commit()
        return {'status':'Existing File Information updated Successfull!'}
    return {'status':'File Information not found in system for update!'}

def get_db_table_excel_sheet_mapping_info(file_name):
    excel_info = get_excel_info(file_name)
    return db_table_excel_sheet_mapping.query.filter_by(excel_id=excel_info.data_id).first()

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

