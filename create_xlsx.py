import pandas as pd
from datetime import datetime
import os

def calculate_age(birth_date_str):
    """ Обчислює вік на основі дати народження у форматі 'дд.мм.рррр' """
    try:
        birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y')
        today = datetime.now()
        age = today.year - birth_date.year
        
        # Перевіряємо, чи вже був день народження цього року
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
            
        return age
    except:
        return None

def get_age_category(age):
    """ Повертає категорію віку на основі віку """
    if age < 18:
        return "younger_18"
    elif 18 <= age <= 45:
        return "18-45"
    elif 46 <= age <= 70:
        return "45-70"
    else:
        return "older_70"

def main():
    try:
        # Перевіряємо існування CSV файлу
        if not os.path.exists('employees.csv'):
            print("Помилка: Файл employees.csv не знайдено")
            return
        
        # Читаємо CSV файл
        df = pd.read_csv('employees.csv', encoding='utf-8')
        
        # Додаємо стовпець з віком
        df['Вік'] = df['Дата народження'].apply(calculate_age)
        
        # Створюємо Excel файл з кількома аркушами
        with pd.ExcelWriter('employees_analysis.xlsx', engine='openpyxl') as writer:
            # Аркуш "all" - всі дані
            df.to_excel(writer, sheet_name='all', index=False)
            
            # Стовпці для вікових категорій
            age_category_columns = ['Прізвище', 'Ім\'я', 'По батькові', 'Дата народження', 'Вік']
            
            # Аркуш "younger_18" - молодші 18 (лише обрані стовпці)
            younger_18 = df[df['Вік'] < 18][age_category_columns].copy()
            younger_18.reset_index(drop=True, inplace=True)
            younger_18.index = younger_18.index + 1  # Починаємо з 1
            younger_18.to_excel(writer, sheet_name='younger_18', index=True, index_label='№')
            
            # Аркуш "18-45" - від 18 до 45 (лише обрані стовпці)
            age_18_45 = df[(df['Вік'] >= 18) & (df['Вік'] <= 45)][age_category_columns].copy()
            age_18_45.reset_index(drop=True, inplace=True)
            age_18_45.index = age_18_45.index + 1
            age_18_45.to_excel(writer, sheet_name='18-45', index=True, index_label='№')
            
            # Аркуш "45-70" - від 45 до 70 (лише обрані стовпці)
            age_45_70 = df[(df['Вік'] >= 45) & (df['Вік'] <= 70)][age_category_columns].copy()
            age_45_70.reset_index(drop=True, inplace=True)
            age_45_70.index = age_45_70.index + 1
            age_45_70.to_excel(writer, sheet_name='45-70', index=True, index_label='№')
            
            # Аркуш "older_70" - старші 70 (лише обрані стовпці)
            older_70 = df[df['Вік'] > 70][age_category_columns].copy()
            older_70.reset_index(drop=True, inplace=True)
            older_70.index = older_70.index + 1
            older_70.to_excel(writer, sheet_name='older_70', index=True, index_label='№')
        
        print("Ok")
        
    except FileNotFoundError:
        print("Помилка: Файл employees.csv не знайдено")
    except PermissionError:
        print("Помилка: Немає дозволу на запис у файл")
    except Exception as e:
        print(f"Помилка при створенні XLSX файлу: {e}")

if __name__ == '__main__':
    main()