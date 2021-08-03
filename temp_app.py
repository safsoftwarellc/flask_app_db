import requests

values={
    'queueName':'queueName', 
    'messageProperties':'', 
    'hostName':'hostName',
    'portNumber':'123', 
    'queueManager':'queueManager',
    'channel':'', 
    'sslCipherSuite':'sslCipherSuite',
    'useIBMCipherMappings':'useIBMCipherMappings',
    'keyStorePwd':'keyStorePwd',
    'trustStorePwd':'trustStorePwd'
}

files={
    'messageFile': open('/Users/sunilduvvuru/Documents/git/flask_app_db/Upload_Files/msg-ex21-credit-event-notice.xml', 'rb'),
    'keyStoreFile': open('/Users/sunilduvvuru/Documents/git/flask_app_db/Upload_Files/msg-ex21-credit-event-notice.xml', 'rb'),
    'trustStoreFile': open('/Users/sunilduvvuru/Documents/git/flask_app_db/Upload_Files/msg-ex21-credit-event-notice.xml', 'rb')
}

res = requests.post('http://localhost:8080/rest/mq/postMessageTest', \
    data=values, files=files)

print(res.text)

