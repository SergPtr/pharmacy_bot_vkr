import os
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Справочник русской языковой модели
MODEL_PATH = "vosk-model-small-ru-0.22"

# Частота дискретизации для записи человеческого голоса (стандарт для Vosk)
SAMPLE_RATE = 16000 

def record_and_recognize(duration=4):
    """
    Записывает аудио с микрофона в течение указанных секунд (по умолчанию 4 сек)
    и переводит русскую речь в текстовую строку.
    """
    if not os.path.exists(MODEL_PATH):
        print("Ошибка ВКР: Папка голосовой модели не найдена! Проверьте путь:", MODEL_PATH)
        return ""

    print(f"\n🎤 Микрофон включен! Говорите запрос (у вас есть {duration} сек)...")
    
    try:
        # Записываем звук с микрофона в массив памяти Python ("по-деревянному" без файлов)
        audio_data = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
        sd.wait() # Ждем завершения времени записи
        print("🛑 Запись завершена. Начинается распознавание речи...")

        # Инициализируем модель Vosk
        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, SAMPLE_RATE)
        
        # Переводим байты аудио в понятный для Vosk формат
        audio_bytes = audio_data.tobytes()
        recognizer.AcceptWaveform(audio_bytes)
        
        # Получаем финальный текстовый результат в формате JSON
        result_json = recognizer.FinalResult()
        result_dict = json.loads(result_json)
        
        # Вытаскиваем чистый текст
        recognized_text = result_dict.get("text", "").strip()
        print(f"➔ Результат распознавания: '{recognized_text}'")
        return recognized_text

    except Exception as e:
        print(f"Системный сбой модуля голосового ввода: {e}")
        return ""

# Локальный тест модуля
if __name__ == "__main__":
    print("--- Тестируем изолированный модуль распознавания речи voice_recognizer.py ---")
    text = record_and_recognize(duration=4)
    if text:
        print(f"Успех! Распознано слово: {text}")
    else:
        print("Речь не распознана или микрофон отключен.")