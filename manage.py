from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from main import create_app, db
from main.model.model_app import (
    user_info, xml_data, xpath_data, excel_data, queue_config, certificates_info, 
    db_connection_info, db_table_excel_sheet_mapping)

from main.controller.user_db_controller import (
    saveUserInfo, getUserInfo, getAllUsers, removeUserInfo)

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
    getValidationExcelFileInfo, getAllValidationExcelFilesInfo, validateTestInDatabase,
    saveExcelSheetDBTableMappingInfo, removeExcelSheetDBTableMappingInfo, 
    getExcelSheetDBTableMappingInfo, getAllExcelSheetDBTableMappingInfo,
    saveJSONPathDataInfo, removeJSONPathDataInfo, getJSONPathDataInfo,
    getAllJSONPathDataInfo,
    validateExcelDataWithXMLData, validateExcelDataWithJSONData)

from main.controller.sql_db_controller import (
    save_db_connection, get_db_connection, delete_db_connection, get_all_db_connection_info,
    runSQL)

from main.controller.test_scripts_contrller import (
    PostToMQ_XMLAndValidateInDB, PostMultipleToMQ_XMLAndValidateInDB,
    PostMultipleToMQ_MessageAndValidateInDB, PostMultipleToMQ_SplitMessagesAndValidateInDB)

from main.controller.message_db_controller import (
    save_message_file_data_info, get_message_file_data_file, remove_message_file_data,
    get_message_file_data_info, get_all_message_file_data_info, 
    save_split_message_text_data_info, get_message_text_data, remove_message_text_data,
    get_all_message_text_data)


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
