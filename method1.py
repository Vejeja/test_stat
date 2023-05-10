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

# Метод для сохранения событий
@app.route('/events', methods=['POST'])
def save_event():
    # Получение данных из запроса
    event_name = request.json['event_name']
    is_authorized = request.json['is_authorized']
    ip_address = request.remote_addr
    
    # Добавление вспомогательной информации
    user_agent = request.headers.get('User-Agent')
    
    # Сохранение события в базе данных
    cur = conn.cursor()
    cur.execute("INSERT INTO events (event_name, is_authorized, ip_address, user_agent) VALUES (%s, %s, %s, %s)", (event_name, is_authorized, ip_address, user_agent))
    conn.commit()
    cur.close()
    
    return jsonify({'message': 'Event saved successfully'})

if __name__ == '__main__':
    app.run(debug=True)