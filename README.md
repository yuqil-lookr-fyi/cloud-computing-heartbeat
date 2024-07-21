# Test

```shell
# Generate a random new unread message
curl -X POST http://100.28.74.221:5000/generate_random

# Read the top 3 undismissable messages, by default it return top 3
curl -X GET http://100.28.74.221:5000/read_undismissable_messages

# But you can return custom top N
curl -X GET http://100.28.74.221:5000/read_undismissable_messages?top=4

# Toggle the dismissable status of message with msg_id 36e6e0f5-5206-4022-b28c-dacde30b8749
curl -X POST http://100.28.74.221:5000/toggle_dismissable \
-H "Content-Type: application/json" \
-d '{"msg_id": "36e6e0f5-5206-4022-b28c-dacde30b8749"}'

# Read all messages
curl -X GET http://100.28.74.221:5000/read_all

# Delete specific messages with msg_ids 2 and 3
curl -X DELETE http://100.28.74.221:5000/delete \
-H "Content-Type: application/json" \
-d '{"msg_ids": [..., ...]}'

# Read all messages to verify deletion
curl -X GET http://100.28.74.221:5000/read_all

# Delete all messages
curl -X DELETE http://100.28.74.221:5000/delete \
-H "Content-Type: application/json" \
-d '{}'

# Read all messages to confirm all are deleted
curl -X GET http://100.28.74.221:5000/read_all

```
