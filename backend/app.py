import os
import joblib
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

CORS(app)


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

def _find_file(filename):
    candidates = [
        os.path.join(BASE_DIR, filename),
        os.path.join(os.getcwd(), "api", filename),
        os.path.join(os.getcwd(), "backend", filename),
        os.path.join(os.getcwd(), filename),
        os.path.join(os.path.dirname(BASE_DIR), "api", filename),
        os.path.join(os.path.dirname(BASE_DIR), "backend", filename),
        os.path.join(os.path.dirname(BASE_DIR), filename),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]

MODEL_PATH = _find_file("cardio_model.pkl")
SCALER_PATH = _find_file("scaler.pkl")


# ============================================================
# LOAD MODEL
# ============================================================

model = None

try:

    model = joblib.load(
        MODEL_PATH
    )

    print(
        "[+] Model loaded successfully"
    )

    print(
        MODEL_PATH
    )

except Exception as e:

    print(
        "[!] Error loading model:"
    )

    print(e)


# ============================================================
# LOAD SCALER
# ============================================================

scaler = None

try:

    scaler = joblib.load(
        SCALER_PATH
    )

    print(
        "[+] Scaler loaded successfully"
    )

    print(
        SCALER_PATH
    )

except Exception as e:

    print(
        "[!] Error loading scaler:"
    )

    print(e)


# ============================================================
# BMI CALCULATION
# ============================================================

def calculate_bmi(
    height_cm,
    weight_kg
):

    if height_cm <= 0 or weight_kg <= 0:

        return 0.0, "Unknown"


    height_m = (
        height_cm / 100
    )


    bmi = (
        weight_kg /
        (height_m ** 2)
    )


    bmi = round(
        bmi,
        1
    )


    if bmi < 18.5:

        category = "Underweight"

    elif bmi < 25:

        category = "Normal Weight"

    elif bmi < 30:

        category = "Overweight"

    else:

        category = "Obese"


    return bmi, category


# ============================================================
# BLOOD PRESSURE CATEGORY
# ============================================================

def get_bp_category(
    ap_hi,
    ap_lo
):

    if ap_hi < 120 and ap_lo < 80:

        return "Normal Blood Pressure"


    elif (
        120 <= ap_hi <= 129
        and ap_lo < 80
    ):

        return "Elevated Blood Pressure"


    elif (
        130 <= ap_hi <= 139
        or 80 <= ap_lo <= 89
    ):

        return "Hypertension Stage 1"


    elif (
        140 <= ap_hi <= 180
        or 90 <= ap_lo <= 120
    ):

        return "Hypertension Stage 2"


    else:

        return (
            "Hypertensive Crisis - "
            "Consult Doctor Immediately"
        )


# ============================================================
# RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    data,
    prediction_probability,
    bp_category,
    bmi_category
):

    recommendations = []


    # --------------------------------------------------------
    # OVERALL RISK
    # --------------------------------------------------------

    if prediction_probability > 0.5:

        recommendations.append(
            "High overall cardiovascular risk detected. "
            "We recommend scheduling a comprehensive "
            "cardiac health evaluation."
        )

    else:

        recommendations.append(
            "Cardiovascular risk is low. "
            "Maintain healthy habits to preserve "
            "cardiac well-being."
        )


    # --------------------------------------------------------
    # BLOOD PRESSURE
    # --------------------------------------------------------

    if (
        data["ap_hi"] >= 130
        or data["ap_lo"] >= 80
    ):

        recommendations.append(
            f"Blood pressure is elevated "
            f"({bp_category}). Reduce sodium intake, "
            "manage stress, and monitor BP regularly."
        )


    # --------------------------------------------------------
    # CHOLESTEROL
    # --------------------------------------------------------

    if data["cholesterol"] > 1:

        recommendations.append(
            "Elevated cholesterol levels detected. "
            "Limit saturated fats, increase dietary fiber, "
            "and consult a physician."
        )


    # --------------------------------------------------------
    # GLUCOSE
    # --------------------------------------------------------

    if data["gluc"] > 1:

        recommendations.append(
            "Glucose level is above normal. "
            "Limit sugar intake and monitor blood "
            "sugar levels."
        )


    # --------------------------------------------------------
    # SMOKING
    # --------------------------------------------------------

    if data["smoke"] == 1:

        recommendations.append(
            "Smoking significantly increases heart disease "
            "risk. Consider a smoking cessation program."
        )


    # --------------------------------------------------------
    # ALCOHOL
    # --------------------------------------------------------

    if data["alco"] == 1:

        recommendations.append(
            "Alcohol consumption noted. "
            "Moderate or eliminate alcohol to protect "
            "heart health."
        )


    # --------------------------------------------------------
    # PHYSICAL ACTIVITY
    # --------------------------------------------------------

    if data["active"] == 0:

        recommendations.append(
            "Physical activity is low. Aim for at least "
            "150 minutes of moderate aerobic exercise "
            "per week."
        )


    # --------------------------------------------------------
    # BMI
    # --------------------------------------------------------

    if bmi_category in [
        "Overweight",
        "Obese"
    ]:

        recommendations.append(
            f"BMI indicates {bmi_category}. "
            "Adopting a balanced diet and regular exercise "
            "can improve heart health."
        )


    return recommendations


