import db_queries

# Обязательное медицинское предупреждение по стандартам защиты данных
DISCLAIMER = "\n\n⚠️ Внимание! Информация носит справочный характер. Перед применением лекарственных средств обязательно проконсультируйтесь с врачом."

def build_reply(ai_result):
    """
    Главный диспетчер логики.
    Принимает словарь от ИИ (intent и drug_name) и формирует итоговый текст ответа.
    """
    # Если ИИ столкнулся с системной ошибкой сети
    if ai_result["intent"] == "error":
        return "Извините, произошла ошибка при подключении к модулю ИИ. Попробуйте повторить запрос позже."
        
    intent = ai_result.get("intent")
    drug_name = ai_result.get("drug_name", "").strip()
    #drug_name = ai_result.get("drug_name", "").strip().capitalize() #делаем первую букву заглавной

    # Если ИИ не смог понять намерение пользователя
    if intent == "unknown" or not drug_name:
        return "Извините, мне не удалось распознать название препарата или суть вашего вопроса. Переформулируйте запрос, пожалуйста."

    # Сценарий 1: Запрос инструкции / описания
    if intent == "description":
        db_data = db_queries.get_drug_instruction(drug_name)
        if db_data:
            # Разворачиваем кортеж из базы данных (название, показания, противопоказания, побочки, дозировка)
            name, indications, contraindications, side_effects, dosage = db_data
            reply = (
                f"📋 Справочная информация по препарату *{name}*:\n\n"
                f"🔹 *Показания:* {indications}\n"
                f"🔹 *Противопоказания:* {contraindications}\n"
                f"🔹 *Побочные эффекты:* {side_effects}\n"
                f"🔹 *Дозировка:* {dosage}"
            )
            return reply + DISCLAIMER
        else:
            return f"К сожалению, препарата '{drug_name}' пока нет в нашей аптечной базе данных."

    # Сценарий 2: Запрос аналогов
    elif intent == "analogs":
        db_data = db_queries.get_drug_analogs(drug_name)
        if db_data:
            reply = f"🔍 Аналоги для препарата *{drug_name}*, найденные в базе данных:\n"
            for item in db_data:
                analog_name, relation_type = item
                reply += f"• *{analog_name}* ({relation_type})\n"
            return reply + DISCLAIMER
        else:
            return f"К сожалению, в базе данных не найдены аналоги для препарата '{drug_name}'."

    # Сценарий 3: Проверка совместимости
    elif intent == "compatibility":
        # Если ИИ передал два лекарства через запятую, пробуем их разделить
        drugs = [d.strip() for d in drug_name.split(",")]
        
        if len(drugs) >= 2:
            drug1, drug2 = drugs[0], drugs[1]
            db_data = db_queries.check_compatibility(drug1, drug2)
            if db_data:
                effect, description = db_data
                return f"⚠️ *Результат проверки совместимости ({drug1} + {drug2}):*\n\nСтатус: *{effect}*\nОписание: {description}" + DISCLAIMER
            else:
                return f"✅ Ограничений на совместный прием препаратов *{drug1}* и *{drug2}* в нашей базе данных не обнаружено." + DISCLAIMER
        else:
            return "Для проверки совместимости укажите, пожалуйста, сразу два названия препаратов через запятую."

    # Сценарий 4: Поиск лекарства по симптому
    elif intent == "indication":
        db_data = db_queries.find_drugs_by_indication(drug_name)
        if db_data:
            reply = f"💡 По вашему запросу '{drug_name}' найдены следующие препараты:\n\n"
            for item in db_data:
                name, indications = item
                reply += f"• *{name}* (Показания: {indications})\n"
            return reply + DISCLAIMER
        else:
            return f"К сожалению, в базе данных не найдены лекарства, помогающие от: '{drug_name}'."

    return "Запрос принят, но обработка данного типа сценариев еще находится в разработке."

# Блок локального тестирования модуля сборки ответов
if __name__ == "__main__":
    print("--- Тестируем модуль сборки ответов response_builder.py ---")
    
    # Имитируем успешный ответ от nlp_analyzer.py (как будто ИИ распознал аналог Нурофена)
    mock_ai_result = {"intent": "analogs", "drug_name": "Нурофен"}
    
    print(f"\nВходные данные от ИИ: {mock_ai_result}")
    final_reply = build_reply(mock_ai_result)
    print("\nИтоговый ответ, который увидит пользователь:")
    print(final_reply)