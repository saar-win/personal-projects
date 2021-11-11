# This script checks against the Stripe API the subscription key
# and gets back from them the information about the plan of the client.

1. get the subscription list from the Firestore.
2. send to stripe the information about the client.
3. write the information to biqQuery within right structure after formatting.