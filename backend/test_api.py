import urllib.request
import json


BASE_URL = "http://127.0.0.1:5000"


# ============================================================
# GET HOME
# ============================================================

def test_home():

    print("\nTesting GET / ...")


    request = urllib.request.Request(

        f"{BASE_URL}/"

    )


    with urllib.request.urlopen(
        request
    ) as response:

        data = json.loads(

            response.read().decode(
                "utf-8"
            )

        )


        print(
            json.dumps(
                data,
                indent=2
            )
        )


# ============================================================
# HEALTH
# ============================================================

def test_health():

    print(
        "\nTesting GET /api/health ..."
    )


    request = urllib.request.Request(

        f"{BASE_URL}/api/health"

    )


    with urllib.request.urlopen(
        request
    ) as response:

        data = json.loads(

            response.read().decode(
                "utf-8"
            )

        )


        print(
            json.dumps(
                data,
                indent=2
            )
        )


        if not data.get("model_loaded"):

            raise Exception(
                "Model is not loaded!"
            )


        if not data.get("scaler_loaded"):

            raise Exception(
                "Scaler is not loaded!"
            )


# ============================================================
# PREDICTION
# ============================================================

def test_prediction():

    print(
        "\nTesting POST /api/predict ..."
    )


    payload = {

        "age": 45,

        "gender": 1,

        "height": 170,

        "weight": 70,

        "ap_hi": 120,

        "ap_lo": 80,

        "cholesterol": 1,

        "gluc": 1,

        "smoke": 0,

        "alco": 0,

        "active": 1

    }


    request = urllib.request.Request(

        f"{BASE_URL}/api/predict",

        data=json.dumps(
            payload
        ).encode("utf-8"),

        headers={

            "Content-Type":
                "application/json"

        },

        method="POST"

    )


    with urllib.request.urlopen(
        request
    ) as response:

        data = json.loads(

            response.read().decode(
                "utf-8"
            )

        )


        print(
            json.dumps(
                data,
                indent=2
            )
        )


        if not data.get("success"):

            raise Exception(
                "Prediction failed!"
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        test_home()

        test_health()

        test_prediction()


        print(
            "\n=========================================="
        )

        print(
            "All Backend API Tests Passed Successfully!"
        )

        print(
            "=========================================="
        )


    except Exception as e:

        print(
            "\n[!] API Test Failed:"
        )

        print(
            str(e)
        )