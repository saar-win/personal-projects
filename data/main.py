import pandas as pd
import firebase_admin, json, os
from flask import Flask, jsonify
from distutils import util
from datetime import datetime
from datetime import timedelta, timezone
from google.cloud import bigquery, logging
from google.cloud.logging import DESCENDING
from firebase_admin import firestore, credentials

firebase_admin.initialize_app(credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
env = "releai-bot-prod" if "releai-bot-prod" in os.environ["GOOGLE_APPLICATION_CREDENTIALS"] else "releai-bot-dev"
client = bigquery.Client(project=env)
app = Flask(__name__)

def statistics(hours, app_list, flag):
    '''
    get the all logs regarding to the services.
    '''
    env_ms_name = "bot-ms-1"
    last_hour_date_time = datetime.now(timezone.utc) - timedelta(hours=int(hours))
    _date = last_hour_date_time.isoformat().split(".")[0]
    _list = []
    for app in app_list:
        FILTER = f'resource.type="k8s_container" AND resource.labels.cluster_name="{env_ms_name}" AND resource.labels.container_name="{app}" AND timestamp >= "{_date}" AND "{flag}"'
        logging_client = logging.Client()
        for entry in logging_client.list_entries(order_by=DESCENDING, filter_=FILTER):
            _list.append(entry.payload)
    return _list

def fs_users():
    '''
    uses for each user on FS dataBase
    '''
    # collect orgs
    store = firestore.client()
    orgs = store.collection(u"orgs").order_by(u"create_timestamp").get()
    users = store.collection(u"users").order_by(u"create_timestamp").get()
    _object = {}
    org_ids = []
    for org in orgs:
        org_data = org.to_dict()
        create_timestamp = org_data["create_timestamp"]
        org_ids.append(org.id)
        _object[org.id] = {
            "org_id": str(org.id),
            "org_name": org_data["name"],
            "users_counter": 0,
            "subscription": "true" if org_data.get("subscription") else "false",
            "create_date": str(org_data["create_timestamp"]).split(" ")[0],
            "trail_end": str(create_timestamp + timedelta(days=org_data.get("trail_days"))).split(" ")[0],
            "hubspot_api": "true" if org_data.get("hubspot",{}).get("api_key") else "false",
            "bot_number": str(org_data.get("clara_number")),
            "bot_lang": org_data.get("bot_lang", "None"),
            "daily_new_contact_counter": 0,
            "daily_new_attachment_counter": 0,
            "daily_new_record_counter": 0,
            "daily_new_search_counter": 0,
            "new_user_daily": 0,
            "run_timestamp": datetime.now(),
            "users": []
        }
    # collect users by org id
    for user in users:
        user_data = user.to_dict()
        user_org = user_data.get("orgs", [])
        if len(user_org):
            if user_org[0] in org_ids:
                _object[user_org[0]]["users"].append({
                    "org_name": _object[user_org[0]]["org_name"],
                    "org_id": user_data.get("orgs")[0],
                    "user_id": user.id,
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "is_admin": bool(util.strtobool("true")) if user_data.get("auth",{}).get("access_level") == 10 else bool(util.strtobool("false")),
                    "emails": user_data.get("emails")[0],
                    "mobiles": user_data.get("mobiles")[0],
                    "salesforce": bool(util.strtobool("true")) if user_data.get("salesforce") else bool(util.strtobool("false")),
                    "hubspot_oauth": bool(util.strtobool("true")) if user_data.get("hubspot") else bool(util.strtobool("false")),
                    "mailing": bool(util.strtobool("true")) if user_data.get("mailing") else bool(util.strtobool("false")),
                    "create_timestamp": str(user_data.get("create_timestamp")).split(".")[0],
                    "last_seen": str(user_data.get("last_seen_timestamp")).split(".")[0],
                    "country_code": user_data.get("mobiles_country_code"),
                    "mailing_records_counter": 0,
                    "hubspot_records_counter": 0,
                    "salesforce_records_counter": 0,
                    "hubspot_new_contact_records_counter": 0,
                    "salesforce_new_contact_records_counter": 0,
                    "hubspot_attachment_records_counter": 0,
                    "hubspot_searches_records_counter": 0,
                    "salesforce_attachment_records_counter": 0,
                    "salesforce_searches_records_counter": 0,
                    "mailing_attachment_records_counter": 0,
                    "run_timestamp": datetime.now()
                })

    return _object

def count_logs():
    '''
    count the number of uses on each service
    '''
    logs = statistics(24, app_list=["hubspot", "salesforce","mailing"], flag="new_")
    data = fs_users()
    for org_id in data:
        # for user counter
        if int(str(data[org_id]["users"]).count("user_id")):
            data[org_id]["users_counter"] = int(str(data[org_id]["users"]).count("user_id"))
        for user in data[org_id].get("users", []):
                if str(user["create_timestamp"]).split(" ")[0] in str(datetime.now()).split(' ')[0]:
                    data[org_id]["new_user_daily"] = data[org_id]["new_user_daily"] + 1
        for log in logs:
            if type(log) == str:
                integrations = [ "mailing", "hubspot", "salesforce" ]
                kinds = [ "new_attachment", "new_record", "new_contact", "new_search" ]
                if org_id in log:
                    for kind in kinds:
                        if kind in log:
                            data[org_id][f"daily_{kind}_counter"] = data[org_id][f"daily_{kind}_counter"] + 1
                # user data log for integration in attachment or new test messages
                for user in data[org_id].get("users", []):
                    if user["user_id"] in log:
                        for kind in kinds:
                            if kind in log:
                                for integration in integrations:
                                    if integration in log:
                                        if kind == "new_record":
                                            user[f"{integration}_records_counter"] = user[f"{integration}_records_counter"] + 1
                                        if kind == "new_attachment":
                                            user[f"{integration}_attachment_records_counter"] = user[f"{integration}_attachment_records_counter"] + 1
                                        if kind == "new_contact":
                                            user[f"{integration}_new_contact_records_counter"] = user[f"{integration}_new_contact_records_counter"] + 1
                                        if kind == "new_search":
                                            user[f"{integration}_searches_records_counter"] = user[f"{integration}_searches_records_counter"] + 1
    return data

def user_deleted():
    '''
    for deleted user document
    '''
    logs = statistics(24, app_list=["components"], flag="user_deleted")
    deleted_obj = []
    for log in logs:
        deleted_obj.append({
            "message": log.get("message"),
            "userExecutedDeleteId": log.get("userExecutedDeleteId"),
            "orgName": log.get("orgName"),
            "deletedUserId": log.get("userExecutedDeleteId"),
            "deletedUserFirtName": log.get("deletedUserFirstName"),
            "deletedUserLastName": log.get("deletedUserLastName"),
            "deletedUserEmail": log.get("deletedUserEmail"),
            "deletedUserMobile": log.get("deletedUserMobile"),
            "run_timestamp": datetime.now()
        })
    users_deleted = json.dumps(deleted_obj, default = convert_datetime)
    df = pd.read_json(users_deleted)
    if df.empty:
        return None
    else:
        return df

def org_deleted():
    '''
    for delete org document
    '''
    logs = statistics(24, app_list=["components"], flag="org_deleted")
    deleted_obj = []
    for log in logs:
        deleted_obj.append({
            "message": log.get("message"),
            "userExecutedDeleteId": log.get("userExecutedDeleteId"),
            "orgName": log.get("orgName"),
            "deletedUserId": log.get("userExecutedDeleteId"),
            "deletedUserFirtName": log.get("deletedUserFirstName"),
            "deletedUserLastName": log.get("deletedUserLastName"),
            "deletedUserEmail": log.get("deletedUserEmail"),
            "deletedUserMobile": log.get("deletedUserMobile"),
            "run_timestamp": datetime.now()
        })
    orgs_deleted = json.dumps(deleted_obj, default = convert_datetime)
    df = pd.read_json(orgs_deleted)
    if df.empty:
        return None
    else:
        return df

def convert_datetime(o):
    '''
    format timeStamp
    '''
    if isinstance(o, datetime):
        return o.__str__()

def map_orgs():
    '''
    format the orgs to right structure
    '''
    full_data = count_logs()
    orgs = []
    for full_org_data in full_data.values():
        del full_org_data["users"]
        orgs.append(full_org_data)
    orgs = json.dumps(orgs, default = convert_datetime)
    df = pd.read_json(orgs)
    return df

def map_users():
    '''
    format the user to right structure
    '''
    full_data = count_logs()
    users = []
    for full_org_data in full_data.values():
        if full_org_data["users"] != []:
            if len(full_org_data["users"]) > 1:
                for i in range(len(full_org_data["users"])):
                    users.append(full_org_data["users"][i])
            else:
                users.append(full_org_data["users"][0])
    users_json = json.dumps(users, default = convert_datetime)
    df = pd.read_json(users_json)
    return df

@app.route('/api/v1/bigquery')
def main():
    '''
    write the objects
    '''
    time_now = str(datetime.now()).split('.')[0]
    client.load_table_from_dataframe(map_users(), destination="users_db.users_db")
    client.load_table_from_dataframe(map_orgs(), destination="orgs_db.orgs_db")
    users_deleted = user_deleted()
    orgs_deleted = org_deleted()
    if users_deleted != None:
        try:
            client.load_table_from_dataframe(users_deleted, destination="deleted_users.deleted_users_db")
        except Exception as err:
            print("map_users_deleted ERR", err)
    if orgs_deleted != None:
        try:
            client.load_table_from_dataframe(orgs_deleted, destination="deleted_orgs.deleted_orgs_db")
        except Exception as err:
            print("map_orgs_deleted ERR", err)
    return jsonify({"message": f"writing to Bq completed {time_now}"})


# def env_settings():
#     if os.environ['ENV'] == "prod":
#         os.environ['BUCKET_NAME'] = "prod_database_backup_rb"
#         os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "/etc/releai/keys/releai-bot-prod.json"
# #
#     else:
#         os.environ['ENV'] == "dev"
#         os.environ['BUCKET_NAME'] = "database_backup_rb"
#         os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  "/etc/releai/keys/releai-bot-dev.json"

if __name__ == '__main__':
    app.run(debug=True, port=8081)
    # env_settings()
    # upload_to_bucket()
# ENV to set:
#   google application cred
#   env "ENV"
#   env "BUCKET_NAME"
#   env "FLASK_RUN_PORT"
#   env "FLASK_APP"