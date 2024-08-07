import pymysql

# Замените 'localhost' на IP-адрес или имя хоста вашей базы данных
# Замените 'username' и 'password' на имя пользователя и пароль для базы данных
# Замените 'database' на имя вашей базы данных
connection = pymysql.connect(
    host='localhost',
    user='username',
    password='password',
    db='database',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        # Получаем все строки из первой таблицы "registration"
        sql = "SELECT id, surname, name, atronymic, birthday FROM registration"
        cursor.execute(sql)
        registration_rows = cursor.fetchall()

        for registration_row in registration_rows:
            try:
                # Проверяем, есть ли запись в second_table с таким же фамилией, именем и отчеством
                sql = "SELECT COUNT(*) as count FROM second_table WHERE surname = %s AND name = %s AND atronymic = %s"
                cursor.execute(sql, (registration_row['surname'], registration_row['name'], registration_row['atronymic']))
                is_second_tbl = cursor.fetchone()['count']

                if is_second_tbl > 0:
                    # Обновляем запись в registration, добавляя пометку "second_tbl"
                    sql = "UPDATE registration SET check = 'second_tbl' WHERE id = %s"
                    cursor.execute(sql, (registration_row['id'],))
                    print(f"Record {registration_row['id']} marked as second_tbl.")
                else:
                    # Проверяем, есть ли запись в третей таблице three_table
                    sql = "SELECT COUNT(*) as count FROM three_table WHERE surname = %s AND name = %s AND atronymic = %s AND birthday = %s"
                    cursor.execute(sql, (registration_row['surname'], registration_row['name'], registration_row['atronymic'], registration_row['birthday']))
                    is_approved = cursor.fetchone()['count']

                    if is_approved > 0:
                        sql = "UPDATE registrationt SET check = 'approved' WHERE id = %s"
                        cursor.execute(sql, (registration_row['id'],))
                        print(f"Record {registration_row['id']} approved.")
            except Exception as inner_e:
                print(f"Ошибка при обработке записи {registration_row['id']}: ", inner_e)

        # Сохраняем изменения в базу данных
        connection.commit()

except Exception as e:
    print("Ошибка при выполнении скрипта: ", e)

finally:
    connection.close()
