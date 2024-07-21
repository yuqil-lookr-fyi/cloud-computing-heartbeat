# Test

```shell
curl -X GET http://100.28.74.221:5000/read

curl -X POST http://100.28.74.221:5000/upsert \
-H "Content-Type: application/json" \
-d '{"msg_id": 2, "content": "Alert: Heart rate irregularity detected", "dismissable": "yes"}'

curl -X POST http://100.28.74.221:5000/generate_random

curl -X GET http://100.28.74.221:5000/read_all

curl -X DELETE http://100.28.74.221:5000/delete \
-H "Content-Type: application/json" \
-d '{"msg_ids": [2, 3]}'

curl -X DELETE http://100.28.74.221:5000/delete \
-H "Content-Type: application/json" \
-d '{}'
```