# ============================================================
# HOME ROUTE
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def index():

    return jsonify({

        "status": "online",

        "service":
            "Cardiovascular Disease Prediction API",

        "version":
            "2.0.0",

        "endpoints": {

            "predict":
                "/api/predict (POST)",

            "health":
                "/api/health (GET)"

        }

    })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify({

        "status": "healthy",

        "model_loaded":
            model is not None,

        "scaler_loaded":
            scaler is not None

    })


# ============================================================
# PREDICTION API
# ============================================================

@app.route(
    "/api/predict",
    methods=["POST"]
)
def predict():

    # --------------------------------------------------------
    # CHECK MODEL
    # --------------------------------------------------------

    if (
        model is None
        or scaler is None
    ):

        return jsonify({

            "success": False,

            "error":
                "Model or scaler is not loaded. "
                "Please run train_model.py first."

        }), 500


    try:

        # ----------------------------------------------------
        # GET JSON
        # ----------------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No input JSON data provided."

            }), 400


        # ----------------------------------------------------
        # REQUIRED FIELDS
        # ----------------------------------------------------

        required_fields = [

            "age",
            "gender",
            "height",
            "weight",
            "ap_hi",
            "ap_lo",
            "cholesterol",
            "gluc",
            "smoke",
            "alco",
            "active"

        ]


        missing_fields = [

            field

            for field in required_fields

            if field not in data

        ]


        if missing_fields:

            return jsonify({

                "success": False,

                "error":
                    "Required fields are missing.",

                "missing_fields":
                    missing_fields

            }), 400


        # ----------------------------------------------------
        # CONVERT DATA TYPES
        # ----------------------------------------------------

        age = int(
            data["age"]
        )

        gender = int(
            data["gender"]
        )

        height = float(
            data["height"]
        )

        weight = float(
            data["weight"]
        )

        ap_hi = int(
            data["ap_hi"]
        )

        ap_lo = int(
            data["ap_lo"]
        )

        cholesterol = int(
            data["cholesterol"]
        )

        gluc = int(
            data["gluc"]
        )

        smoke = int(
            data["smoke"]
        )

        alco = int(
            data["alco"]
        )

        active = int(
            data["active"]
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if age <= 0 or age > 120:

            return jsonify({

                "success": False,

                "error":
                    "Age must be between 1 and 120."

            }), 400


        if height <= 0:

            return jsonify({

                "success": False,

                "error":
                    "Height must be greater than 0."

            }), 400


        if weight <= 0:

            return jsonify({

                "success": False,

                "error":
                    "Weight must be greater than 0."

            }), 400


        if gender not in [1, 2]:

            return jsonify({

                "success": False,

                "error":
                    "Gender must be 1 or 2."

            }), 400


        if cholesterol not in [1, 2, 3]:

            return jsonify({

                "success": False,

                "error":
                    "Cholesterol must be 1, 2 or 3."

            }), 400


        if gluc not in [1, 2, 3]:

            return jsonify({

                "success": False,

                "error":
                    "Glucose must be 1, 2 or 3."

            }), 400


        if smoke not in [0, 1]:

            return jsonify({

                "success": False,

                "error":
                    "Smoke must be 0 or 1."

            }), 400


        if alco not in [0, 1]:

            return jsonify({

                "success": False,

                "error":
                    "Alcohol must be 0 or 1."

            }), 400


        if active not in [0, 1]:

            return jsonify({

                "success": False,

                "error":
                    "Active must be 0 or 1."

            }), 400


        if not (
            60 <= ap_hi <= 250
        ):

            return jsonify({

                "success": False,

                "error":
                    "Systolic BP must be between 60 and 250."

            }), 400


        if not (
            40 <= ap_lo <= 200
        ):

            return jsonify({

                "success": False,

                "error":
                    "Diastolic BP must be between 40 and 200."

            }), 400


        # ----------------------------------------------------
        # CREATE FEATURES
        # ----------------------------------------------------
        # IMPORTANT:
        # Same 11 features used during training.
        #
        # id is NOT included.

        features = np.array([

            [
                age,
                gender,
                height,
                weight,
                ap_hi,
                ap_lo,
                cholesterol,
                gluc,
                smoke,
                alco,
                active
            ]

        ])


        # ----------------------------------------------------
        # SCALE FEATURES
        # ----------------------------------------------------

        scaled_features = scaler.transform(
            features
        )


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        prediction_class = int(

            model.predict(
                scaled_features
            )[0]

        )


        # ----------------------------------------------------
        # PROBABILITY
        # ----------------------------------------------------

        probabilities = model.predict_proba(
            scaled_features
        )[0]


        risk_probability = float(
            probabilities[1]
        )


        confidence_score = float(
            max(probabilities)
        )


        # ----------------------------------------------------
        # BMI
        # ----------------------------------------------------

        bmi, bmi_category = calculate_bmi(

            height,
            weight

        )


        # ----------------------------------------------------
        # BLOOD PRESSURE
        # ----------------------------------------------------

        bp_category = get_bp_category(

            ap_hi,
            ap_lo

        )


        # ----------------------------------------------------
        # DATA FOR RECOMMENDATIONS
        # ----------------------------------------------------

        parsed_data = {

            "age":
                age,

            "gender":
                gender,

            "height":
                height,

            "weight":
                weight,

            "ap_hi":
                ap_hi,

            "ap_lo":
                ap_lo,

            "cholesterol":
                cholesterol,

            "gluc":
                gluc,

            "smoke":
                smoke,

            "alco":
                alco,

            "active":
                active

        }


        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        recommendations = generate_recommendations(

            parsed_data,

            risk_probability,

            bp_category,

            bmi_category

        )


        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        response_payload = {

            "success":
                True,

            "prediction":
                prediction_class,

            "risk_label":

                (
                    "High Risk of Cardiovascular Disease"

                    if prediction_class == 1

                    else

                    "Low Risk of Cardiovascular Disease"
                ),


            "risk_probability":

                round(
                    risk_probability * 100,
                    1
                ),


            "confidence_score":

                round(
                    confidence_score * 100,
                    1
                ),


            "health_metrics": {

                "bmi":
                    bmi,

                "bmi_category":
                    bmi_category,

                "bp_category":
                    bp_category,

                "systolic_bp":
                    ap_hi,

                "diastolic_bp":
                    ap_lo

            },


            "recommendations":
                recommendations

        }


        return jsonify(
            response_payload
        ), 200


    except ValueError as e:

        return jsonify({

            "success": False,

            "error":
                f"Invalid input value: {str(e)}"

        }), 400


    except Exception as e:

        print(
            "Prediction error:",
            str(e)
        )

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print(
        "=========================================="
    )

    print(
        " Cardiovascular Disease Prediction API"
    )

    print(
        "=========================================="
    )

    print(
        "Model loaded:",
        model is not None
    )

    print(
        "Scaler loaded:",
        scaler is not None
    )

    print(
        "Server running on:"
    )

    print(
        "http://localhost:5000"
    )

    print(
        "=========================================="
    )


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )