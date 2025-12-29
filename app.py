from flask import Flask, render_template, request
import os
import joblib
import numpy as np

app = Flask(__name__)

MODEL_DIR = "models"

try:
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))
    rf_model = joblib.load(os.path.join(MODEL_DIR, "rf_water_potability_tuned.joblib"))
    svm_model = joblib.load(
        os.path.join(MODEL_DIR, "svm_water_potability_tuned.joblib")
    )
except Exception as e:
    print(f"Error loading models: {e}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            input_features = [
                float(request.form["ph"]),
                float(request.form["Hardness"]),
                float(request.form["Solids"]),
                float(request.form["Chloramines"]),
                float(request.form["Sulfate"]),
                float(request.form["Conductivity"]),
                float(request.form["Organic_carbon"]),
                float(request.form["Trihalomethanes"]),
                float(request.form["Turbidity"]),
            ]
            features_array = np.array([input_features])
            features_scaled = scaler.transform(features_array)
            selected_model_name = request.form["model_choice"]

            if selected_model_name == "svm":
                prediction = svm_model.predict(features_scaled)
                model_used = "Support Vector Machine (SVM)"
            else:
                prediction = rf_model.predict(features_scaled)
                model_used = "Random Forest"

            if prediction[0] == 1:
                result_text = "Layak Minum (Potable)"
                result_color = "green"
            else:
                result_text = "Tidak Layak Minum (Not Potable)"
                result_color = "red"

            return render_template(
                "index.html",
                prediction_text=result_text,
                color=result_color,
                model_used=model_used,
                form_data=request.form,
            )

        except Exception as e:
            return render_template(
                "index.html",
                prediction_text=f"Error: {str(e)}",
                color="black",
                form_data=request.form,
            )


if __name__ == "__main__":
    app.run(debug=True)
