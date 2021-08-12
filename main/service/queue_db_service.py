from main.model.model_app import certificates_info, queue_config
from main import db
import datetime


def save_certificate_info(file_name, file):
    data = certificates_info(file_name=file_name, file_data=file.read(), update_date=datetime.datetime.utcnow())
    save_changes(data)

def get_certificate_info(file_name):
    return certificates_info.query.filter_by(file_name=file_name).first()

def remove_certificate_info(file_name):
    file_data = certificates_info.query.filter_by(file_name=file_name).first()
    delete_changes(file_data)

def update_certificate_info(file_name, file):
    file_data = certificates_info.query.filter_by(file_name=file_name).first()
    file_data.file_data = file.read()
    file_data.update_date=datetime.datetime.utcnow()
    db.session.commit()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()


'''
Queue Config Table Actions
'''

def save_queue_info(queue_name, config_dict):
    queue_info_dict = get_queue_info(queue_name)
    if queue_info_dict is not None:
        delete_queue_info(queue_name)

    for config_name, config_value in config_dict.items():
        data = queue_config(queue_name=queue_name, config_name=config_name, 
                            config_value=config_value, update_date=datetime.datetime.utcnow())
        db.session.add(data)
    db.session.commit()
    return True

def delete_queue_info(queue_name):
    config_dict = get_queue_info(queue_name)
    if (config_dict is None) or config_dict.count()==0:
        return False
    for config_record in config_dict:
        db.session.delete(config_record)
    db.session.commit()
    return True

def get_queue_info(queue_name):
    queue_config_info = queue_config.query.filter_by(queue_name=queue_name)
    all_configs = {}
    if (queue_config_info is None) or  queue_config_info.count()==0:
        return all_configs
    for queue_config_record in queue_config_info:
        all_configs[queue_config_record.config_name]=queue_config_record.config_value
    return all_configs
