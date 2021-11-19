# google123:Releai12!@#
import json, os
import flask, hashlib, base64
from datetime import datetime
from datetime import timedelta, timezone
from flask import Flask, request, jsonify
from discord import Webhook, RequestsWebhookAdapter
from google.cloud import logging
from google.cloud.logging import DESCENDING
import firebase_admin
from firebase_admin import firestore, credentials
import sys

app = flask.Flask(__name__)
error_table = {
    200: (({"message":"Done !!"}), 200),
    401: (({"message":"Unauthorized access !!"}), 401),
    404: (({"message":"Payload Error!!"}), 404),
    400: (({"message":"Payload Error!!"}), 400),
}
def auth_fun():
    '''
    check if it's a valid requset
    '''
    if request.method == "POST":
        req_headers = dict(flask.request.headers)
        headers = flask.request.headers
        users = {f"{os.environ['GOOGLE_USER']}": f"{os.environ['GOOGLE_PASS']}"}
        accept_headers = {
            "User-Agent": "Google-Alerts",
            "Content-Type": "application/json",
            "Authorization": f"Basic {os.environ['GOOGLE_AUTH']}"
        }
        new_req_header = {}
        for key, val in req_headers.items():
            x = {key:val}
            if key in accept_headers:
                new_req_header.update(x)
        if new_req_header == accept_headers:
            token_type, b64token = headers['Authorization'].split(" ")
            if token_type == "Basic":
                value = base64.b64decode(b64token)
                username, password = value.split(b':')
                sha256pass = users.get(username.decode('utf-8'))
                if sha256pass and hashlib.sha256(password).hexdigest() == sha256pass:
                    try:
                        return error_table.get(200)
                    except Exception as e:
                        print(e)
                        return error_table.get(404)
                else:
                    return error_table.get(401)
            else:
                return error_table.get(401)
        else:
            return error_table.get(401)
    else:
        return error_table.get(401)

@app.route("/api/v1/discord/logging", methods=["POST"])
def _logging():
    '''
    Collect the all logs and send it throgh notification channel
    '''
    auth = auth_fun()
    if auth[1] == 200:
        data = flask.request.data
        x = json.loads(data.decode("utf-8"))
        print(x)
        for _, val in x.items():
            if len(val) > 10:
                time_now = datetime.now(timezone.utc)
                last_minutes = time_now - timedelta(minutes=10)
                now = time_now.isoformat().split(".")[0]+"Z"
                before = last_minutes.isoformat().split(".")[0]+"Z"
                project_id = val['resource']['labels'].get("project_id")
                get_env(project_id)
                try:
                    details, link  = val['summary'].split(' '), val['url']
                    err_service = val['summary'].split('/')[2].split("_")[0]
                    err, project= details[0], details[2]
                except Exception as e:
                    discord_send_message(title=project_id, error="I got a service error")
                print("go to get logs")
                DEC_FILTER = f'resource.type="k8s_container" AND resource.labels.cluster_name="{env_ms_name}" AND labels.k8s-pod/app="{err_service.split("_")[0]}" AND timestamp >= "{before}" AND timestamp <= "{now}" AND "error" AND NOT "(node:1) Warning:" AND NOT "userExecuterInfo" '
                _list = get_logs(DEC_FILTER, project_id)
                # print(_list)
                DEC_USER_FILTER = f'resource.type="k8s_container" AND resource.labels.cluster_name="{env_ms_name}" AND labels.k8s-pod/app="{err_service.split("_")[0]}" AND timestamp >= "{before}" AND timestamp <= "{now}" AND "error" AND "userExecuterInfo" AND NOT "(node:1) Warning:" '
                user_executer_info_fun = get_logs(DEC_USER_FILTER, project_id)
                if len(user_executer_info_fun) != 0:
                    user_executer_info = json.loads(user_executer_info_fun[0].split('userExecuterInfo:')[1])
                    userFsId = user_executer_info.get("userFsid")
                    orgId = user_executer_info.get("orgId")
                    print("user_info: ", user_executer_info)
                    print("userFsId: ", userFsId)
                    print("orgId: ", orgId)
                    if len(_list) >= 3:
                        print("len is greater then 3")
                        err1, err2, err3 = _list[0], _list[1], _list[2]
                        discord_send_message(title=project, error=err, message="1. " + err1 + "\n2. " + err2 + "\n3. " + err3 + "\n" + userFsId + "\n" + orgId)
                    if len(_list) >= 2:
                        print("len is greater then 2")
                        err1, err2 = _list[0], _list[1]
                        discord_send_message(title=project, error=err, message="1. " + err1 + "\n2. " + err2 + "\n" + userFsId + "\n" + orgId)
                    if len(_list) == 1 & len(user_executer_info_fun) !=0:
                        print("len is 1")
                        err1 = _list[0]
                        discord_send_message(title=project, error=err, message="1." + err1 + "\n" + userFsId + "\n" + orgId)
                    if len(_list) == 0:
                        print("len is 0")
                        discord_send_message(title=project_id, error=err, message="This is user details:" + userFsId + "\n" + orgId)
                    else:
                        discord_send_message(title=project_id, error="I got a service error", message=link)
                else:
                    discord_send_message(title=project_id, error="I got a service error", message=link)
                return auth
            else:
                return jsonify({"message": "got an error"}, 400)
    else:
        return auth
