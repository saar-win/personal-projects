import socket, gspread, ssl
import datetime, os
import json as JSON
import discord
import pandas as pd
from flask import Flask, jsonify
from discord import Webhook, RequestsWebhookAdapter

app = Flask(__name__)

domains_url = [
"console.rele.ai",
"console.dev.bot.rele.ai",
"wa-agent.dev.bot.rele.ai",
"wa-agent.prod.bot.rele.ai",
"integrations-gw.dev.bot.rele.ai",
"integrations-gw.prod.bot.rele.ai",
"cognition-gw.dev.bot.rele.ai",
"cognition-gw.prod.bot.rele.ai",
"frontend-proxy.dev.bot.rele.ai",
"frontend-proxy.prod.bot.rele.ai",
"whatsapp.prod.bot.rele.ai",
"whatsapp.dev.bot.rele.ai",
]

def ssl_expiry_datetime(url):
    '''
    Get the all information about the url.
    '''
    ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    context.check_hostname = False
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=url,
    )
    # 5 second timeout
    conn.settimeout(5.0)
    conn.connect((url, 443))
    ssl_info = conn.getpeercert()
    # Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_dateformat)

def convert_datetime(o):
    '''
    format datetime
    '''
    if isinstance(o, datetime):
        return o.__str__()

def domains_information():
    '''
    The functions returns information about the url
    from the list to one big list
    '''
    _list = []
    now = datetime.datetime.now()
    date_today = datetime.datetime.now().strftime("%d-%m-%Y")
    time_now = datetime.datetime.now().strftime("%H:%M")
    for value in domains_url:
        try:
            url_info = ssl_expiry_datetime(value)
            expiry_date = url_info.strftime("%d-%m-%Y")
            diff = url_info - now
            days = str(diff).split(',')[0]
            expiry_day = days.split(' ')[0]
            _list.append({
                "domain": value,
                "expiry_date": expiry_date,
                "expiry_day": expiry_day,
                "run_datestamp": date_today,
                "run_timestamp": time_now
            })
        except Exception as e:
            print (e)
    full_info = JSON.dumps(_list)
    return full_info

@app.route('/api/v1/ssl')
def write_to_spreadsheets():
    '''
    GspreadSheets API
    Write and read
    '''
    gc = gspread.service_account(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    ########################
    # spreadsheet id
    dev = '1YLvVkbtakDg8RJ-3EHVXhwcHtxYSiSudSxPm9VhxxkM'
    time_now = datetime.datetime.now().strftime("%d-%m-%Y")
    # spreadsheet defined
    sh = gc.open_by_key(dev)
    ########################
    wsheet = sh.worksheet("ssl")
    dataframe = pd.DataFrame(wsheet.get_all_records())
    csv, _json = ([] for i in range(2))
    _list = domains_information()
    _sorted = pd.read_json(_list)
    x = JSON.loads(_list)
    ##
    title = [_sorted.columns.to_list()]
    values = _sorted.values.tolist()
    for (csv_domain ,csv_days) in zip(dataframe[0:10]["Domain"], dataframe[0:10]["Expiry_Day"]):
        csv.append({"domain": csv_domain, "days": csv_days })
    for row in x:
        _json.append({ "domain": row["Domain"], "days": int(row["Expiry_Day"])})
    for (_json), (csv) in zip(_json, csv):
        if _json["days"] > csv["days"]:
            discord_send_message(title=f"Hey i got renewal for certificate:", message=f"{_json['domain']} \nwas: {csv['days']} days, now: {_json['days']} days\n\n")
    sh.values_update('ssl',
    params = {
        'valueInputOption': 'USER_ENTERED',
        'responseValueRenderOption': 'UNFORMATTED_VALUE',
        },
    body={
        "values": title + values,
        'majorDimension':'ROWS',
        })
    check_domain_days()
    return jsonify ({"message": f'write to spreadsheets complete {time_now}'})

def workdays():
    '''
    Check if is a workDay?
    '''
    work_start_time = datetime.time(9, 0, 0)
    work_end_time = datetime.time(19, 0, 0)
    day_today = datetime.datetime.strptime('January 11, 2010', '%B %d, %Y').strftime('%A')
    time_now = datetime.datetime.now().time()
    workdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
    if time_now <= work_start_time or time_now <= work_end_time and day_today in workdays:
        return True
    else:
        return False

@app.route('/api/v1/discord')
def discord_send_message(message, title):
    '''
    Discord API
    '''
    # time_now = datetime.datetime.now().time()
    if workdays() == True:
        webhook = "https://discord.com/api/webhooks/836502024433958962/aEZntH_dyB9DGSSG4YAdXkl1ymUKq_PYKNc6khaSoMwckQqKeIgUDtDHe3y937cwwe7k" # ssl-rele-channel
        # webhook = "https://discord.com/api/webhooks/834880767314231317/DJAYy1LKvUABIgPGJDRmrkic7AbWTzCg09kwArvwbkToe_pwE8HQWw7cw-uWKZPExnyi" # saar-channel
        _discord = Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())
        _discord.send("\n\n" + "**" + title + "\n**" + "``" + message + "``" + "\n\n")
    else:
        return jsonify ({"message": "is'nt workdays"})

def check_domain_days():
    '''
    Check if domain days lower than 16 Days
    '''
    json = domains_information()
    _list = JSON.loads(json)
    for url in _list:
        if int(domain["expiry_day"]) <= 16:
            domain, expiry_day, expiry_date = url["domain"], url["expiry_day"], url["expiry_date"]
            discord_send_message(title=f"Pay attention",message=f"{domain} expiry in: {expiry_day} days on {expiry_date}\nsend request to renewal !!\n\n")
        else:
            pass

if __name__ == "__main__":
    app.run(debug=True, port=5051)
    # main_fun()
    # renewal_happend()
    # write_to_spreadsheets()