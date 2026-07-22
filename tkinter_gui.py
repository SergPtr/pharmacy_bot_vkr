import tkinter as tk
from tkinter import scrolledtext
import nlp_analyzer
import response_builder

import voice_recognizer  # Подключаем голосовой модуль

def process_message(forced_text=None):
    """Основная функция обработки сообщений (поддерживает и текст, и голос)"""
    # Если текст передан из функции микрофона, берем его, иначе читаем поле ввода
    user_text = forced_text if forced_text else entry_field.get().strip()
    if not user_text:
        return
        
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"Вы: {user_text}\n\n")
    if not forced_text:
        entry_field.delete(0, tk.END)
    
    # Передаем текст в GigaChat API
    ai_result = nlp_analyzer.analyze_user_message(user_text)
    final_reply = response_builder.build_reply(ai_result)
    
    chat_area.insert(tk.END, f"Бот-Фармацевт: {final_reply}\n")
    chat_area.insert(tk.END, "="*50 + "\n\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)

def start_voice_input():
    """Функция, которая вызывается при нажатии на кнопку с микрофоном"""
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "📢 Система: Микрофон активирован. Говорите запрос в течение 4 секунд...\n\n")
    chat_area.config(state=tk.DISABLED)
    root.update() # Принудительно перерисовываем окно, чтобы надпись появилась сразу
    
    # Вызываем наш независимый голосовой модуль
    spoken_text = voice_recognizer.record_and_recognize(duration=4)
    
    if spoken_text:
        # Если речь успешно распознана, отправляем этот текст в наш стандартный обработчик!
        process_message(forced_text=spoken_text)
    else:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, "❌ Система: Не удалось распознать речь. Попробуйте еще раз или введите текст вручную.\n")
        chat_area.insert(tk.END, "="*50 + "\n\n")
        chat_area.config(state=tk.DISABLED)

# === НАСТРОЙКА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА TKINTER ===
root = tk.Tk()
root.title("Интеллектуальная справочная система аптеки (Прототип ВКР)")
root.geometry("650x550")
root.configure(bg="#f0f2f5")

header = tk.Label(root, text="💬 Аптечный ИИ-Помощник", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", pady=10)
header.pack(fill=tk.X)

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 10), state=tk.DISABLED, bg="white")
chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root, bg="#f0f2f5")
input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=10)

entry_field = tk.Entry(input_frame, font=("Arial", 11))
entry_field.pack(fill=tk.X, side=tk.LEFT, expand=True, ipady=5)
entry_field.bind("<Return>", lambda event: process_message())

# КНОПКА 1: Микрофон (Вызывает наш новый голосовой ввод)
voice_button = tk.Button(input_frame, text="🎙️ Голос", font=("Arial", 10, "bold"), bg="#2196F3", fg="white", command=start_voice_input)
voice_button.pack(side=tk.RIGHT, padx=2)

# КНОПКА 2: Стандартная отправка текста
send_button = tk.Button(input_frame, text="Отправить", font=("Arial", 10, "bold"), bg="#4CAF50", fg="white", command=lambda: process_message())
send_button.pack(side=tk.RIGHT, padx=2)

chat_area.config(state=tk.NORMAL)
chat_area.insert(tk.END, "Бот-Фармацевт: Приветствую! Нажмите кнопку '🎙️ Голос' или введите текстовый запрос (например: 'аналог нурафена').\n")
chat_area.insert(tk.END, "="*50 + "\n\n")
chat_area.config(state=tk.DISABLED)

if __name__ == "__main__":
    root.mainloop()