@app.route("/api/v1/discord/payments", methods=["POST"])
def payment():
    '''
    Once we get a new payment the script will send a notification
    '''
    auth = auth_fun()
    if auth[1] == 200:
        data = flask.request.data
        print(data)
        try:
            x = json.loads(data.decode("utf-8"))
        except Exception as e:
            print("got an error when trying to do json loads ", e)
            return error_table.get(400)
        for key, val in x.items():
            if len(val) > 10:
                time_now = datetime.now(timezone.utc)
                last_minutes = time_now - timedelta(minutes=10)
                now = time_now.isoformat().split(".")[0]+"Z"
                before = last_minutes.isoformat().split(".")[0]+"Z"
                project_id = val['resource']['labels'].get("project_id")
                get_env(project_id)
                title = val['policy_name']
                print("go to get logs")
                function_name = "stripeWebhook"
                DEC_FILTER = f'resource.type="cloud_function" AND resource.labels.function_name="{function_name}" AND resource.labels.region="us-central1" AND timestamp >= "{before}" AND timestamp <= "{now}" AND "Payment action succeeded notify"'
                _list = get_logs(DEC_FILTER, project_id)
                cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
                firebase_admin.initialize_app(cred)
                store = firestore.client()
                try:
                    org_id = _list[0].split(' ')[4]
                    org_name = store.collection("orgs").document(org_id).get().to_dict()["name"]
                    print("orgId: ", org_id)
                    print("orgName: ", org_name)
                    discord_send_message(title=project_id, error=title, message=f"We've a new customer!\norgName: '{org_name}'\norgId: '{org_id}'\n")
                except Exception as e:
                    print("got an error when trying to get orgId, orgName", e)
                    discord_send_message(title=project_id, error=title, message=f"We've a new customer!\n")
                return auth
            else:
                return ""
    else:
        return auth

def get_env(project_id):
    '''
    defines the env.
    '''
    global env_ms_name
    if project_id == "releai-bot-dev":
        env_ms_name = "bot-ms-1"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/etc/releai/keys/releai-bot-dev.json"
    else:
        env_ms_name = "bot-ms"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/etc/releai/keys/releai-bot-prod.json"

def get_logs(DEC_FILTER, _):
    '''
    get the logs from google logging
    '''
    print("get_logs function")
    _list = []
    FILTER = DEC_FILTER
    logging_client = logging.Client()
    for entry in logging_client.list_entries(order_by=DESCENDING, filter_=FILTER):
        _list.append(entry.payload)
    return _list

def workdays():
    '''
    check if this is workDays
    '''
    print("check workdays function")
    import datetime
    start = datetime.time(8, 0, 0)
    end = datetime.time(20, 0, 0)
    today = datetime.datetime.strptime('January 11, 2010', '%B %d, %Y').strftime('%A')
    workdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    time_now = datetime.datetime.now().time()
    if time_now <= start or time_now <= end and today in workdays:
        print("this is a workday!, true")
        return True
    else:
        print("this is not a workday!, false")
        return False

def discord_send_message(title, error, message):
    '''
    Discord API
    '''
    print("discord send message function")
    currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
    # import datetime
    # time_now = datetime.datetime.now().time()
    print("came from: ", currentFuncName(1))
    if workdays() == True:
        if currentFuncName(1) == "payment":
            webhook = f"{os.environ['RELE_PAYMENTS']}" # rele-payments-channel
        if currentFuncName(1) == "_logging":
            # webhook = f"{os.environ['SAAR_LOGGING']}" # saar-logging-channel
            webhook = f"{os.environ['RELE_LOGGING']}" # rele-logging-channel
        if currentFuncName(1) == "github_webhook":
            webhook = f"{os.environ['RELE_LOGGING']}" # rele-logging-channel
        init = Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())
        init.send("\n\n\n\n" + "**" + title + "\n**" + "``" + error +  "\n" + message + "``" + "\n\n\n\n")
    else:
        return "is'nt workdays"

@app.route("/api/v1/discord/github", methods=["POST"])
def github_webhook():
    '''
    Feature function.
    When we have a new PR \ merge
    or when deleted branch
    the script will send notify
    '''
    # auth = auth_fun()
    headers = flask.request.headers
    print(headers)
    # if auth[1] == 200:
        # data = json.loads(flask.request.data.decode("utf-8"))
        # print("This is TEST !!", data.get('sender').get('login'))
        # # print(type(data))
        # if data.get("deleted") == True:
        #     discord_send_message(title="Branch deleted", error=f"Branch Name: {data.get('ref')}", message=f'Executor Name: {data.get("sender").get("login")}')
        # ##
        # if data.get("created") == True:
        #     discord_send_message(title="New Branch created", error=f"Branch Name: {data.get('ref')}", message=f'Executor Name: {data.get("sender").get("login")}')
    # return auth
    # return jsonify({ data })
    #     # try:
    #         x = json.loads(data.decode("utf-8"))
    #     except Exception as e:
    #         return error_table.get(400)
    #     for key, val in x.items():
    #         if len(val) > 10:

    #             return auth
    #         else:
    #             return ""
    # else:
    #     return auth

if __name__ == '__main__':
    app.run(debug=True)
    # main()
    # get_env()
    # get_logs("salesforce_ads_asd")
# ENV to set:
#   google application cred
#   env "ENV"
#   env "BUCKET_NAME"
#   env "FLASK_RUN_PORT"
#   env "FLASK_APP"