import argparse
import requests
import base64
import mysql.connector
from datetime import datetime, timedelta
import logging


def create_the_logger():
    try:
        global logger
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        # Add a console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    except Exception as e:
        raise e


def parse_args():
    try:
        parser = argparse.ArgumentParser(usage='%(prog)s [OPTIONS]')
        parser.add_argument("--file_name", action="store", dest="file name including urls to check"
                            , required=True, help="add file name")
        return parser.parse_args()
    except Exception as e:
        raise e



def virusTotalGet(imply_url, headers):
    try:
        response = requests.get(imply_url, headers=headers)
        return response.json()
    except Exception as e:
        raise e


def execute_mysql_query(query, mysqlhost, mysql_db_user, mysql_db_password, is_ddl):
    try:

        # Create mysql connection
        conn = mysql.connector.connect(user = mysql_db_user
                                       , password = mysql_db_password
                                       , host = mysqlhost
                                   )
        # Create new reader(cursor)
        reader = conn.cursor(buffered=True)
        # Execute the query
        reader.execute(query)
        if is_ddl:
            conn.commit()
        # Fetch all the results
        else:
            results = reader.fetchall()
            return results
    except Exception as e:
        raise e
    finally:
        reader.close()
        conn.close()


###################
## Main
###################
try:
    # define the logger
    create_the_logger()

    ### params ###
    args = parse_args()
    logger.info("Got the following script argument:")
    for arg in vars(args):
        logger.info("-- {}: {}".format(arg, getattr(args, arg)))

    file_name = args.file_name

    # DB connection info
    mysql_host = <add DB host>
    mysql_db_user = <add DB user>
    mysql_password = <add DB password>

    headers = {"x-apikey": "f9d904c64af1f6bceb7b9fbd393da7d871921a38a06a68d196463beb868241ff"}
    site_classification = {}
    results = {}

    # read urls from file
    with open('/usr/sites/' + file_name) as f:
        content = f.readlines()
    # strip the lines
    content = [x.strip() for x in content]

except Exception as e:
    raise e

for url in content:
    try:
        # check if url check if updated (not older than 30 minutes)
        is_status_updated = "select last_check_request  from maint.site_risk_managment where site_url = '{}'".format(url)
        is_status_updated = execute_mysql_query(is_status_updated, mysql_host,mysql_db_user, mysql_password, None)
        # check if there is a need for getting info from virustotal api
        if (not is_status_updated) or (is_status_updated[0][0]) < datetime.utcnow() + timedelta(minutes=-30):
            # get url status from virustotal api
            url_id = base64.urlsafe_b64encode("{}".format(url).encode()).decode().strip("=")
            virustotal_api = 'https://www.virustotal.com/api/v3/urls/{}'.format(url_id)
            api_result = virusTotalGet(virustotal_api, headers)

            status = 'safe'
            # get categories
            for i in api_result['data']['attributes']['categories']:
                site_classification[api_result['data']['attributes']['categories'][i]] \
                    = site_classification.get(api_result['data']['attributes']['categories'][i], 0) + 1

            # get voting
            for i in api_result['data']['attributes']['last_analysis_results']:
                results[api_result['data']['attributes']['last_analysis_results'][i]['result']] \
                    = results.get(api_result['data']['attributes']['last_analysis_results'][i]['result'], 0) + 1

            # check if safe or risk
            if ('malicious' or 'phishing' or 'malware') in results:
                status = 'risk'

            if not is_status_updated:
                update_db = """insert into maint.site_risk_managment (site_url,last_check_request, status, classification, voting) 
                values('{}', '{}', '{}', "{}", "{}")""".format(url, datetime.utcnow(), status, str(site_classification), str(results))
            else:
                update_db = """update maint.site_risk_managment 
                set last_check_request = '{}', status = '{}', classification = "{}", voting = "{}"
                where site_url = '{}' """.format(datetime.utcnow(), status, str(site_classification), str(results), url)
            # update the DB with results
            execute_mysql_query(update_db, mysql_host, mysql_db_user, mysql_password, 1)
    except Exception as e:
        raise e
