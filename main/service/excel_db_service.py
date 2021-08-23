from main.model.model_app import excel_data
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

