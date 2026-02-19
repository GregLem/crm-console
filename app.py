import datetime


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Пусто введи значение: ")

def add_lead(leads):
    name = input_non_empty("Имя клиента: ")
    phone = input_non_empty("Телефон: ")
    service = input_non_empty("Услуга: ")

    lead = {
    "name": name,
    "phone": phone,
    "service": service,
    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    leads.append(lead)
    print("Заявка добавлена.")

def show_leads(leads):
    if not leads:
        print("Заявок пока нет.")
        return

    print("-" * 60)
    for i, lead in enumerate(leads, start=1):
        print(f"{i}. {lead['created_at']} | {lead['name']} | {lead['phone']} | {lead['service']}")
    print("-" * 60)

# Главная функция с меню
def main():
    leads = []  # пока храним заявки здесь

    while True:
        print()
        print("Меню:")
        print("1 - Добавить заявку")
        print("2 - Показать все заявки")
        print("0 - Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            add_lead(leads)
        elif choice == "2":
            show_leads(leads)
        elif choice == "0":
            print("Пока.")
            break
        else:
            print("Не понял. Выбери 1, 2 или 0.")

# Точка входа: код выполнится только при прямом запуске файла
if __name__ == "__main__":
    main()