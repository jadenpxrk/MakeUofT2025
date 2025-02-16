from flask import Flask, jsonify

app = Flask(__name__)

# Dummy game result data
game_result = {"Game": "7", "Winner": "473"}


@app.route("/game_result.json", methods=["GET"])
def get_game_result():
    return jsonify(game_result)


if __name__ == "__main__":
    # Run the server on localhost at port 9000
    app.run(host="0.0.0.0", port=9000)
