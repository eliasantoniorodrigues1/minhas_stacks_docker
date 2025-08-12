from flask import Flask, request, jsonify
from bark import generate_audio, preload_models
import tempfile
import os

app = Flask(__name__)
preload_models()

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    audio_array = generate_audio(text)
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    audio_array.save(tmpfile.name)

    return jsonify({'message': 'Audio generated', 'file': tmpfile.name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
