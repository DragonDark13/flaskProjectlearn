from peewee import SqliteDatabase, Model, CharField, IntegerField

# Встановлення з'єднання з базою даних SQLite
db = SqliteDatabase('mydatabase.db')

# Оголошення моделі даних
class MyModel(Model):
    name = CharField()
    lastname = CharField()
    age = IntegerField()

    class Meta:
        database = db  # Пов'язуємо модель з базою даних

# Підключення до бази даних
db.connect()

# Створення таблиць, якщо вони ще не існують
MyModel.drop_table()
db.create_tables([MyModel])

# Створення нових записів
new_entry = MyModel(name='John', lastname='Smith', age=30)
aleksandr = MyModel(name="Aleksandr", lastname='Zachkevich', age=31)

# Збереження записів в базі даних
new_entry.save()
aleksandr.save()

sq = MyModel.select().order_by(MyModel.lastname)

for person in sq:
    print('{} {} {} age {}'.format(
        person.name,
        person.lastname,
        person.age,
        person.id
    ))
