from main.model.model_app import db_connection_info
from main import db
import datetime
from sqlalchemy import create_engine
from sqlalchemy.sql import text

def create_db_connection_info(db_name, 
                                db_connection_string,
                                db_user_name, 
                                db_password):
    data = db_connection_info(
        db_name=db_name, 
        db_connection_string=db_connection_string,
        db_user_name=db_user_name,
        db_password=db_password,
        update_date=datetime.datetime.utcnow()) 
    save_changes(data=data)
    return {'status':'DB Info Saved Successfull!'}

def get_db_connection_info(db_name):
    return db_connection_info.query.filter_by(db_name=db_name).first()
    
def read_db_connection_info(db_name):
    row_data = get_db_connection_info(db_name)
    row_info = {}
    if row_data is not None:
        row_info[row_data.db_name]={
        'db_name':row_data.db_name,
        'db_connection_string':row_data.db_connection_string,
        'db_user_name':row_data.db_user_name,
        'db_password':row_data.db_password,
        'update_date':row_data.update_date}
    return {'DB Info':row_info}

def update_db_connection_info(db_name, 
                                db_connection_string,
                                db_user_name, 
                                db_password):
    data = get_db_connection_info(db_name)
    data.db_connection_string = db_connection_string
    data.db_user_name = db_user_name
    data.db_password = db_password
    data.update_date = datetime.datetime.utcnow()
    db.session.commit()
    return {'status':'DB Info Saved Successfull!'}

def delete_db_connection_info(db_name):
    delete_changes(get_db_connection_info(db_name))
    return {'status':'DB Info Deleted Successfull!'}

def read_all_db_connection_info():
    all_rows = db_connection_info.query.all()
    rows_info = {}
    for row_data in all_rows:
        rows_info[row_data.db_name]={
        'db_name':row_data.db_name,
        'db_connection_string':row_data.db_connection_string,
        'db_user_name':row_data.db_user_name,
        'db_password':row_data.db_password,
        'update_date':row_data.update_date}
    return {'DB Info':rows_info}

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def delete_changes(data):
    db.session.delete(data)
    db.session.commit()

'''
    read data from DB
'''
def get_data_from_db_using_SQL(db_connection_info, sql_query):
    db_connection_string = db_connection_info.db_connection_string
    db_connection_string= db_connection_string.replace("<USER_NAME>", db_connection_info.db_user_name)
    db_connection_string= db_connection_string.replace("<PASSWORD>", db_connection_info.db_password)
    
    sql_query_data = []
    try:
        engine = create_engine(db_connection_string, echo=True)
        conn = engine.connect()

        res = conn.execute(sql_query)
        res_fecth_all = res.fetchall()
        for row in res_fecth_all:
            sql_query_data.append(dict(row))
        
    except:
        print('Exception in getting DB data!!!')
    finally:
        if conn:
            try:
                conn.close()
            except:
                print('Exception in Closing Connection')
        if engine:
            try:
                engine.dispose()
            except:
                print('Exception in Closing Engine')

    
    return sql_query_data

    
def get_data_from_DB(db_name, sql_query):
    db_connection_info = get_db_connection_info(db_name)
    return get_data_from_db_using_SQL(db_connection_info, sql_query)
