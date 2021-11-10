import collections
import json, os
import pandas as pd
import gspread, requests
import firebase_admin
from firebase_admin import firestore, credentials


tabs_list = {
  "tab1": [ "500.1", "500.2", "500.3", "500.4", "500.5", "500.6", "500.7", "500.8", "500.9", "500.10" ],
  "tab2": [ "500.12", "500.13", "500.14", "500.15", "500.16", "500.17", "500.18", "500.19", "500.20" ],
  "tab3": [ "500.21", "500.22", "500.23", "500.24", "500.25", "500.26", "500.27", "500.28", "500.29", "500.30" ],
  "tab4": [ "500.31", "500.32", "500.33", "500.34", "500.35", "500.36", "500.37", "500.38", "500.39", "500.40" ]
}
tabs = {
    "tab1": [ "500.1" ],
    "tab2": [ "500.2" ],
    "tab3": [ "500.3" ],
    "tab4": [ "500.4" ],
    "tab5": [ "500.5" ],
    "tab6": [ "500.6" ],
    "tab7": [ "500.7" ],
    "tab8": [ "500.8" ],
    "tab9": [ "500.9" ],
    "tab10": [ "500.10" ],
    "tabs12": [ "500.12" ],
    "tabs13": [ "500.13" ],
    "tabs14": [ "500.14" ],
    "tabs15": [ "500.15" ],
    "tabs16": [ "500.16" ],
    "tabs17": [ "500.17" ],
    "tabs18": [ "500.18" ],
    "tabs19": [ "500.19" ],
    "tabs20": [ "500.20" ],
    "tabs21": [ "500.21" ],
    "tabs22": [ "500.22" ],
    "tabs23": [ "500.23" ],
    "tabs24": [ "500.24" ],
    "tabs25": [ "500.25" ],
    "tabs26": [ "500.26" ],
    "tabs27": [ "500.27" ],
    "tabs28": [ "500.28" ],
    "tabs29": [ "500.29" ],
    "tabs30": [ "500.30" ],
    "tabs31": [ "500.31" ],
    "tabs32": [ "500.32" ],
    "tabs33": [ "500.33" ],
    "tabs34": [ "500.34" ],
    "tabs35": [ "500.35" ],
    "tabs36": [ "500.36" ],
    "tabs37": [ "500.37" ],
    "tabs38": [ "500.38" ],
    "tabs39": [ "500.39" ],
    "tabs40": [ "500.40" ]
}

os.environ['ORG_ID'] = "rNNVkDjjxLkBzjxVZTr8"
cred = credentials.Certificate(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
firebase_admin.initialize_app(cred)
store = firestore.client()

def check_the_nubmer(tab):
    '''
    Append the from spreadsheet numbers to list.
    return the list.
    '''
    gc = gspread.service_account(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
    spreadsheet_id = '14QSQa0LtmdAdTLBWswmr_P-d1V_FtOjZ-_OTChNbu6U'
    sh = gc.open_by_key(spreadsheet_id)
    wsheet = sh.worksheet(tab)
    dataframe = pd.DataFrame(wsheet.get_all_records())
    list_numbers = []
    for number in dataframe['mobile']:
        list_numbers.append(f"+{number}")
    return json.dumps(list_numbers)

def check_valid(numbers):
    '''
    Build a curl commnad,
    send the command to whatsapp api
    '''
    url = "https://waba.messagepipe.io/v1/contacts"
    headers = {
      "D360-API-KEY": f"{os.environ['WHATSAPP_KEY']}",
      "Content-Type": "application/json"
    }
    n = f'{numbers}'
    d = ', "blocking":"wait","force_check": true'
    data = '{"contacts":' + f'{n}' + f'{d}'+"}"
    command = requests.post(url, headers=headers, data=data)
    user = json.loads(command.text).get("contacts")
    numbers_len = len(user)
    invalid_numbers = []
    for index in range(0, numbers_len):
      if user[index]['status'] == "invalid" or user[index]['status'] == "processing":
        x = { "nubmer": user[index]['input'], "status": user[index]['status'] }
        invalid_numbers.append(x)
    return invalid_numbers

def write_to_spreadseets(nubmers, tab_name):
  '''
  Get the tab name
  Get the numbers from the tab
  Write to G-spread
  '''
  gc = gspread.service_account(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
  spreadsheet_id = '14QSQa0LtmdAdTLBWswmr_P-d1V_FtOjZ-_OTChNbu6U'
  sh = gc.open_by_key(spreadsheet_id)
  _sorted = pd.read_json(json.dumps(nubmers))
  values = _sorted.values.tolist()
  sh.values_append(tab_name,
  params = {
      'valueInputOption': 'USER_ENTERED',
      'responseValueRenderOption': 'UNFORMATTED_VALUE',
      },
  body={
      "values": values,
      'majorDimension':'ROWS',
      })

def find_duplicates(numbers):
    '''
    Get list of numbers
    Check if there is a duplicats numbers in list
    '''
    duplicats = []
    x = collections.Counter(json.loads(numbers))
    for number, count in x.items():
      if count != 1:
        x = { "number": number, "count": count }
        duplicats.append(x)
    return duplicats


def users_from_db():
    '''
    Get the user informations from db
    '''
    try:
      count = 0
      result, valid_users = ([] for i in range(2))
      for user in store.collection("users").where("orgs", "array_contains", f"{os.environ['ORG_ID']}").get():
        doc = user.to_dict()
        user_obj = {
          "first_name": doc.get('first_name', "None"),
          "last_name":  doc.get('last_name',"None"),
          "mobile":  doc.get('mobiles', 'None')[0],
          "emails":  doc.get('emails', 'None')[0]
          }
        count += 1
        valid_users.append(user_obj)
        if count == 1000:
          count = 0
          result.append(valid_users)
          valid_users = []
      if count > 0:
        result.append(valid_users)

      return result
    except Exception as e:
      print(e)

def main():
    '''
    for loop for every tab
    '''
    ## for duplicats numbers
    # for tab in tabs.values():
    #   for t in tabs:
    #     numbers = check_the_nubmer(tab[0])
    #     duplicats_numbers = find_duplicates(numbers)
    #     write_to_spreadseets(duplicats_numbers, tab_name = "duplicats")

    # ## for valid numbers
    # valid_users = users_from_db()
    # for number in valid_users:
    #   write_to_spreadseets(number, tab_name = "valid_nubmers")
    #   time.sleep(5)

    # for check number against 360dialog
    # for tab in tabs.values():
    #   numbers = check_the_nubmer(tab)
    #   invalid_numbers = check_valid(numbers)
    #   write_to_spreadseets(invalid_numbers, tab_name = "invalid_numbers")
    #   time.sleep(5)

if __name__ == "__main__":
    main()
