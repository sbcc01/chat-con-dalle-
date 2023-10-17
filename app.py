from flask import Flask, render_template, request
import openai

app = Flask(__name__)

OPENAI_API_KEY = "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"

class OpenAIAPI:
    def __init__(self, api_key):
        openai.api_key = api_key

    def crear_imagen(self, descripcion, cantidad):
        respuesta = openai.Image.create(
            prompt=descripcion,
            n=cantidad,
            size="512x512"
        )
        return respuesta["data"]

    def enviar_pregunta(self, descripcion):
        if len(descripcion.split()) > 1:
            respuesta = openai.Image.create(
                prompt=descripcion,
                n=1,
                size="512x512"
            )
            if respuesta["data"]:
                return respuesta["data"][0]["caption"]
            else:
                return "No se encontraron imágenes para la descripción proporcionada."
        else:
            respuesta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": descripcion}
                ],
            )
            respuesta_texto = respuesta["choices"][0]["message"]["content"]
            return respuesta_texto

openai_api = OpenAIAPI(OPENAI_API_KEY)

@app.route('/')
def index():
    return render_template('index.html', urls=None, pregunta_respuesta=None)

@app.route('/generar_imagen', methods=['POST'])
def generar_imagen():
    descripcion = request.form['descripcion']
    cantidad = int(request.form['cantidad'])
    res = openai_api.crear_imagen(descripcion, cantidad)
    urls = [url['url'] for url in res]
    pregunta_respuesta = openai_api.enviar_pregunta(descripcion)
    return render_template('index.html', urls=urls, pregunta_respuesta=pregunta_respuesta, descripcion=descripcion)

if __name__ == "__main__":
    app.run(debug=True)
