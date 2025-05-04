from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data with actual beats from the static directory
beats = [
    {
        "id": 1,
        "name": "Beat 1",
        "mood": "Energetic",
        "bpm": 120,
        "audio_url": "/static/audio/Beat1.mp3",
        "is_playing": False
    },
    {
        "id": 2,
        "name": "Beat 2",
        "mood": "Energetic",
        "bpm": 125,
        "audio_url": "/static/audio/Beat2.mp3",
        "is_playing": False
    },
    {
        "id": 3,
        "name": "Beat 3",
        "mood": "Energetic",
        "bpm": 130,
        "audio_url": "/static/audio/Beat3.mp3",
        "is_playing": False
    },
    {
        "id": 4,
        "name": "Beat 4",
        "mood": "Energetic",
        "bpm": 128,
        "audio_url": "/static/audio/Beat4.mp3",
        "is_playing": False
    },
    {
        "id": 5,
        "name": "Beat 5",
        "mood": "Energetic",
        "bpm": 132,
        "audio_url": "/static/audio/Beat5.mp3",
        "is_playing": False
    },
    {
        "id": 6,
        "name": "Beat 6",
        "mood": "Energetic",
        "bpm": 135,
        "audio_url": "/static/audio/Beat6.mp3",
        "is_playing": False
    },
    {
        "id": 7,
        "name": "Beat 7",
        "mood": "Energetic",
        "bpm": 140,
        "audio_url": "/static/audio/Beat7.mp3",
        "is_playing": False
    },
    {
        "id": 8,
        "name": "Beat 8",
        "mood": "Energetic",
        "bpm": 138,
        "audio_url": "/static/audio/Beat8.mp3",
        "is_playing": False
    },
    {
        "id": 9,
        "name": "Beat 9",
        "mood": "Energetic",
        "bpm": 142,
        "audio_url": "/static/audio/Beat9.mp3",
        "is_playing": False
    },
    {
        "id": 10,
        "name": "Beat 10",
        "mood": "Energetic",
        "bpm": 145,
        "audio_url": "/static/audio/Beat10.mp3",
        "is_playing": False
    },
    {
        "id": 11,
        "name": "Lofi Beat",
        "mood": "Relax",
        "bpm": 90,
        "audio_url": "/static/audio/lofi.mp3",
        "is_playing": False
    },
    {
        "id": 12,
        "name": "Bollywood Beat",
        "mood": "Happy",
        "bpm": 110,
        "audio_url": "/static/audio/bollywood.mp3",
        "is_playing": False
    }
]

moods = ["Relax", "Energetic", "Sad", "Happy"]

@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Flask API Connected!"}), 200

@app.route("/api/beats", methods=["GET"])
def get_beats():
    return jsonify({"beats": beats}), 200

@app.route("/api/beats/<int:beat_id>/play", methods=["POST"])
def play_beat(beat_id):
    beat = next((b for b in beats if b["id"] == beat_id), None)
    if not beat:
        abort(404, description="Beat not found")
    
    # Reset all beats to not playing
    for b in beats:
        b["is_playing"] = False
    
    beat["is_playing"] = True
    return jsonify(beat), 200

@app.route("/api/beats/<int:beat_id>/stop", methods=["POST"])
def stop_beat(beat_id):
    beat = next((b for b in beats if b["id"] == beat_id), None)
    if not beat:
        abort(404, description="Beat not found")
    
    beat["is_playing"] = False
    return jsonify(beat), 200

@app.route("/api/beats", methods=["POST"])
def add_beat():
    if not request.json or not all(k in request.json for k in ("name", "mood", "bpm", "audio_url")):
        abort(400, description="Missing required fields")
    
    data = request.json
    if data["mood"] not in moods:
        abort(400, description="Invalid mood")
        
    new_id = max([beat["id"] for beat in beats]) + 1 if beats else 1
    new_beat = {
        "id": new_id,
        "name": data["name"],
        "mood": data["mood"],
        "bpm": data["bpm"],
        "audio_url": data["audio_url"],
        "is_playing": False
    }
    beats.append(new_beat)
    return jsonify(new_beat), 201

@app.route("/api/beats/<int:beat_id>", methods=["GET"])
def get_beat(beat_id):
    beat = next((b for b in beats if b["id"] == beat_id), None)
    if not beat:
        abort(404, description="Beat not found")
    return jsonify(beat), 200

@app.route("/api/beats/<int:beat_id>", methods=["DELETE"])
def delete_beat(beat_id):
    beat = next((b for b in beats if b["id"] == beat_id), None)
    if not beat:
        abort(404, description="Beat not found")
    beats.remove(beat)
    return "", 204

@app.route("/api/moods", methods=["GET"])
def get_moods():
    return jsonify({"moods": moods}), 200

@app.route("/api/beats/stop-all", methods=["POST"])
def stop_all_beats():
    for beat in beats:
        beat["is_playing"] = False
    return jsonify({"message": "All beats stopped"}), 200

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": error.description}), 404

if __name__ == "__main__":
    app.run(port=5001)
