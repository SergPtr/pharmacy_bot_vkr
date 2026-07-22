import sqlite3
from db_queries import DATABASE_NAME

def seed_data():
    """Наполняет базу данных тестовыми медицинскими препаратами"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    print("Начинаем наполнение базы данных...")

    # 1. Добавляем препараты в таблицу drugs
    # Используем INSERT OR IGNORE, чтобы не дублировать записи при повторном запуске
    drugs_data = [
        (1, 'парацетамол', 'парацетамол', 'таблетки'),
        (2, 'аспирин', 'ацетилсалициловая кислота', 'таблетки шипучие'),
        (3, 'нурофен', 'ибупрофен', 'капсулы')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO drugs (id, name, substance, form) 
        VALUES (?, ?, ?, ?)
    ''', drugs_data)

    # 2. Добавляем медицинские инструкции в таблицу instructions
    instructions_data = [
        (1, 'головная боль, жар, зубная боль', 'тяжелые нарушения функции печени или почек', 'аллергические реакции, тошнота', 'взрослым по 1-2 таблетки до 4 раз в сутки'),
        (2, 'лихорадка, болевой синдром слабой интенсивности', 'язва желудка, кровотечения, астма', 'боль в животе, изжога', 'растворить 1 таблетку в стакане воды, принимать после еды'),
        (3, 'головная, мигренозная и менструальная боль, жар', 'язвенная болезнь в фазе обострения, III триместр беременности', 'головная боль, нарушения работы жкт', 'по 1 капсуле (200 мг) 3-4 раза в сутки')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO instructions (drug_id, indications, contraindications, side_effects, dosage) 
        VALUES (?, ?, ?, ?, ?)
    ''', instructions_data)

    # 3. Устанавливаем связи аналогов в таблицу analogs (Нурофен и Парацетамол как схожие по действию)
    analogs_data = [
        (1, 3, 'схожее анальгезирующее действие'),
        (3, 1, 'схожее анальгезирующее действие')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO analogs (drug_id, analog_id, relation_type) 
        VALUES (?, ?, ?)
    ''', analogs_data)

    # 4. Добавляем информацию о совместимости в таблицу compatibility (Аспирин + Нурофен)
    compatibility_data = [
        (2, 3, 'опасно', 'одновременный прием повышает риск развития язвы желудка и кровотечений.')
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO compatibility (drug1_id, drug2_id, effect, description) 
        VALUES (?, ?, ?, ?)
    ''', compatibility_data)

    conn.commit()
    conn.close()
    print("База данных успешно наполнена тестовыми данными!")

if __name__ == "__main__":
    seed_data()