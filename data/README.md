# This is Data driven made for RELE.AI
#
1. The script collects all movement of last 24 hours from RELE.AI services.
2. Every log from every service gets an id, and is associated with the right org and right user from DB
3. Once in 24 hours the data is written to the bigquery by the call to the endpoint