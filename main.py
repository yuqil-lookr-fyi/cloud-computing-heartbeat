from flask import Flask, request, jsonify
import pandas as pd
import random
import uuid
from datetime import datetime

app = Flask(__name__)
csv_file = "notifications.csv"


# API to read the top 3 undismissable messages
@app.route("/read_undismissable_messages", methods=["GET"])
def read_undismissable_messages():
    # Get the number of messages to return from the query parameter, defaulting to 3 if not provided
    top_n = request.args.get("top", default=3, type=int)

    df = pd.read_csv(csv_file)
    undismissable_msgs = df[df["dismissable"] == "no"].head(top_n)
    # order by timestamp
    undismissable_msgs = undismissable_msgs.sort_values(by="timestamp", ascending=False)
    return jsonify(undismissable_msgs.to_dict(orient="records"))


# API to upsert a message
@app.route("/upsert", methods=["POST"])
def upsert_message():
    msg_id = request.json["msg_id"]
    content = request.json["content"]
    dismissable = request.json["dismissable"]

    df = pd.read_csv(csv_file)
    index = df.index[df["msg_id"] == msg_id].tolist()

    # Update if exists, otherwise append
    if index:
        df.loc[index[0], "content"] = content
        df.loc[index[0], "dismissable"] = dismissable
    else:
        new_row = pd.DataFrame(
            {"msg_id": [msg_id], "content": [content], "dismissable": [dismissable]}
        )
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(csv_file, index=False)
    return jsonify({"status": "success", "message": "Data updated!"})


# API to read all messages
@app.route("/read_all", methods=["GET"])
def read_all_messages():
    df = pd.read_csv(csv_file)
    return jsonify(df.to_dict(orient="records"))


# API to generate a random new unread message
@app.route("/generate_random", methods=["POST"])
def generate_random_message():
    msg_id = uuid.uuid4()
    content = f"Random Heartbeat Alert: {random.choice(['Normal', 'Irregular', 'High', 'Low'])} bpm"
    dismissable = "no"
    timestamp = datetime.now().isoformat()  # Current timestamp in ISO 8601 format
    new_row = pd.DataFrame(
        {
            "msg_id": [msg_id],
            "content": [content],
            "dismissable": [dismissable],
            "timestamp": [timestamp],
        }
    )

    df = pd.read_csv(csv_file)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_file, index=False)
    return jsonify(
        {"status": "success", "message": f"Random message generated with ID {msg_id}"}
    )


# API to delete messages
@app.route("/delete", methods=["DELETE"])
def delete_messages():
    msg_ids = request.json.get("msg_ids", None)
    df = pd.read_csv(csv_file)

    if msg_ids:
        df = df[~df["msg_id"].isin(msg_ids)]
    else:
        df = df.iloc[0:0]  # Clear all data

    df.to_csv(csv_file, index=False)
    # return what messages are deleted
    return jsonify(
        {"status": "success", "message": f"Messages with ID {msg_ids} deleted!"}
    )


# API to toggle the dismissable status of a message by its ID
@app.route("/toggle_dismissable", methods=["POST"])
def toggle_dismissable():
    msg_id = request.json["msg_id"]

    df = pd.read_csv(csv_file)
    if msg_id in df["msg_id"].values:
        current_value = df.loc[df["msg_id"] == msg_id, "dismissable"].iloc[0]
        new_value = "no" if current_value == "yes" else "yes"
        df.loc[df["msg_id"] == msg_id, "dismissable"] = new_value
        df.to_csv(csv_file, index=False)
        return jsonify(
            {
                "status": "success",
                "message": f"Dismissable status for message ID {msg_id} toggled to {new_value}",
            }
        )
    else:
        return jsonify({"status": "error", "message": "Message ID not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
