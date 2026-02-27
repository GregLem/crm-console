import csv
import datetime

CSV_FILE = "leads.csv"
FIELDNAMES = ["created_at", "name", "phone", "service"]


def input_non_empty(prompt):
    """Ввод строки, которая не может быть пустой"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Пусто. Введи значение.")


def normalize_phone(phone):
    """Оставляет только цифры (для стабильного поиска)"""
    return "".join(ch for ch in phone if ch.isdigit())


def input_phone(prompt):
    """Ввод телефона с минимальной проверкой"""
    while True:
        phone = input_non_empty(prompt)
        if normalize_phone(phone):
            return phone
        print("Телефон некорректный. Введи номер (должны быть цифры).")


def input_int(prompt):
    """Ввод целого числа (пока не введут корректно)"""
    while True:
        s = input_non_empty(prompt)
        try:
            return int(s)
        except ValueError:
            print("Нужно ввести число.")


def save_leads_to_csv(leads, filename=CSV_FILE):
    """Сохраняет список заявок в CSV (перезаписывает файл)"""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()          # записываем заголовки
        writer.writerows(leads)       # записываем все строки


def load_leads_from_csv(filename=CSV_FILE):
    """Загружает заявки из CSV. Если файла нет, возвращает пустой список."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            leads = []
            for row in reader:
                # Гарантируем, что у каждой заявки есть все поля (даже пустые)
                # и убираем лишние пробелы
                lead = {key: (row.get(key, "") or "").strip() for key in FIELDNAMES}
                leads.append(lead)
        print(f"Загружено заявок: {len(leads)}")
        return leads
    except FileNotFoundError:
        print("Файл leads.csv не найден. Начинаем с пустого списка.")
        return []
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return []


def add_lead(leads):
    """Добавляет новую заявку и сразу сохраняет весь список в CSV"""
    name = input_non_empty("Имя клиента: ")
    phone = input_phone("Телефон: ")
    service = input_non_empty("Услуга: ")

    lead = {
        "name": name,
        "phone": phone,
        "service": service,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    leads.append(lead)
    save_leads_to_csv(leads)
    print("Заявка добавлена и сохранена.")


def show_leads(leads):
    """Показывает все заявки в консоли с красивым форматированием"""
    if not leads:
        print("Заявок пока нет.")
        return

    # Ширина колонок (подобрана для средних значений)
    w_date = 16
    w_name = 18
    w_phone = 14
    w_service = 18

    def cut(s, w):
        """Обрезает строку до ширины w, добавляя '...' если нужно"""
        s = s or ""
        return (s[: w - 1] + "...") if len(s) > w else s

    # Формируем заголовок
    header = (
        "№".ljust(4)
        + "Дата".ljust(w_date + 2)
        + "Клиент".ljust(w_name + 2)
        + "Телефон".ljust(w_phone + 2)
        + "Услуга".ljust(w_service + 2)
    )
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Выводим строки
    for i, lead in enumerate(leads, start=1):
        line = (
            str(i).ljust(4)
            + cut(lead["created_at"], w_date).ljust(w_date + 2)
            + cut(lead["name"], w_name).ljust(w_name + 2)
            + cut(lead["phone"], w_phone).ljust(w_phone + 2)
            + cut(lead["service"], w_service).ljust(w_service + 2)
        )
        print(line)
    print("-" * len(header))


def find_leads_by_phone(leads, phone_query):
    """Ищет заявки по телефону (по цифрам, частичное совпадение)"""
    q = normalize_phone(phone_query)
    if not q:
        return []

    result = []
    for lead in leads:
        lead_phone = normalize_phone(lead.get("phone", ""))
        if q in lead_phone:
            result.append(lead)
    return result


def show_found_leads(found):
    """Показывает найденные заявки (коротко)"""
    if not found:
        print("Ничего не найдено.")
        return

    print(f"Найдено: {len(found)}")
    print("-" * 60)
    for i, lead in enumerate(found, start=1):
        print(f"{i}. {lead['created_at']} | {lead['name']} | {lead['phone']} | {lead['service']}")
    print("-" * 60)


def delete_lead(leads):
    """Удаляет заявку по номеру из списка (как в show_leads) и сохраняет CSV"""
    if not leads:
        print("Удалять нечего. Заявок нет.")
        return

    show_leads(leads)
    number = input_int("Введите номер заявки для удаления (0 - отмена): ")
    if number == 0:
        print("Отмена.")
        return
    if number < 1 or number > len(leads):
        print("Нет такой заявки.")
        return
    # Удаляем элемент (индексация с 0)
    deleted = leads.pop(number - 1)
    save_leads_to_csv(leads)
    print(f"Удалено: {deleted['created_at']} | {deleted['name']} | {deleted['phone']} | {deleted['service']}")

def edit_lead(leads):
    """Редактирует существующую заявку по номеру и сохраняет CSV"""
    if not leads:
        print("Редактировать нечего. Заявок нет.")
        return

    show_leads(leads)
    number = input_int("Введите номер заявки для редактирования (0 - отмена): ")
    if number == 0:
        print("Отмена.")
        return
    if number < 1 or number > len(leads):
        print("Нет такой заявки.")
        return

    # Получаем заявку для редактирования
    lead = leads[number - 1]
    print(f"Текущие данные: {lead['created_at']} | {lead['name']} | {lead['phone']} | {lead['service']}")
    print("Если хотите оставить поле без изменений, просто нажмите Enter.")

    # Редактируем имя
    new_name = input(f"Имя [{lead['name']}]: ").strip()
    if new_name:
        lead['name'] = new_name

    # Редактируем телефон (с проверкой)
    new_phone = input(f"Телефон [{lead['phone']}]: ").strip()
    if new_phone:
        # Можно добавить проверку через normalize_phone, но для простоты сохраняем как ввели
        lead['phone'] = new_phone

    # Редактируем услугу
    new_service = input(f"Услуга [{lead['service']}]: ").strip()
    if new_service:
        lead['service'] = new_service

    # Сохраняем изменения
    save_leads_to_csv(leads)
    print("Заявка обновлена и сохранена.")

def main():
    leads = load_leads_from_csv()

    try:
        while True:
            print()
            print("Меню:")
            print("1 - Добавить заявку")
            print("2 - Показать все заявки")
            print("3 - Поиск по телефону")
            print("4 - Удалить заявку")
            print("5 - Редактировать заявку")
            print("0 - Выход")
            choice = input("Выбор: ").strip()

            if choice == "1":
                add_lead(leads)
            elif choice == "2":
                show_leads(leads)
            elif choice == "3":
                phone_query = input_non_empty("Введите телефон или часть телефона: ")
                found = find_leads_by_phone(leads, phone_query)
                show_found_leads(found)
            elif choice == "4":
                delete_lead(leads)
            elif choice == "5":
                edit_lead(leads)
            elif choice == "0":
                print("Пока.")
                break
            else:
                print("Не понял. Выбери 1, 2, 3, 4 или 0.")
    except KeyboardInterrupt:
        # Красивый выход при нажатии Ctrl+C
        print()
        print("Остановка. Пока.")


if __name__ == "__main__":
    main()