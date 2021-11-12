# This is the first script control by post request
#
1. The function backup the firestore database collections.
2. Uses FireStore import-export.
3. At the end of the process, all the JSON files upload to the bucket.
# Example to post request:

**Header type:**
```
    Authorization value in base64.
```
**Body type:**
```
    key: string (have to contains "env")
    value: string (have to contains "keyword")
```
```
url = "http://localhost:5002/api/v1/backup"
curl -X POST $url \
    -H "User-Agent: Releai" \
    -H "Content-Type: application/json" \
    -H "Authorization: Basic THIS_IS_FAKE==" \
    -d '{"env":"dev"}'
```
