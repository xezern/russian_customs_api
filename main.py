from flask import Flask, request, jsonify
from tks_api_official.calc import CustomsCalculator
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    try:
        # Calculator obyektini config faylı ilə yarat
        calculator = CustomsCalculator("config.yaml")

        # Parametrləri təyin et
        calculator.set_vehicle_details(
            age=data.get("age"),
            engine_capacity=int(data.get("engine_capacity")),
            engine_type=data.get("engine_type"),
            power=int(data.get("power")),
            price=float(data.get("price")),
            owner_type=data.get("owner_type"),
            currency=data.get("currency")
        )

        # ETC və CTP hesablamaları
        etc_result = calculator.calculate_etc()
        ctp_result = calculator.calculate_ctp()

        return jsonify({
            "ETC": etc_result,
            "CTP": ctp_result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
