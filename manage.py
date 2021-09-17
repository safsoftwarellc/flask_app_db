from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from main import create_app, db
from main.model.model_app import xml_data, xpath_data, excel_data, queue_config
from main.controller.xml_controller import (
    saveTemplateXMLFile, getTemplateXMLFile,
    removeTemplateXMLFile, generateXpathsForXMLFile,
    getAllTemplateXMLFiles, getUpdatedTemplateXMLFile,
    saveXpathsForTemplateFile, getXpathsForTemplateFile,
    deleteXpathsForTemplateFile, getUpdatedTemplateXMLFile,
    getXpathNamesWithSampleDataForTemplateFile)
from main.controller.queue_controller import (
    saveCertificate, removeCertificate, getCertificate, getCertificateInfo,
    saveQueueInformation, deleteQueueInformation, getQueueInformation,
    postMessageToMQ, postMessageToSolaceQueue, getAllQueueNames, getAllCertificateInfo)

from main.controller.excel_validations_controller import (
    saveValidationExcelFile, getValidationExcelFile, removeValidationExcelFile,
    getValidationExcelFileInfo, getAllValidationExcelFilesInfo
)

from main.controller.sql_db_controller import (
    save_db_connection, get_db_connection, delete_db_connection, get_all_db_connection_info,
    runSQL
)


app = create_app('dev')
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

if __name__ == '__main__':
    manager.run()
