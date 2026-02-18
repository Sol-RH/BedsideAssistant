# Read intents from JSON file 
# rn the intents correspond only to category: room_iot 
import json 
from pathlib import Path
import logging

INTENTS_FILE= Path(__file__).parent / "intents.json"
logger = logging.getLogger(__name__)
def load_intents():
    try:
        with open(INTENTS_FILE, 'r', encoding='utf-8') as intents_file:
            data= json.load(intents_file)
        return data["intents"]
    except FileNotFoundError:
        logger.error("Error: The file was not found.")
        return []
    except json.JSONDecodeError:
        logger.error("Error: failed to decode JSON from file")
        return []
        
        
    
if __name__== "__main__":
    logging.basicConfig(level=logging.INFO)
    intents= load_intents()
    logger.info(f"Cargados {len(intents)} intents")