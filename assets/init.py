#!/usr/bin/python
import json
import os
import re
import shutil
import sys
import time

__author__ = 'Sebastien LANGOUREAUX'

GHOST_PATH = '/var/lib/ghost'

class ServiceRun():

  def set_config(self, db_type, db, db_port, db_host, db_user, db_password, url, port, mail_transport, mail_host, mail_ssl, mail_port, mail_user, mail_password, mail_from_address, mail_service, mail_key, mail_key_id):

    global GHOST_PATH

    # Check database parameters
    if db_type is None or db_type == '':
        raise KeyError("You must set the database type")
    if db is None or db == '':
        raise KeyError("You must set the database name")
    if (db_type == 'mysql') or (db_type == 'postgresql'):
        if db_user is None or db_user == '':
            raise KeyError("You must set the user to access on database")
        if db_password is None or db_password == '':
            raise KeyError("You must set the password to access on database")
        if db_port is None or db_port == '':
            raise KeyError("You must set the port to access on database server")
        if db_host is None or db_host == '':
            raise KeyError('You must set the host to access on database server')

    # Check node parameters
    if url is None or url == '':
        raise KeyError("You must set the URL of your Ghost blog")
    if port is None or port == '':
        raise KeyError("You must set the port to access of your Ghost blog")


    # Create Json

    json_config = {}
    json_config['production'] = {}


    # Set the database parameter
    if db_type == "sqlite":
        json_config['production']['database'] = {}
        json_config['production']['database']['client'] = 'sqlite3'
        json_config['production']['database']['connection'] = {}
        json_config['production']['database']['connection']['filename'] = 'path.join(__dirname, \'/content/data/' + db + '.db\')'
        json_config['production']['database']['debug'] = 'false'
    elif db_type == "postgresql":
        json_config['production']['database'] = {}
        json_config['production']['database']['client'] = 'pg'
        json_config['production']['database']['connection'] = {}
        json_config['production']['database']['connection']['host'] = db_host
        json_config['production']['database']['connection']['port'] = db_port
        json_config['production']['database']['connection']['user'] = db_user
        json_config['production']['database']['connection']['password'] = db_password
        json_config['production']['database']['connection']['database'] = db
        json_config['production']['database']['connection']['charset'] = 'utf8'
        json_config['production']['database']['debug'] = 'false'
    elif db_type == "mysql":
        json_config['production']['database'] = {}
        json_config['production']['database']['client'] = 'mysql'
        json_config['production']['database']['connection'] = {}
        json_config['production']['database']['connection']['host'] = db_host
        json_config['production']['database']['connection']['port'] = db_port
        json_config['production']['database']['connection']['user'] = db_user
        json_config['production']['database']['connection']['password'] = db_password
        json_config['production']['database']['connection']['database'] = db
        json_config['production']['database']['connection']['charset'] = 'utf8'
        json_config['production']['database']['debug'] = 'false'
    else:
        raise KeyError("The database type must be sqlite, mysql or postgresql")

    # Set node parameters
    json_config['production']['server'] = {}
    json_config['production']['server']['host'] = '0.0.0.0'
    json_config['production']['server']['port'] = port
    json_config['production']['url'] = url


    # Set mail setting
    json_config['production']['mail'] = {}
    if mail_host is not None and mail_host != '':
        json_config['production']['mail']['options'] = {}
        json_config['production']['mail']['options']['host'] = mail_host
        if mail_transport is None or mail_transport == '':
            raise KeyError("You must set the mail protocol")
        if mail_ssl is None or mail_ssl == '':
            raise KeyError("You must set if you should use encrypted connection with your mail server")
        if mail_port is None or mail_port == '':
            raise KeyError("You must set the mail server port")
        json_config['production']['mail']['transport'] = mail_transport
        json_config['production']['mail']['options']['port'] = mail_port
        json_config['production']['mail']['options']['secureConnection'] = mail_ssl

        if mail_user is not None and mail_user != '' and mail_password is not None and mail_password != '' :
            json_config['production']['mail']['options']['auth'] = {}
            json_config['production']['mail']['options']['auth']['user'] = mail_user
            json_config['production']['mail']['options']['auth']['pass'] = mail_password
    if mail_service == 'mailgun' and mail_user is not None and mail_user != '' and mail_password is not None and mail_password != '' :
        json_config['production']['mail']['transport'] = 'SMTP'
        json_config['production']['mail']['options'] = {}
        json_config['production']['mail']['options']['service'] = 'Mailgun'
        json_config['production']['mail']['options']['auth'] = {}
        json_config['production']['mail']['options']['auth']['user'] = mail_user
        json_config['production']['mail']['options']['auth']['pass'] = mail_password
    if mail_service == 'ses' and mail_key is not None and mail_key != '' and mail_key_id is not None and mail_key_id != '' :
        json_config['production']['mail']['transport'] = 'SES'
        json_config['production']['mail']['options'] = {}
        json_config['production']['mail']['options']['AWSAccessKeyID'] = mail_key_id
        json_config['production']['mail']['options']['AWSSecretKey'] = mail_key
    if mail_service == 'gmail' and mail_user is not None and mail_user != '' and mail_password is not None and mail_password != '' :
        json_config['production']['mail']['transport'] = 'SMTP'
        json_config['production']['mail']['options'] = {}
        json_config['production']['mail']['options']['auth'] = {}
        json_config['production']['mail']['options']['auth']['user'] = mail_user
        json_config['production']['mail']['options']['auth']['pass'] = mail_password
    if mail_from_address is not None and mail_from_address != '':
        json_config['production']['mail']['fromaddress'] = mail_from_address


    json_config = json.dumps(json_config)

    config = '''
        // # Ghost Configuration
        // Setup your Ghost install for various [environments](http://support.ghost.org/config/#about-environments).

        // Ghost runs in `development` mode by default. Full documentation can be found at http://support.ghost.org/config/

        var path = require('path'),
        config;

        config = ''' + str(json_config) + ''';
        module.exports = config;
    '''

    self.add_end_file(GHOST_PATH + '/config.js', config)


  def replace_all(self, file, searchRegex, replaceExp):
    """ Replace String in file with regex
    :param file: The file name where you should to modify the string
    :param searchRegex: The pattern witch must match to replace the string
    :param replaceExp: The string replacement
    :return:
    """

    regex = re.compile(searchRegex, re.IGNORECASE)

    f = open(file,'r')
    out = f.readlines()
    f.close()

    f = open(file,'w')

    for line in out:
      if regex.search(line) is not None:
        line = regex.sub(replaceExp, line)

      f.write(line)

    f.close()


  def add_end_file(self, file, line):
    """ Add line at the end of file
    :param file: The file where you should to add line to the end
    :param line: The line to add in file
    :return:
    """
    with open(file, "a") as myFile:
        myFile.write("\n" + line + "\n")






