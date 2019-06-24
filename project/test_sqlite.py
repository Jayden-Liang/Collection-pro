import sqlite3

connection = sqlite3.connect("app.db")

cursor = connection.cursor()

cursor.execute("SELECT * FROM todo")

result = cursor.fetchall()
for r in result:
    print(r[1])














# def create(conn):
#     sql_create = '''
#          CREATE TABLE `users`(
#          `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#          `username` TEXT NOT NULL UNIQUE,
#          `password` TEXT NOT NULL,
#          `email` TEXT
#          )
#     '''
#     conn.execute(sql_create)
#     print('创建成功')
#
# def select(conn):
#     sql='''
#       SELECT
#          *
#       FROM
#          users
#     '''
#     cursor = conn.execute(sql)
#     print(list(cursor))
#     # for row in cursor:
#     #     print(row)
# def insert(conn, username, password, email):
#     sql_insert ='''
#         INSERT INTO
#         `users` (`username`,`password`,`email`)
#         VALUES
#             (?,?,?);    #如果这里传入了数据，则用conn.execute(sql_insert)
#     '''
#     conn.execute(sql_insert, (username, password, email))
#
# def update(conn, user_id, email):
#     sql_update='''
#         UPDATE
#             `users`
#         SET
#             `email`=?
#         WHERE
#             `id`=?
#     '''
#     conn.execute(sql_update, (email, user_id))
#
# def delete(conn, user_id):
#     sql_delete = '''
#        DELETE FROM
#            users
#         WHERE
#             id=?
#     '''
#     conn.execute(sql_delete, (user_id,))
# def main():
#     db_path='text_.sqlite'
#     conn = sqlite3.connect(db_path)
#     # create(conn)
#     insert(conn,'jayden', '123', 'gua@qq.com')
#     select(conn)
#     conn.commit()
#     conn.close()



#
# if __name__ == '__main__':
#     main()