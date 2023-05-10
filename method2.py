from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myusername",
    password="mypassword"
)

# Метод для получения статистики
@app.route('/statistics', methods=['GET'])
def get_statistics():
    # Получение параметров из запроса
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    event_name = request.args.get('event_name')
    
    # Формирование SQL-запроса
    sql = "SELECT COUNT(*) FROM events WHERE 1=1"
    params = []
    
    if start_date:
        sql += " AND created_at >= %s"
        params.append(start_date)
    
    if end_date:
        sql += " AND created_at <= %s"
        params.append(end_date)
    
    if event_name:
        sql += " AND event_name = %s"
        params.append(event_name)
    
    # Выполнение SQL-запроса
    cur = conn.cursor()
    cur.execute(sql, tuple(params))
    result = cur.fetchone()[0]
    cur.close()
    
    # Формирование ответа в формате JSON
    response = {
        'event_count': result,
        'ip_count': 0,  # TODO: добавить подсчет по IP адресу
        'authorized_count': 0  # TODO: добавить подсчет по статусу пользователя
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)