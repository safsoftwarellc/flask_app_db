from main.model.model_app import user_info
from main import db
import datetime

def save_user_info(user_name, user_password):
    data = user_info(user_name=user_name, 
                     user_password=user_password, 
                     update_date=datetime.datetime.utcnow())
    save_changes(data)
    return {'status':'User Saved Successfull!'}

def update_user_info(user_name, user_password):
    user_data = get_user_info(user_name)
    if user_data is not None:
        user_data.user_password = user_password
        user_data.update_date=datetime.datetime.utcnow()
        db.session.commit()
        return {'status':'Existing User updated Successfull!'}
    return {'status':'User not found in system for update!'}

def get_user_info(user_name):
    return user_info.query.filter_by(user_name=user_name).first()

def remove_user_info(user_name):
    user_data = get_user_info(user_name)
    if user_data is not None:
        db.session.delete(user_data)
        db.session.commit()
        return {'status':'User deleted Successfull!'}
    return {'status':'User not found in system for delete!'}

def get_all_users_info():
    return user_info.query.all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()
