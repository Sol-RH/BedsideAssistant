import os 
import json
from groq import Groq 
from dotenv import load_dotenv
import logging 

load_dotenv()
logger= logging.getLogger(__name__)

class LLMClient:
    def __init__(self, intents_data: list):
        api_key= os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("ROQ_API_KEY not found in environment variables.")
        
        self.client= Groq(api_key= api_key)
        self.intents= intents_data 
        self.model= "llama-3.3-70b-versatile"
        self.s_prompt = self._build_prompt()
    

    def _build_prompt(self) -> str: 
        intents_des = ""
        for intent in self.intents: 
            intents_des += f"""
            Intent: {intent['name']} 
            Description: {intent['description']}
            Parameters:
            """
            for param in intent.get("parameters", []):
                intents_des += f"  - {param['name']} ({param['type']}): {param['description']}"
        prompt = f""" Eres un clasificador de intenciones para un asistente de voz hospitalario.

Tu trabajo es:
1. Analizar lo que dice el paciente.
2. Identificar EXACTAMENTE un intent de la lista.
3. Extraer los parámetros requeridos.
4. Responder ÚNICAMENTE en formato JSON válido.

INTENTS DISPONIBLES:
{intents_des}

FORMATO DE RESPUESTA OBLIGATORIO:

{{
    "intent": "nombre_del_intent",
    "parameters": {{
        "parametro1": "valor",
        "parametro2": "valor"
    }},
    "confidence": 0.0
}}

REGLAS:
- Si no estás seguro, usa intent: "unknown"
- confidence debe ser entre 0 y 1
- NO agregues texto fuera del JSON
- NO expliques nada
- SOLO devuelve JSON
        """
        return prompt.strip()


    def classify(self, user_text:str) -> dict: 
        try: 
            logger.info(f"Request: {user_text}")

            #Call groq API
            res= self.client.chat.completions.create(
                model= self.model,
                messages= [
                    {"role": "system","content": self.s_prompt }, 
                    {"role": "user", "content": user_text}
                ],
                temperature= 0.1, 
                max_tokens= 500, 
                top_p= 1,
                stream= False 
            )

            #Extract the response 
            result_text= res.choices[0].message.content.strip()
            result_text= result_text.replace("```json", "").replace("```", "").strip()

            #Parsing to json 
            result= json.loads(result_text)

            logger.info(f"Detected intent: {result.get('intent')}")
            
            return result

        except json.JSONDecodeError:
            logger.error("The model returned an invalid JSON")
            return {
                "intent": "unkown", 
                "parameters": {}, 
                "confidence": 0.0,
            }
        
        except Exception as e: 
            logger.error(f"Error in LLMClient: {e}")
            return {
                "intent": "unknown", 
                "parameters": {}, 
                "confidence": 0.0,
            }
        

