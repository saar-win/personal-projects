
import json, os, time
import grequests
import firebase_admin
import pandas as pd
from datetime import datetime
from firebase_admin import firestore, credentials

firebase_admin.initialize_app(credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"]))
store = firestore.client()

def get_list():
    '''
    get the subscription list from Firestore db
    '''
    t0 = time.time()
    subcriptions_list = []
    orgs_ids = store.collection(u"orgs").where(u'subscription', u'!=', u'null').stream()
    for org in orgs_ids:
        subcriptions_list.append({ "orgId": org.id, "orgName": org.get('name'), "subscription": org.get('subscription') if 'sub_' in org.get('subscription') else '' })
    for client in list(subcriptions_list):
        if client["subscription"] == '':
            del subcriptions_list[subcriptions_list.index(client)]
    t1 = time.time()
    total_time = t1 - t0
    print(total_time)
    return subcriptions_list

def stripe(db_list):
    '''
    get from stripe api the information about plan.
    async request
    '''
    t0 = time.time()
    url = "https://api.stripe.com/v1/subscriptions/"
    headers = {"Authorization": f"Bearer {os.environ['STRIPE_AUTH']}"}
    releai_client_object, clients = ([] for i in range(2))
    for subscription in db_list:
        clients.append(url + subscription["subscription"])
    stripe_res = (grequests.get(client, headers=headers) for client in clients)
    responses = [json.loads(res.text) for res in grequests.map(stripe_res)]
    for (stripe_obj, rele_obj) in zip(responses, db_list):
        if type(stripe_obj.get("canceled_at", "None")) == int:
            subs_canceled_time = datetime.utcfromtimestamp(stripe_obj.get("canceled_at", "None")).strftime('%Y-%m-%d %H:%M:%S')
        else:
            subs_canceled_time = "None"
        releai_client_object.append({
            "orgName": rele_obj.get("orgName", "None"),
            "orgId": rele_obj.get("orgId", "None"),
            "start_period": (datetime.utcfromtimestamp(stripe_obj.get("current_period_start", "None")).strftime('%Y-%m-%d %H:%M:%S')),
            "end_period": (datetime.utcfromtimestamp(stripe_obj.get("current_period_end", "None")).strftime('%Y-%m-%d %H:%M:%S')),
            "cancel_time": subs_canceled_time,
            "plan": stripe_obj.get("items")["data"][0].get("plan").get("interval"),
            "subscription": rele_obj.get("subscription", "None"),
            "runtimestamp": str(datetime.now()),
            })
    df = pd.read_json(json.dumps(releai_client_object))
    t1 = time.time()
    total_time = t1 - t0
    print(total_time)
    return df

def main():
    '''
    write the result into biqQuery
    '''
    from google.cloud import bigquery
    time_now = str(datetime.now()).split(".")[0]
    stripe_full_info = stripe(get_list())
    if os.environ["GOOGLE_APPLICATION_CREDENTIALS"] == "/etc/releai/keys/releai-bot-prod.json":
        client = bigquery.Client(project="releai-bot-prod")
    else:
        client = bigquery.Client(project="releai-bot-dev")
    client.load_table_from_dataframe(stripe_full_info, destination='orgs_db.subscriptions_db')
    print(stripe_full_info)
    return ({"message": f"writing on to Bq completed {time_now}"})

if __name__ == "__main__":
    main()