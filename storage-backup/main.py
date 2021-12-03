import shutil, base64
import os, subprocess
import flask, hashlib
from flask import Flask, request, jsonify
from datetime import datetime, date
from google.cloud import storage

# from app import server

_dir = f"./{str(date.today())}"
collection_list = [ "apps", "workflows", "operations", "app_actions", "users", "orgs", "versions", "translations" ]
app = flask.Flask(__name__)
#
error_table = {
    200: (({"message":"Done !!"}), 200),
    401: (({"message":"Unauthorized access !!"}), 401),
    400: ({"":""}),
    404: (({"message":"Payload Error!!"}), 404),
}
@app.route("/api/v1/backup", methods=["POST"])
def auth_fun():
    if request.method == "POST":
        req_headers = dict(flask.request.headers)
        headers = flask.request.headers
        users = {f"{os.environ['USER_NAME']}": f"{os.environ['USER_PASS']}"}
        accept_headers = {
            "User-Agent": "Releai",
            "Content-Type": "application/json",
            "Authorization": f"Basic {os.environ['AUTH_HEADER']}",
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
                    req = request.get_json()
                    env = req['env']
                    if env in ["dev","prod"]:
                        link = upload_to_bucket(env) ## move forward inside !
                        return jsonify({"message": link})
                        # return error_table.get(200)
                    else:
                        return error_table.get(404)
                else:
                    return error_table.get(401)
            else:
                return error_table.get(401)
        else:
            return error_table.get(401)
    else:
        return error_table.get(401)

def defines_env(env):
    '''
    '''
    if env == "dev":
        print("dev")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/releai/keys/releai-bot-dev.json"
        subprocess.run(f"gcloud auth activate-service-account --key-file=/etc/releai/keys/releai-bot-dev.json",shell=True)
        os.environ['BUCKET_NAME'] = "database_backup_rb"
    if env == "prod":
        print("prod")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/releai/keys/releai-bot-prod.json"
        subprocess.run(f"gcloud auth activate-service-account --key-file=/etc/releai/keys/releai-bot-prod.json",shell=True)
        os.environ['BUCKET_NAME'] = "prod_database_backup_rb"

def create_backup():
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    for col in collection_list:
        subprocess.run(f'firestore-export -a {os.environ["GOOGLE_APPLICATION_CREDENTIALS"]} -b "{_dir}/{col}.json" -n "{col}"', shell=True)
    print("Done")

def upload_to_bucket(env):
    '''
    '''
    env = defines_env(env)
    create_backup()
    storage_client = storage.Client()
    if storage_client.get_bucket(os.environ['BUCKET_NAME']).exists():
        print(f"OK, Found {os.environ['BUCKET_NAME']} bucket")
        if os.path.exists(_dir):
            for col in collection_list:
                subprocess.run(f"gsutil cp {_dir}/{col}.json gs://{os.environ['BUCKET_NAME']}/{str(date.today())}/{col}.json", shell=True)
                # bucket = storage_client.get_bucket(os.environ['BUCKET_NAME'])
                # blob = bucket.blob(f"{_dir}/{col}.json")
                # with open(f"{_dir}/{col}.json", 'rb') as json_file:
                #     print("uploading", col, "to bucket")
                #     blob.upload_from_file(json_file)
        else:
            print("But I haven't the dir")
        if os.path.exists(_dir):
            print(f"Removing {_dir}")
            shutil.rmtree(_dir)
    return f"https://console.cloud.google.com/storage/browser/{os.environ['BUCKET_NAME']}/{str(date.today())}"
if __name__ == '__main__':
    app.run(debug=True)
    # upload_to_bucket(env="dev")