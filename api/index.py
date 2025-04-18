from flask import Flask, request, jsonify
from tks_api_official.calc import CustomsCalculator
from flask_cors import CORS 

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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


@app.route('/enums/<lang>', methods=['GET'])
def getEnums(lang):
    try:
        supported_langs = ["az", "en", "ru", "ko"]
        if lang not in supported_langs:
            return jsonify({"error": "Unsupported language"}), 400

        obj = {
            "age": [
                {
                    "az": {"option": "Yeni", "value": "new"},
                    "en": {"option": "New", "value": "new"},
                    "ru": {"option": "Новый", "value": "new"},
                    "ko": {"option": "신규", "value": "new"}
                },
                {
                    "az": {"option": "1 ildən 3 ilə", "value": "1-3"},
                    "en": {"option": "1 to 3 years", "value": "1-3"},
                    "ru": {"option": "От 1 до 3 лет", "value": "1-3"},
                    "ko": {"option": "1년에서 3년", "value": "1-3"}
                },
                {
                    "az": {"option": "5 ildən 7 ilə", "value": "5-7"},
                    "en": {"option": "5 to 7 years", "value": "5-7"},
                    "ru": {"option": "От 5 до 7 лет", "value": "5-7"},
                    "ko": {"option": "5년에서 7년", "value": "5-7"}
                },
                {
                    "az": {"option": "7 ildən çox", "value": "over_7"},
                    "en": {"option": "Over 7 years", "value": "over_7"},
                    "ru": {"option": "Более 7 лет", "value": "over_7"},
                    "ko": {"option": "7년 이상", "value": "over_7"}
                }
            ],
            "engine_type": [
                {
                    "az": {"option": "Benzin", "value": "gasoline"},
                    "en": {"option": "Gasoline", "value": "gasoline"},
                    "ru": {"option": "Бензин", "value": "gasoline"},
                    "ko": {"option": "가솔린", "value": "gasoline"}
                },
                {
                    "az": {"option": "Dizel", "value": "diesel"},
                    "en": {"option": "Diesel", "value": "diesel"},
                    "ru": {"option": "Дизель", "value": "diesel"},
                    "ko": {"option": "디젤", "value": "diesel"}
                },
                {
                    "az": {"option": "Elektrik", "value": "electric"},
                    "en": {"option": "Electric", "value": "electric"},
                    "ru": {"option": "Электро", "value": "electric"},
                    "ko": {"option": "전기", "value": "electric"}
                },
                {
                    "az": {"option": "Hibrid", "value": "hybrid"},
                    "en": {"option": "Hybrid", "value": "hybrid"},
                    "ru": {"option": "Гибрид", "value": "hybrid"},
                    "ko": {"option": "하이브리드", "value": "hybrid"}
                }
            ],
            "owner_type": [
                {
                    "az": {"option": "Fərdi şəxs", "value": "individual"},
                    "en": {"option": "Individual", "value": "individual"},
                    "ru": {"option": "Физическое лицо", "value": "individual"},
                    "ko": {"option": "개인", "value": "individual"}
                },
                {
                    "az": {"option": "Şirkət", "value": "company"},
                    "en": {"option": "Company", "value": "company"},
                    "ru": {"option": "Компания", "value": "company"},
                    "ko": {"option": "회사", "value": "company"}
                }
            ],
            "currency": [
                {
                    "az": {"option": "AZN", "value": "AZN"},
                    "en": {"option": "AZN", "value": "AZN"},
                    "ru": {"option": "AZN", "value": "AZN"},
                    "ko": {"option": "AZN", "value": "AZN"}
                },
                {
                    "az": {"option": "USD", "value": "USD"},
                    "en": {"option": "USD", "value": "USD"},
                    "ru": {"option": "USD", "value": "USD"},
                    "ko": {"option": "USD", "value": "USD"}
                },
                {
                    "az": {"option": "EUR", "value": "EUR"},
                    "en": {"option": "EUR", "value": "EUR"},
                    "ru": {"option": "EUR", "value": "EUR"},
                    "ko": {"option": "EUR", "value": "EUR"}
                },
                {
                    "az": {"option": "RUB", "value": "RUB"},
                    "en": {"option": "RUB", "value": "RUB"},
                    "ru": {"option": "RUB", "value": "RUB"},
                    "ko": {"option": "RUB", "value": "RUB"}
                }
            ]
        }

        # Dilə uyğun dəyərləri çıxar
        localized = {}
        for key, items in obj.items():
            localized[key] = [
                {"option": item[lang]["option"], "value": item[lang]["value"]}
                for item in items
            ]

        return jsonify(localized)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
   

# SSR üçün lazım:
def handler(environ, start_response):
    return app(environ, start_response)

if __name__ == '__main__':
    app.run(debug=True)
