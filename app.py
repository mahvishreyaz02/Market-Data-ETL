from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Market Data ETL API is running"})


@app.route("/run_etl", methods=["POST"])
def run_etl():
    try:
        data = request.get_json()
        vendor = data.get("vendor")
        interface = data.get("interface")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        symbols = data.get("symbols")  

        if not all([vendor, interface, start_date, end_date]):
            return jsonify({"error": "Missing required parameters: vendor, interface, start_date, end_date"}), 400

        #Build command with argparse-friendly flags 
        cmd = [
            "python",
            "main.py",
            vendor,
            interface,
            "--start_date", start_date,
            "--end_date", end_date,
        ]


        if symbols and isinstance(symbols, list):
            cmd.append("--symbols")
            cmd.extend(symbols)

        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        if result.returncode == 0:
            return jsonify({
                "message": "ETL process completed successfully.",
                "details": result.stdout
            })
        else:
            return jsonify({
                "error": "ETL process failed.",
                "details": result.stderr or result.stdout 
            }), 500

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
