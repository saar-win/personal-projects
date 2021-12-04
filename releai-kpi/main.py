import pandas as pd
import firebase_admin
import os, json
from flask import Flask, jsonify
from datetime import datetime
from datetime import timedelta, timezone
from google.cloud import logging, bigquery
from google.cloud.logging import DESCENDING
from firebase_admin import firestore, credentials

cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
firebase_admin.initialize_app(cred)
app = Flask(__name__)

def statistics(hours):
    '''
    get the logs from google logging
    '''
    clusters = [ "bot-ms-1" ]
    app = "cognition"
    last_hour_date_time = datetime.now(timezone.utc) - timedelta(hours=int(hours))
    _date = last_hour_date_time.isoformat().split(".")[0]
    _list = []
    for cluster in clusters:
        FILTER = f'resource.type="k8s_container" AND resource.labels.cluster_name="{cluster}" AND resource.labels.container_name="{app}" AND timestamp >= "{_date}" AND "session ended"'
        logging_client = logging.Client()
        for entry in logging_client.list_entries(order_by=DESCENDING, filter_=FILTER):
            _list.append(entry.payload)
    return _list

def kpi1():
    '''
    format the logs to the right structure
    '''
    store = firestore.client()
    _sum = []
    collections = [ "workflows", "apps", "orgs", "users" ]
    known_workflows, known_apps, known_orgs, known_users = ({} for i in range(4))
    for collection in collections:
        col_name = store.collection(collection).get()
        for doc in col_name:
            if collection == "workflows":
                known_workflows[doc.id] = doc.get("key")
            if collection == "apps":
                known_apps[doc.id] = doc.get("system_key")
            if collection == "orgs":
                known_orgs[doc.id] = doc.get("name")
            if collection == "users":
                known_users[doc.id] = [ doc.to_dict().get("first_name","None"), doc.to_dict().get("last_name","None"), doc.to_dict().get("emails", "None")[0]]

    for log in statistics(12):
        log = json.loads(log["message"])
        app_ids = [app for app in log["appIds"].split(",")]
        for app_id in app_ids:
            _sum.append({
                "session_id": log["sessionId"],
                "org_id": log["orgId"],
                "org_name": known_orgs.get(log["orgId"], ""),
                "user_id": log["userId"],
                "first_name": known_users.get(log["userId"])[0] if known_users.get(log["userId"]) else None,
                "last_name": known_users.get(log["userId"])[1] if known_users.get(log["userId"]) else None,
                "emails": known_users.get(log["userId"])[2] if known_users.get(log["userId"]) else None,
                "app_name": known_apps.get(app_id),
                "app_id": app_id,
                "workflow_name": known_workflows.get(log["workflowId"], ""),
                "workflow_id": log["workflowId"],
                "run_timestamp": datetime.now(),
            })
    information = json.dumps(_sum, default = convert_datetime)
    df = pd.read_json(information)
    return df

def convert_datetime(o):
    '''
    format timeStamp
    '''
    if isinstance(o, datetime):
        return o.__str__()

@app.route('/api/v1/bigquery')
def main():
    '''
    main function
    write the content to bigquery
    '''
    env = "releai-bot-prod" if "releai-bot-prod" in os.environ["GOOGLE_APPLICATION_CREDENTIALS"] else "releai-bot-dev"
    time_now = str(datetime.now()).split(".")[0]
    info = kpi1()
    client = bigquery.Client(project=env)
    client.load_table_from_dataframe(info, destination="kpi.kpi_db")
    return jsonify({"message": f"write to BigQuery complete {time_now}"})

if __name__ == '__main__':
    app.run(debug=True)
    # _bigquery()
    # kpi1()