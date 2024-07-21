from flask import Flask, request, jsonify
import pandas as pd
import random

app = Flask(__name__)
csv_file = "notifications.csv"


# API to read all undismissable messages
@app.route("/read", methods=["GET"])
def read_messages():
    df = pd.read_csv(csv_file)
    undismissable_msgs = df[df["dismissable"] == "no"]
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
    msg_id = random.randint(100, 999)  # Generate a random message ID
    content = f"Random Heartbeat Alert: {random.choice(['Normal', 'Irregular', 'High', 'Low'])} bpm"
    dismissable = "no"
    new_row = pd.DataFrame(
        {"msg_id": [msg_id], "content": [content], "dismissable": [dismissable]}
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
