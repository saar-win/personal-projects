DOMAIN=http://saar.rele.ai

# Math service
```
DOMAIN=http://saar.rele.ai
curl -x POST \
    -H "Content-Type: application/json" \
    -d '{"data": [2, 1, 3]}' \
    $DOMAIN/api/v1/math/sort

# returns -> [1, 2, 3]
```
```
DOMAIN=http://saar.rele.ai
curl -x POST \
    -H "Content-Type: application/json" \
    -d '{"a": 1, "b": 2}' \
    $DOMAIN/api/v1/math/sum

# returns -> 3
```
# Audit service
```
DOMAIN=http://saar.rele.ai
curl -x POST \
    -H "Content-Type: application/json" \
    -d '{"ip": "127.1.1.1", "operation": "sum"}' \
    $DOMAIN/api/v1/audit

# returns -> OK
```
```
DOMAIN=http://saar.rele.ai
curl "$DOMAIN/api/v1/audit?limit=20"

# returns -> [{"ip": "", "operation": "", "timestamp": ""}, {...}, {...}]
```