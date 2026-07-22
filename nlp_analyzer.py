import os
import json
from dotenv import load_dotenv
from gigachat import GigaChat

# 1. Загружаем секретные переменные окружения из .env файла
load_dotenv()
GIGACHAT_API = os.getenv("GIGACHAT_API")

def analyze_user_message(user_message):
    """
    Модуль анализа естественного языка (NLP).
    Отправляет запрос в GigaChat и выводит результат анализа в консоль.
    """
    system_prompt = (
        "Ты — модуль классификации запросов для аптечного справочного бота. "
        "Твоя задача — проанализировать фразу пользователя и строго вернуть ответ в формате JSON. "
        "Доступные намерения (intent):\n"
        "1. 'description' — если пользователь просит инструкцию, описание лекарства, показания, противопоказания или дозировку.\n"
        "2. 'analogs' — если пользователь просит найти замену, аналоги или дженерики.\n"
        "3. 'compatibility' — если пользователь спрашивает, можно ли принимать два лекарства одновременно.\n"
        "4. 'indication' — если пользователь ищет лекарство по симптому (например: от головы, от жара, от кашля).\n\n"
        "Формат твоего ответа должен быть СТРОГО следующим JSON-шаблоном, без лишних слов, без разметки markdown (```json) и пояснений:\n"
        '{"intent": "название_намерения", "drug_name": "название_лекарства_или_симптома"}\n'
        "Если в запросе два лекарства (для совместимости), укажи их через запятую в поле drug_name."
    )

    with GigaChat(credentials=GIGACHAT_API, verify_ssl_certs=False) as giga:
        try:
            # Склеиваем обычным плюсом
            full_prompt = system_prompt + "\n\nПользователь пишет: " + user_message
            response = giga.chat(full_prompt)
            
            raw_text = response.choices[0].message.content.strip()
            
            # Превращаем в словарь Python
            structured_data = json.loads(raw_text)
            
            if "drug_name" in structured_data and structured_data["drug_name"]:
                structured_data["drug_name"] = structured_data["drug_name"].strip()
            
            # Наш простой и надежный принт без наворотов
            print("\n[ИИ-АНАЛИЗ] Фраза:", user_message, "➔ Результат GigaChat:", structured_data)
                
            return structured_data
            
        except json.JSONDecodeError:
            print("Ошибка: ИИ вернул некорректный формат JSON. Ответ был:", raw_text)
            return {"intent": "unknown", "drug_name": ""}
        except Exception as e:
            print("Произошла ошибка при обращении к GigaChat API:", e)
            return {"intent": "error", "drug_name": ""}

# Блок тестирования работоспособности модуля ИИ
if __name__ == "__main__":
    print("--- Тестируем модуль ИИ nlp_analyzer.py ---")
    
    # Тест 1: Запрос аналога
    test_phrase = "Подскажи, чем можно заменить Нурофен?"
    print(f"\nПользователь пишет: '{test_phrase}'")
    result = analyze_user_message(test_phrase)
    print(f"Результат анализа ИИ: {result}")