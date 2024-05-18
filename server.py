from flask import Flask, jsonify, request
from peewee import SqliteDatabase, Model, CharField, IntegerField, AutoField, ForeignKeyField
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Встановлення з'єднання з базою даних SQLite
db = SqliteDatabase('mydatabase.db')


class BaseModel(Model):
    class Meta:
        database = db


class KyivanPrince(Model):
    name = CharField()
    id = AutoField()

    class Meta:
        table_name = 'kyivan_prince'
        database = db


class MyModel(Model):
    name = CharField()
    lastname = CharField()
    age = IntegerField()
    id = AutoField()
    prince = ForeignKeyField(KyivanPrince, backref='my_models')

    class Meta:
        database = db


db.connect()
db.drop_tables([MyModel])
db.create_tables([KyivanPrince, MyModel])
# Додайте імена князів до таблиці
# Оновіть імена князів у таблиці
kyivan_princes = ['Олег', 'Ігор', 'Олександр', 'Володимир', 'Ярослав']
for i, name in enumerate(kyivan_princes, start=1):
    prince = KyivanPrince.get_or_none(id=i)
    if prince:
        prince.name = name
        prince.save()

# Отримайте ім'я князя з таблиці kyivan_prince
kyivan_princes = KyivanPrince.select()

# Оновіть записи в таблиці MyModel
with db.atomic():
    for model_instance, prince_name in zip(MyModel.select(), KyivanPrince.select()):
        # Перевірте, чи існує принц у базі даних
        prince = KyivanPrince.get_or_none(KyivanPrince.name == prince_name.name)
        if prince:
            model_instance.name = prince_name.name
            model_instance.prince = prince.id
            model_instance.save()


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


@app.route('/save_item', methods=['POST'])
def save_item():
    data = request.json  # Отримання даних з POST запиту
    item_id = data['id']
    name = data['name']
    lastname = data['lastname']
    age = data['age']

    # Оновлення даних елемента у базі даних
    item = MyModel.get_by_id(item_id)
    item.name = name
    item.lastname = lastname
    item.age = age
    item.save()

    return jsonify({'message': 'Item updated successfully'})


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


@app.route('/api/kyivan_princes', methods=['GET'])
def get_kyivan_princes():
    princes = KyivanPrince.select()
    princes_list = [{'id': prince.id, 'name': prince.name} for prince in princes]
    return jsonify(princes_list)


if __name__ == '__main__':
    app.run(debug=True)
