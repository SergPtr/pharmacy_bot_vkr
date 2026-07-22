import db_queries
import tkinter_gui

def main():
    print("=== ЗАПУСК ДИПЛОМНОГО ПРОЕКТА ===")
    
    # 1. Автоматически проверяем и создаем таблицы БД при старте программы
    db_queries.init_db()
    
    # 2. Запускаем графическое окно пользователя (GUI)
    print("Инициализация графического интерфейса Tkinter...")
    tkinter_gui.root.mainloop()

if __name__ == "__main__":
    main()