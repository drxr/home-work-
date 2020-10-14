account_1 = {'login': 'ivan', 'password': 'q1'}
account_2 = {'login': 'petr', 'password': 'q2'}
account_3 = {'login': 'olga', 'password': 'q3'}
account_4 = {'login': 'anna', 'password': 'q4'}

user_1 = {'name': 'Иван', 'age': 20, 'account': account_1}
user_2 = {'name': 'Петр', 'age': 25, 'account': account_2}
user_3 = {'name': 'Ольга', 'age': 18, 'account': account_3}
user_4 = {'name': 'Анна', 'age': 27, 'account': account_4}

users_list = [user_1, user_2, user_3, user_4]

choice = input('Введите ключ (name или account): ').lower()

if choice in ['name', 'account']:
    print(f' Значение ключа {choice} для юзера 1 = {user_1[choice]}')
    print(f' Значение ключа {choice} для юзера 2 = {user_2[choice]}')
    print(f' Значение ключа {choice} для юзера 3 = {user_3[choice]}')
    print(f' Значение ключа {choice} для юзера 4 = {user_4[choice]}')
else:
    print('Введенный ключ не найден')

number = int(input('Введите порядковый номер: '))
if number in range(1, 5):
    print(f'Данные по юзеру № {number}')
    print(f"Имя: {users_list[number - 1]['name']}")
    print(f"Возраст: {users_list[number - 1]['age']}")
    print(f"Логин: {users_list[number - 1]['account']['login']}")
    print(f"Пароль: {users_list[number - 1]['account']['password']}")
else:
    print('Порядковый номер не найден')

eraser = int(input('Введите номер пользователя, которого нужно переместить в конец: '))

print(users_list)
print(users_list[eraser - 1])
users_list.append(users_list.pop(eraser - 1))
print(users_list)

sum_age = []
for user in users_list:
    sum_age.append(user['age'])
print(f'Средний возраст всех юзеров {sum(sum_age) / len(sum_age)} лет')
