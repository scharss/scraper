from flask import render_template, request, jsonify, flash
from flask_login import login_required
from app.main import bp
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai
import asyncio
import json

# Configuración para forzar la salida en modo JSON en Gemini
json_output_config = genai.GenerationConfig(response_mime_type="application/json")

async def process_url_with_smart_prompt(url: str, task_description: str):
    """
    Rastrea una URL y usa un prompt inteligente para que Gemini extraiga los datos
    solicitados e infiera la estructura JSON más apropiada.
    """
    try:
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url)
        if not result or not result.markdown:
            return {"error": "No se pudo extraer contenido de la página."}
    except Exception as e:
        return {"error": f"Error durante el rastreo: {e}"}

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Eres un sistema de extracción de datos experto. Tu tarea es analizar el contenido de una página web
        y cumplir la petición del usuario generando un objeto JSON estructurado.

        TAREA DEL USUARIO:
        "{task_description}"

        INSTRUCCIONES CLAVE:
        1. Analiza la "TAREA DEL USUARIO" para entender qué datos necesita.
        2. Infiere una estructura JSON lógica y apropiada para presentar esos datos.
        3. Tu respuesta DEBE ser únicamente el objeto JSON válido. No incluyas texto introductorio,
           explicaciones, ni los delimitadores de código ```json.

        CONTENIDO DE LA PÁGINA PARA ANALIZAR:
        ---
        {result.markdown}
        ---
        """
        response = await model.generate_content_async(prompt, generation_config=json_output_config)
        gemini_response_text = response.text
        structured_data = json.loads(gemini_response_text)
        return {"data": structured_data}
    except json.JSONDecodeError:
        return {"error": "Gemini no devolvió un JSON válido.", "raw_response": gemini_response_text}
    except Exception as e:
        return {"error": f"Error al llamar a la API de Gemini: {e}"}


@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/scrape', methods=['POST'])
@login_required
def scrape():
    url = request.form.get('url')
    prompt = request.form.get('prompt')

    if not url or not prompt:
        flash('La URL y el prompt son obligatorios.', 'danger')
        return render_template('index.html')

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    result = loop.run_until_complete(process_url_with_smart_prompt(url, prompt))
    
    if "error" in result:
        return jsonify({"status": "error", "message": result["error"], "raw_response": result.get("raw_response")})
    
    return jsonify({"status": "success", "data": result["data"]}) 