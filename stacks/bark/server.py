import io
import json
from flask import Flask, request, jsonify, send_file
import scipy.io.wavfile
from bark.api import generate_audio
from bark.generation import preload_models

# Inicializa o Flask
app = Flask(__name__)

# Rota para a API de geração de áudio
@app.route('/generate', methods=['POST'])
def generate_bark_audio():
    # Verifica se a requisição é JSON
    if not request.is_json:
        return jsonify({"error": "A requisição deve ser JSON"}), 400

    # Pega o texto do corpo da requisição
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "O campo 'text' é obrigatório"}), 400

    print(f"Gerando áudio para o texto: '{text}'")

    try:
        # Gera o áudio usando a função do Bark
        audio_array = generate_audio(text)

        # Salva o áudio em um buffer de memória
        buffer = io.BytesIO()
        scipy.io.wavfile.write(buffer, 24000, audio_array)
        buffer.seek(0) # Volta ao início do buffer para a leitura

        # Retorna o arquivo de áudio como resposta HTTP
        return send_file(
            buffer,
            mimetype='audio/wav',
            as_attachment=True,
            download_name='output.wav'
        )

    except Exception as e:
        # Trata possíveis erros
        print(f"Erro ao gerar áudio: {e}")
        return jsonify({"error": str(e)}), 500

# Executa o servidor Flask quando o script é chamado diretamente
if __name__ == '__main__':
    # Pré-carrega os modelos do Bark antes de iniciar o servidor
    print("Pré-carregando modelos do Bark...")
    preload_models()
    # Inicia o servidor, permitindo conexões de qualquer IP
    app.run(host='0.0.0.0', port=5000)