if __name__ == '__main__':

    if os.path.isfile(GHOST_PATH + '/config.js'):
        shutil.copy2(GHOST_PATH + '/config.js', GHOST_PATH + '/config.js.org')
        os.remove(GHOST_PATH + '/config.js')

    service = ServiceRun()


    if os.getenv('DB_TYPE') is None:
        db_type = 'sqlite'
    else :
        db_type = os.getenv('DB_TYPE')


    if os.getenv('DB_HOST') is None:
        db_host = 'db'
    else:
        db_host = os.getenv('DB_HOST')

    if os.getenv('DB_DATABASE') is not None:
        db = os.getenv('DB_DATABASE')
    elif os.getenv('DB_ENV_POSTGRES_DB') is not None:
        db = os.getenv('DB_ENV_POSTGRES_DB')
    elif os.getenv('DB_ENV_MYSQL_DATABASE') is not None:
        db = os.getenv('DB_ENV_MYSQL_DATABASE')
    else:
        db = 'ghost'


    if os.getenv('DB_USER') is not None:
        db_user = os.getenv('DB_USER')
    elif os.getenv('DB_ENV_POSTGRES_USER') is not None:
        db_user = os.getenv('DB_ENV_POSTGRES_USER')
    elif os.getenv('DB_ENV_MYSQL_USER') is not None:
        db_user = os.getenv('DB_ENV_MYSQL_USER')
    else:
        db_user = None

    if os.getenv('DB_PASS') is not None:
        db_pass = os.getenv('DB_PASS')
    elif os.getenv('DB_ENV_POSTGRES_PASSWORD') is not None:
        db_pass = os.getenv('DB_ENV_POSTGRES_PASSWORD')
    elif os.getenv('DB_ENV_MYSQL_PASSWORD') is not None:
        db_pass = os.getenv('DB_ENV_MYSQL_PASSWORD')
    else:
        db_pass = None

    if os.getenv('DB_PORT') is not None:
        db_port = os.getenv('DB_PORT')
    elif os.getenv('DB_TYPE') == 'postgresql':
        db_port = '5432'
    elif os.getenv('DB_TYPE') == 'mysql':
        db_port = '3306'
    else:
        db_pass = None



    if os.getenv('GHOST_PORT') is None:
        port = '2368'
    else:
        port = os.getenv('GHOST_PORT')

    if os.getenv('MAIL_NAME') is None:
        mail_host = 'mail'
    else:
        mail_host = os.getenv('MAIL_NAME')



    service.set_config(db_type, db, db_port, db_host, db_user, db_pass, os.getenv('GHOST_URL'), port, os.getenv('MAIL_TRANSPORT'), mail_host, os.getenv('MAIL_SSL'), os.getenv('MAIL_PORT'), os.getenv('MAIL_USER'), os.getenv('MAIL_PASSWORD'), os.getenv('MAIL_FROM_ADDRESS'), os.getenv('MAIL_SERVICE'), os.getenv('MAIL_SES_KEY'), os.getenv('MAIL_SES_KEY_ID'))
