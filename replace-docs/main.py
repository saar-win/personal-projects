from tqdm import tqdm
import os, firebase_admin
from firebase_admin import firestore, credentials


###################################
collections = [ "operations", "translations", "workflows", "apps", "app_actions" ]
###################################

def get_global_operations(dev_db):
    '''
    This function create lists with all the global operations from dev env
    and return it to other functions.
    '''
    operation_lists = { "operations": {}, "translations": {}, "workflows": {}, "apps": {}, "app_actions": {} }
    for docs, col in zip(operation_lists.values(), collections):
        for doc in dev_db.collection(col).where(u'org', '==', 'global').get():
          docs[doc.id] = doc.to_dict()
    return operation_lists

def replace_operations(dev_globals_db, prod_db):
    '''
    Take the global operation and
    replace the docs on prod env.
    '''
    is_passed = True
    counter_passed = 0
    counter_failed = 0
    docs_exception = []
    for collection in collections:
      print(collection, "On replacing")
      for doc_id, doc_val in tqdm(dev_globals_db.get(collection).items()):
        try:
          counter_passed += 1
          prod_db.collection(collection).document(doc_id).set(doc_val)
        except Exception as e:
          counter_failed += 1
          is_passed = False
          print("I've got an err", e)
          docs_exception.append({ collection: doc_id })
    if is_passed:
      print(counter_passed, "Docs was replaced")
      print(f"The collections was replaced")
    else:
      print(counter_failed, "Docs was failed")
      print(f"There is a problem with one of the collections", docs_exception)

def check_os():
    '''
    check the os kind (made for test environment)
    '''
    if os.path.exists("/etc/releai/keys/releai-bot-dev.json"):
      print("Mac / Linux environment !")
      _creds = {
        "GOOGLE_APPLICATION_CREDENTIALS": "/etc/releai/keys/releai-bot-dev.json",
        "GOOGLE_APPLICATION_CREDENTIALS_PROD": "/etc/releai/keys/rele-test-2.json"
      }
    else:
      print("Github Actions environment !")
      _creds = {
        "GOOGLE_APPLICATION_CREDENTIALS": "/home/runner/work/rb/rb/ops/keys/releai-bot-dev.json",
        "GOOGLE_APPLICATION_CREDENTIALS_PROD": "/home/runner/work/rb/rb/ops/keys/releai-bot-prod.json"
      }
    return _creds

def init_fs():
    '''
    initialize the fireStore project
    on 2 parallel environments
    '''
    other_app = firebase_admin.initialize_app(credentials.Certificate(check_os().get("GOOGLE_APPLICATION_CREDENTIALS_PROD")), name="other_app")
    prod_db = firestore.client(other_app)
    ###################################
    default_app = firebase_admin.initialize_app(credentials.Certificate(check_os().get("GOOGLE_APPLICATION_CREDENTIALS")))
    dev_db = firestore.client(default_app)
    return dev_db, prod_db

if __name__ == '__main__':
    dev_db, prod_db = init_fs()
    dev_globals_db = get_global_operations(dev_db)
    replace_operations(dev_globals_db, prod_db)