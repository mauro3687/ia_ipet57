import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request
import json
from transcriber import Transcriber
from llm import LLM
from weather import Weather
from tts import TTS
from pc_command import PcCommand

# Cargar llaves del archivo .env
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("recorder.html")


@app.route("/audio", methods=["POST"])
def audio():

    audio = request.files.get("audio")
    text = Transcriber().transcribe(audio)

    llm = LLM()
    function_name, args, message = llm.process_functions(text)
    if function_name is not None:

        if function_name == "get_weather":

            function_response = Weather().get(args["ubicacion"])
            function_response = json.dumps(function_response)
            print(f"Respuesta de la funcion: {function_response}")

            final_response = llm.process_response(
                text, message, function_name, function_response)
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "send_email":

            final_response = "Tu que estas leyendo el codigo, implementame y envia correos muahaha"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "open_chrome":
            PcCommand().open_chrome(args["website"])
            final_response = "Listo, ya abrí chrome en el sitio " + \
                args["website"]
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "dominate_human_race":
            final_response = "No te creas. jajaja , no pudo hacer eso o tal vez si "
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "quien_messi":
            final_response = "Lionel Andrés Messi Cuccittini (Rosario, 24 de junio de 1987), conocido como Leo Messi, es un futbolista argentino que juega como delantero o centrocampista. Desde 2023, integra el plantel del Inter Miami de la MLS estadounidense. Es también internacional con la selección de Argentina, de la que es capitán. "
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "quien_presidente":
            final_response = "No te puedo dar un dato asi , pero segun mis predicciones y por datos estadisticos pueda llegar a ganar javier milei con 43 porciente y puede perder en buenos aires y en chaco "
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "que_ipet57":
            final_response = " Martin comodoro rivadavia ipet 57 es una escuela tecnico donde cuenta con la especialidad de Programacion, electronica y automotor, ubicada en Cordoba capital en barrio general paz en la calle 25 de mayo numeracion 1500"
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

        elif function_name == "presentar":
            final_response = "Hola ! soy IA del ipet 57, me creo Ezequiel, soy una  inteligencia donde aprendo con las preguntas que voy haciendo gracias a mi red reuronal, no me presione conozco muy poco de su mundo "
            tts_file = TTS().process(final_response)
            return {"result": "ok", "text": final_response, "file": tts_file}

    else:
        final_response = "Perdon, no pude entender tu pregunta , por favor me puedes repetir. puede ser que haya mucho ruido ?"
        tts_file = TTS().process(final_response)
        return {"result": "ok", "text": final_response, "file": tts_file}
