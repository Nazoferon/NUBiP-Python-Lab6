import pandas as pd
import matplotlib.pyplot as plt
import os

# Налаштування шрифтів для підтримки української мови
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.sans-serif'] = ['Times New Roman']

def calculate_age(birth_date_str):
    """ Обчислює вік на основі дати народження у форматі 'дд.мм.рррр' """
    from datetime import datetime
    try:
        birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y')
        today = datetime.now()
        age = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
            
        return age
    except:
        return None

def main():
    try:
        # Перевірка наявності файлу
        if not os.path.exists('employees.csv'):
            print("Помилка: Файл employees.csv не знайдено")
            return
        
        # Читання CSV файлу
        df = pd.read_csv('employees.csv', encoding='utf-8')
        
        # Обчислення віку для кожного працівника
        df['Вік'] = df['Дата народження'].apply(calculate_age)
        
        def get_age_category(age):
            """ Повертає категорію віку на основі віку """
            if age < 18:
                return "Молодші 18"
            elif 18 <= age <= 45:
                return "18-45"
            elif 46 <= age <= 70:
                return "45-70"
            else:
                return "Старші 70"
        
        df['Категорія віку'] = df['Вік'].apply(get_age_category)
        
        print("Ok")
        
        # 1. Аналіз по статі
        print("\n=== АНАЛІЗ ПО СТАТІ ===")
        gender_counts = df['Стать'].value_counts()
        print(f"Чоловіки: {gender_counts.get('Чоловік', 0)}")
        print(f"Жінки: {gender_counts.get('Жінка', 0)}")
        
        # Діаграма по статі
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 2, 1)
        gender_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightpink'])
        plt.title('Розподіл співробітників по статі')
        plt.ylabel('')
        
        # 2. Аналіз по віковим категоріям
        print("\n=== АНАЛІЗ ПО ВІКОВИМ КАТЕГОРІЯМ ===")
        age_category_counts = df['Категорія віку'].value_counts()
        for category, count in age_category_counts.items():
            print(f"{category}: {count}")
        
        # Діаграма по віковим категоріям
        plt.subplot(2, 2, 2)
        age_category_counts.plot(kind='bar', color='lightgreen')
        plt.title('Розподіл по віковим категоріям')
        plt.xlabel('Вікова категорія')
        plt.ylabel('Кількість')
        plt.xticks(rotation=45)
        
        # 3. Аналіз по статі в кожній віковій категорії
        print("\n=== АНАЛІЗ ПО СТАТІ В КОЖНІЙ ВІКОВІЙ КАТЕГОРІЇ ===")
        cross_tab = pd.crosstab(df['Категорія віку'], df['Стать'])
        print(cross_tab)
        
        # Діаграма по статі в кожній віковій категорії
        plt.subplot(2, 1, 2)
        cross_tab.plot(kind='bar', color=['lightpink', 'lightblue'])
        plt.title('Розподіл по статі в кожній віковій категорії')
        plt.xlabel('Вікова категорія')
        plt.ylabel('Кількість')
        plt.legend(title='Стать')
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('analysis_diagrams.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Додаткова діаграма
        # Кругова діаграма по віковим категоріям
        plt.figure(figsize=(8, 8))
        age_category_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'gold', 'lightcoral'])
        plt.title('Розподіл співробітників по віковим категоріям')
        plt.ylabel('')
        plt.savefig('age_categories_pie.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    except FileNotFoundError:
        print("Помилка: Файл employees.csv не знайдено")
    except Exception as e:
        print(f"Помилка при аналізі даних: {e}")

if __name__ == '__main__':
    main()