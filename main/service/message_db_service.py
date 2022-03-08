from main.model.model_app import message_data, message_text_data
from main import db
import datetime

def save_message_data_info(file_name, file):
    data = message_data(file_name=file_name, 
                        file_data=file.read(), 
                        update_date=datetime.datetime.utcnow())
    db.session.add(data)
    db.session.commit()
    return {'status':'File Saved Successfull!'}

def update_message_data_info(file_name, file):
    message_data_info = get_message_data_info(file_name)
    if message_data_info is not None:
        message_data_info.file_data = file.read()
        message_data_info.update_date=datetime.datetime.utcnow()
        db.session.commit()
        return {'status':'Existing File updated Successfull!'}
    return {'status':'File not found in system for update!'}

def get_message_data_info(file_name):
    return message_data.query.filter_by(file_name=file_name).first()

def remove_message_data_info(file_name):
    message_data_info = get_message_data_info(file_name)
    if message_data_info is not None:
        db.session.delete(message_data_info)
        db.session.commit()
        return {'status':'File deleted Successfull!'}
    return {'status':'File not found in system for delete!'}

def get_all_message_data_info():
    return message_data.query.all()


#######################

def save_message_text_data_info(file_name, header_text, footer_text, 
                                line_1, line_2, line_3, line_4, line_5,
                                line_6, line_7, line_8, line_9, line_10):
    data = message_text_data(file_name=file_name, 
                        header_text=header_text, 
                        footer_text=footer_text, 
                        line_1=line_1, line_2=line_2, 
                        line_3=line_3, line_4=line_4, 
                        line_5=line_5, line_6=line_6, 
                        line_7=line_7, line_8=line_8, 
                        line_9=line_9, line_10=line_10, 
                        update_date=datetime.datetime.utcnow())
    db.session.add(data)
    db.session.commit()
    return {'status':'Data Saved Successfull!'}

def update_message_text_data_info(file_name, header_text, footer_text, 
                                line_1, line_2, line_3, line_4, line_5,
                                line_6, line_7, line_8, line_9, line_10):
    message_text_data_info = get_message_text_data_info(file_name)
    if message_text_data_info is not None:
        message_text_data_info.header_text = header_text
        message_text_data_info.footer_text = footer_text
        message_text_data_info.line_1 = line_1
        message_text_data_info.line_2 = line_2
        message_text_data_info.line_3 = line_3
        message_text_data_info.line_4 = line_4
        message_text_data_info.line_5 = line_5
        message_text_data_info.line_6 = line_6
        message_text_data_info.line_7 = line_7
        message_text_data_info.line_8 = line_8
        message_text_data_info.line_9 = line_9
        message_text_data_info.line_10 = line_10
        message_text_data_info.update_date=datetime.datetime.utcnow()
        db.session.commit()
        return {'status':'Existing Data updated Successfull!'}
    return {'status':'File not found in system for update!'}

def get_message_text_data_info(file_name):
    return message_text_data.query.filter_by(file_name=file_name).first()

def remove_message_text_data_info(file_name):
    message_text_data_info = get_message_text_data_info(file_name)
    if message_text_data_info is not None:
        db.session.delete(message_text_data_info)
        db.session.commit()
        return {'status':'File deleted Successfull!'}
    return {'status':'File not found in system for delete!'}

def get_all_message_text_data_info():
    return message_text_data.query.all()

