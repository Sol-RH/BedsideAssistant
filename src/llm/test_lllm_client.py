import logging
from src.nlp.intent_scheme import load_intents
from src.llm.llm_client import LLMClient


logging.basicConfig(level=logging.INFO)

def main():
    # 1️⃣ Cargar intents desde JSON
    intents = load_intents()

    if not intents:
        print("No intents loaded")
        return

    print(f"Loaded {len(intents)} intents")

    # 2️⃣ Inicializar LLM Client
    llm = LLMClient(intents)

    # 3️⃣ Texto de prueba
    user_input = "Subele"

    # 4️⃣ Clasificar
    result = llm.classify(user_input)

    print("\nRESULT:")
    print(result)


if __name__ == "__main__":
    main()
