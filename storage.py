def load_qa_from_file():
    filename = 'questions.txt'  # путь к файлу с вопросами и ответами
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()

    # Формируем словарь question → answer
    qa_dict = {}
    for line in lines:
        parts = line.strip().split('|')
        
        if len(parts) != 2:
            continue  # пропускаем некорректные строки

        question, answer = parts
        qa_dict[question] = answer

    return qa_dict

if __name__ == "__main__":
    print("Загрузка вопросов и ответов...")