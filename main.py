from flask import Flask, request, jsonify
import pandas as pd

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
