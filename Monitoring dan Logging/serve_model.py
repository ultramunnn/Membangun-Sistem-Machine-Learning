import mlflow.pyfunc
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

model_uri = "D:/dicoding/Membangun-Sistem-Machine-Learning/mlruns/0/b54092687e9947b4a5d871ba295e2615/artifacts/model"
model = mlflow.pyfunc.load_model(model_uri)

@app.route("/invocations", methods=["POST"])
def predict():
    input_data = request.get_json()
    df = pd.DataFrame(input_data["dataframe_split"]["data"], columns=input_data["dataframe_split"]["columns"])
    predictions = model.predict(df)
    return jsonify({"predictions": predictions.tolist()})

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
