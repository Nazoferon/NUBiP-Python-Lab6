import csv
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker(locale='uk_UA')

# Словник для імен по батькові
male_middle_names = [
    'Андрійович', 'Олександрович', 'Сергійович', 'Іванович', 'Петрович',
    'Васильович', 'Миколайович', 'Володимирович', 'Богданович', 'Тарасович',
    'Юрійович', 'Дмитрович', 'Анатолійович', 'Вікторович', 'Геннадійович',
    'Євгенович', 'Романович', 'Станіславович', 'Федорович', 'Ярославович'
]

female_middle_names = [
    'Андріївна', 'Олександрівна', 'Сергіївна', 'Іванівна', 'Петрівна',
    'Василівна', 'Миколаївна', 'Володимирівна', 'Богданівна', 'Тарасівна',
    'Юріївна', 'Дмитрівна', 'Анатоліївна', 'Вікторівна', 'Геннадіївна',
    'Євгенівна', 'Романівна', 'Станіславівна', 'Федорівна', 'Ярославівна'
]

def generate_employee():
    # Визначення статі (60% чоловіків, 40% жінок)
    is_male = random.random() < 0.6
    
    if is_male:
        first_name = fake.first_name_male()
        middle_name = random.choice(male_middle_names)
        gender = 'Чоловік'
    else:
        first_name = fake.first_name_female()
        middle_name = random.choice(female_middle_names)
        gender = 'Жінка'
    
    last_name = fake.last_name()
    
    # Дата народження
    start_date = datetime(1938, 1, 1)
    end_date = datetime(2008, 12, 31)
    birth_date = fake.date_between(start_date=start_date, end_date=end_date)

    # Посада
    position = fake.job()
    
    # Місто проживання
    city = fake.city()
    
    # Адреса проживання
    address = fake.address().replace('\n', ', ')
    
    # Телефон
    phone = fake.phone_number()
    
    # Email
    email = fake.email()
    
    return {
        'Прізвище': last_name,
        'Ім\'я': first_name,
        'По батькові': middle_name,
        'Стать': gender,
        'Дата народження': birth_date.strftime('%d.%m.%Y'),
        'Посада': position,
        'Місто проживання': city,
        'Адреса проживання': address,
        'Телефон': phone,
        'Email': email
    }

def main():
    try:
        with open('employees.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Прізвище', 'Ім\'я', 'По батькові', 'Стать', 'Дата народження',
                'Посада', 'Місто проживання', 'Адреса проживання', 'Телефон', 'Email'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for i in range(2000):
                employee = generate_employee()
                writer.writerow(employee)
                """employee — це звичайний Python-словник із ключами та значеннями.
                    csv.DictWriter бере цей словник і серіалізує його: перетворює у рядок, 
                    де значення розділені комами (CSV-формат).
                    Потім цей рядок записується у файл employees.csv."""
                
                if (i + 1) % 100 == 0:
                    print(f'Згенеровано {i + 1} записів')
            
            print(f'Успішно згенеровано 2000 записів у файл employees.csv')
            
    except Exception as e:
        print(f'Помилка при створенні CSV файлу: {e}')

if __name__ == '__main__':
    main()