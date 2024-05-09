from flask import Flask, jsonify, request
from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Встановлення з'єднання з базою даних SQLite
db = SqliteDatabase('mydatabase.db')


# Оголошення моделі даних
class MyModel(Model):
    name = CharField()
    lastname = CharField()
    age = IntegerField()
    id = AutoField()

    class Meta:
        database = db  # Пов'язуємо модель з базою даних


# Підключення до бази даних
db.connect()


@app.route('/get_data')
def get_data():
    # Отримання даних з бази даних за допомогою Peewee
    data = list(MyModel.select().dicts())

    # Повернення даних у форматі JSON
    return jsonify(data)


@app.route('/save_data', methods=['POST'])
def save_data():
    data = request.json  # Отримання даних з POST-запиту у форматі JSON
    # Тепер ви можете використовувати ці дані, наприклад, зберігати їх у базі даних

    # Створення запису за допомогою моделі Peewee та збереження його в базі даних
    new_entry = MyModel(name=data['name'], lastname=data['lastname'], age=data['age'])
    new_entry.save()

    # Повертаємо відповідь у форматі JSON
    return jsonify({'message': 'Data received successfully!'})


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = MyModel.get(MyModel.id == user_id)
        user.delete_instance()
        return jsonify({'message': 'User deleted successfully!'})
    except MyModel.DoesNotExist:
        return jsonify({'error': 'User not found'}), 404


@app.route('/')
def index():
    return 'Welcome to my API!'


if __name__ == '__main__':
    app.run(debug=True)
