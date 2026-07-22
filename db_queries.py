import sqlite3

DATABASE_NAME = "pharmacy_bot.db"

def init_db():
    """Создает базу данных и таблицы, если они еще не созданы"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # 1. Таблица препаратов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            substance TEXT NOT NULL,
            form TEXT NOT NULL
        )
    ''')
    
    # 2. Таблица инструкций
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instructions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_id INTEGER NOT NULL,
            indications TEXT,
            contraindications TEXT,
            side_effects TEXT,
            dosage TEXT,
            FOREIGN KEY (drug_id) REFERENCES drugs (id)
        )
    ''')
    
    # 3. Таблица аналогов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug_id INTEGER NOT NULL,
            analog_id INTEGER NOT NULL,
            relation_type TEXT,
            FOREIGN KEY (drug_id) REFERENCES drugs (id),
            FOREIGN KEY (analog_id) REFERENCES drugs (id)
        )
    ''')
    
    # 4. Таблица совместимости
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compatibility (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug1_id INTEGER NOT NULL,
            drug2_id INTEGER NOT NULL,
            effect TEXT,
            description TEXT,
            FOREIGN KEY (drug1_id) REFERENCES drugs (id),
            FOREIGN KEY (drug2_id) REFERENCES drugs (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("База данных и таблицы успешно инициализированы!")


# =====================================================================
# ФУНКЦИИ ПОИСКА (ЗАПРОСЫ / QUERIES) В БАЗУ ДАННЫХ
# =====================================================================

def get_drug_instruction(drug_name):
    """1. Запрос инструкции, показаний, противопоказаний и дозировки"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d.name, i.indications, i.contraindications, i.side_effects, i.dosage
        FROM drugs d
        JOIN instructions i ON d.id = i.drug_id
        WHERE LOWER(d.name) = LOWER(?)
    ''', (drug_name,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_drug_analogs(drug_name):
    print("get_drug_analogs")
    """2. Запрос на поиск аналогов лекарства"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT d2.name, a.relation_type
        FROM drugs d1
        JOIN analogs a ON d1.id = a.drug_id
        JOIN drugs d2 ON a.analog_id = d2.id
        WHERE LOWER(d1.name) = LOWER(?)
    ''', (drug_name,))
    results = cursor.fetchall()
    conn.close()
    return results

def check_compatibility(drug1_name, drug2_name):
    """3. Запрос на проверку совместимости двух препаратов"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.effect, c.description
        FROM compatibility c
        JOIN drugs d1 ON c.drug1_id = d1.id
        JOIN drugs d2 ON c.drug2_id = d2.id
        WHERE (LOWER(d1.name) = LOWER(?) AND LOWER(d2.name) = LOWER(?))
           OR (LOWER(d1.name) = LOWER(?) AND LOWER(d2.name) = LOWER(?))
    ''', (drug1_name, drug2_name, drug2_name, drug1_name))
    result = cursor.fetchone()
    conn.close()
    return result


def find_drugs_by_indication(search_text):
    """4. Запрос на поиск лекарств по симптомам или показаниям"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Склеиваем знак процента, поисковое слово и знак процента обычными плюсами
    search_pattern = "%" + search_text + "%"
    
    # Ищем лекарства, у которых в поле "indications" (показания) встречается нужное слово
    # Оператор LIKE и знаки % позволяют искать частичное совпадение (например, "боль" внутри фразы)
    cursor.execute('''
        SELECT d.name, i.indications
        FROM drugs d
        JOIN instructions i ON d.id = i.drug_id
        WHERE LOWER(i.indications) LIKE LOWER(?)
    ''', (search_pattern,)) # Передаем готовую строку в круглых скобках с запятой - передаем список а не просто текст
    
    results = cursor.fetchall()
    conn.close()
    return results  # Возвращает список всех подходящих лекарств




# =====================================================================

if __name__ == "__main__":
    init_db()