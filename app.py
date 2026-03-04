import csv
import datetime

CSV_FILE = "leads.csv"
FIELDNAMES = ["created_at", "name", "phone", "service", "status"]

# Возможные статусы заявки
STATUSES = ["новая", "в работе", "выполнена", "отменена"]


class Lead:
    """Класс, представляющий одну заявку"""
    def __init__(self, name: str, phone: str, service: str):
        self.name = name
        self.phone = phone
        self.service = service
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.status = "новая"  # По умолчанию

    def __str__(self):
        """Для красивого вывода в консоль"""
        return f"{self.created_at} | {self.name} | {self.phone} | {self.service} | {self.status}"


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
        writer.writeheader()
        leads_dicts = []
        for lead in leads:
            leads_dicts.append({
                "created_at": lead.created_at,
                "name": lead.name,
                "phone": lead.phone,
                "service": lead.service,
                "status": lead.status
            })
        writer.writerows(leads_dicts)


def load_leads_from_csv(filename=CSV_FILE):
    """Загружает заявки из CSV. Если файла нет, возвращает пустой список."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            leads = []
            for row in reader:
                lead = Lead(
                    name=row.get("name", "").strip(),
                    phone=row.get("phone", "").strip(),
                    service=row.get("service", "").strip()
                )
                lead.created_at = row.get("created_at", "").strip()
                lead.status = row.get("status", "новая").strip()
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
    """Добавляет новую заявку (объект Lead) и сохраняет"""
    name = input_non_empty("Имя клиента: ")
    phone = input_phone("Телефон: ")
    service = input_non_empty("Услуга: ")

    lead = Lead(name, phone, service)
    leads.append(lead)
    save_leads_to_csv(leads)
    print("Заявка добавлена и сохранена.")


def show_leads(leads):
    """Показывает все заявки в консоли с красивым форматированием"""
    if not leads:
        print("Заявок пока нет.")
        return

    # Ширина колонок
    w_date = 16
    w_name = 18
    w_phone = 14
    w_service = 18
    w_status = 10

    def cut(s, w):
        s = s or ""
        return (s[: w - 1] + "...") if len(s) > w else s

    header = (
        "№".ljust(4)
        + "Дата".ljust(w_date + 2)
        + "Клиент".ljust(w_name + 2)
        + "Телефон".ljust(w_phone + 2)
        + "Услуга".ljust(w_service + 2)
        + "Статус".ljust(w_status + 2)
    )
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for i, lead in enumerate(leads, start=1):
        line = (
            str(i).ljust(4)
            + cut(lead.created_at, w_date).ljust(w_date + 2)
            + cut(lead.name, w_name).ljust(w_name + 2)
            + cut(lead.phone, w_phone).ljust(w_phone + 2)
            + cut(lead.service, w_service).ljust(w_service + 2)
            + cut(lead.status, w_status).ljust(w_status + 2)
        )
        print(line)

    print("-" * len(header))
    print(f"Всего заявок: {len(leads)}")


def find_leads_by_phone(leads, phone_query):
    """Ищет заявки по телефону (по цифрам, частичное совпадение)"""
    q = normalize_phone(phone_query)
    if not q:
        return []

    result = []
    for lead in leads:
        lead_phone = normalize_phone(lead.phone)
        if q in lead_phone:
            result.append(lead)
    return result


def show_found_leads(found):
    """Показывает найденные заявки (коротко)"""
    if not found:
        print("Ничего не найдено.")
        return

    print(f"Найдено: {len(found)}")
    print("-" * 70)
    for i, lead in enumerate(found, start=1):
        print(f"{i}. {lead.created_at} | {lead.name} | {lead.phone} | {lead.service} | {lead.status}")
    print("-" * 70)


def delete_lead(leads):
    """Удаляет заявку по номеру из списка и сохраняет CSV"""
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

    deleted = leads.pop(number - 1)
    save_leads_to_csv(leads)
    print(f"Удалено: {deleted.created_at} | {deleted.name} | {deleted.phone} | {deleted.service} | {deleted.status}")


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

    lead = leads[number - 1]
    print(f"Текущие данные: {lead.created_at} | {lead.name} | {lead.phone} | {lead.service} | {lead.status}")
    print("Если хотите оставить поле без изменений, просто нажмите Enter.")

    new_name = input(f"Имя [{lead.name}]: ").strip()
    if new_name:
        lead.name = new_name

    new_phone = input(f"Телефон [{lead.phone}]: ").strip()
    if new_phone:
        lead.phone = new_phone

    new_service = input(f"Услуга [{lead.service}]: ").strip()
    if new_service:
        lead.service = new_service

    # Редактирование статуса
    print("Выберите новый статус (или Enter, чтобы оставить текущий):")
    for idx, s in enumerate(STATUSES, start=1):
        print(f"{idx} - {s}")
    status_choice = input(f"Статус [{lead.status}]: ").strip()
    if status_choice:
        try:
            idx = int(status_choice) - 1
            if 0 <= idx < len(STATUSES):
                lead.status = STATUSES[idx]
            else:
                print("Неверный номер, статус не изменён.")
        except ValueError:
            print("Нужно ввести число, статус не изменён.")

    save_leads_to_csv(leads)
    print("Заявка обновлена и сохранена.")


def show_today_leads(leads):
    """Показывает заявки, созданные сегодня"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_leads = [lead for lead in leads if lead.created_at.startswith(today)]
    if not today_leads:
        print("За сегодня заявок нет.")
    else:
        print(f"\nЗаявки за {today}:")
        show_leads(today_leads)


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
            print("6 - Показать за сегодня")
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
            elif choice == "6":
                show_today_leads(leads)
            elif choice == "0":
                print("Пока.")
                break
            else:
                print("Не понял. Выбери 1, 2, 3, 4, 5, 6 или 0.")
    except KeyboardInterrupt:
        print()
        print("Остановка. Пока.")


if __name__ == "__main__":
    main()