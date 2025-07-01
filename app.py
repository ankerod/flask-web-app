from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_NAME = os.environ.get('POSTGRES_DB', 'mydatabase')
DB_USER = os.environ.get('POSTGRES_USER', 'myuser')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'mypassword')

def get_db_connection():
    """Встановлює з'єднання з базою даних PostgreSQL."""
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

@app.route('/', methods=('GET', 'POST'))
def index():
    """
    Головна сторінка додатку.
    Обробляє відображення і збереження записів.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Якщо форма була надіслана, беремо текст і зберігаємо його
        entry_text = request.form['entry_text']
        if entry_text:
            try:
                cursor.execute('INSERT INTO entries (text) VALUES (%s)', (entry_text,))
                conn.commit()
            except Exception as e:
                print(f"Помилка при вставці даних: {e}")
                conn.rollback() # Відкочуємо зміни в разі помилки
            return redirect(url_for('index')) # Перенаправляємо, щоб уникнути повторного надсилання форми

    # Отримуємо всі записи з бази даних для відображення
    cursor.execute('SELECT id, text, created_at FROM entries ORDER BY created_at DESC')
    entries = cursor.fetchall()
    conn.close() # Закриваємо з'єднання з базою даних

    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    # При першому запуску, створимо таблицю, якщо її не існує
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Помилка при створенні таблиці: {e}")

    app.run(debug=True, host='0.0.0.0') # Запускаємо додаток