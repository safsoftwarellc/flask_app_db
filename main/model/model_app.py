from main import db

class xml_data(db.Model):
    __tablename__='xml_data'
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(50), unique = True, nullable = False)
    file_data = db.Column(db.LargeBinary)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'File - {}'.format(self.file_name)


class xpath_data(db.Model):
    __tablename__='xpath_data'
    xpath_id = db.Column(db.Integer, primary_key=True)

    file_id = db.Column(db.Integer, db.ForeignKey('xml_data.file_id'), nullable=False)
    file_id_relation = db.relationship('xml_data', backref=db.backref('xpaths', lazy=True))

    xpath_name = db.Column(db.String(80), nullable = False)
    xpath_string = db.Column(db.String(250), nullable = False)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'Xpath - {}'.format(self.xpath_string)

class excel_data(db.Model):
    __tablename__='excel_data'
    data_id = db.Column(db.Integer, primary_key=True)
    excel_file_name=db.Column(db.String(50), unique = True, nullable = False)
    excel_file_data=db.Column(db.LargeBinary, nullable=False)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'File Name - {}'.format(self.excel_file_name)

class queue_config(db.Model):
    __tablename__='queue_config'
    config_id = db.Column(db.Integer, primary_key=True)
    queue_name=db.Column(db.String(50), nullable = False)
    config_name=db.Column(db.String(80), nullable = False)
    config_value=db.Column(db.String(120), nullable = True)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'Config Name - {} and Value - {}'.format(self.config_name, self.config_value)

class certificates_info(db.Model):
    __tablename__='certificates_info'
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(50), unique = True, nullable = False)
    file_data = db.Column(db.LargeBinary)
    file_password = db.Column(db.String(120), nullable = True)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'File - {}'.format(self.file_name)


class db_connection_info(db.Model):
    __tablename__='db_connection_info'
    id = db.Column(db.Integer, primary_key=True)
    db_name = db.Column(db.String(50), unique = True, nullable = False)
    db_connection_string = db.Column(db.String(250), nullable = True)
    db_user_name = db.Column(db.String(120), nullable = True)
    db_password = db.Column(db.String(250), nullable = True)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'Database name - {}'.format(self.db_name)


class db_table_excel_sheet_mapping(db.Model):
    __tablename__='db_table_excel_sheet_mapping'
    id = db.Column(db.Integer, primary_key=True)
    excel_id = db.Column(db.Integer, unique=True, nullable = False)
    table_mapping=db.Column(db.String(600), nullable=False)
    update_date = db.Column(db.DateTime())

    def __repr__(self):
        return 'table_mapping - {}'.format(self.table_mapping)
