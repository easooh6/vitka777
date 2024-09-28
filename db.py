import sqlite3



class Database:
    def __init__(self, db_name) -> None:
        self.con = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.con.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT (DATETIME(CURRENT_TIMESTAMP, '+5 hours'))
            );
        """)
        self.con.commit()
    
    def add_item(self, name, price, description=''):
        try:
            if name == '':
                print("Название не может быть пустым.")
                return
            if price <= 0:
                print("Цена должна быть больше 0.")
                return

            self.cur.execute('INSERT INTO Items (name, description, price) VALUES (?, ?, ?)', (name, description, price))
            self.con.commit()
            print("Элемент добавлен.")

        except sqlite3.Error as e:
            print(f"Ошибка при добавлении записи: {e}")

    def update_item_name(self, id, name):
        try:
            if name != '':
                self.cur.execute("UPDATE Items SET name = ? WHERE id = ?", (name, id))
                self.con.commit()
                print(f"Имя элемента с id {id} обновлено.")
            else:
                print("Название не может быть пустым.")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении имени: {e}")


    def update_item_price(self, id, price):
        try:
            if price > 0:
                self.cur.execute("UPDATE Items SET price = ? WHERE id = ?", (price, id))
                self.con.commit()
                print(f"Цена элемента с id {id} обновлена.")
            else:
                print("Цена не может быть меньше или равна 0.")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении цены: {e}")


    def update_item_description(self, id, description):
        try:
            self.cur.execute("UPDATE Items SET description = ? WHERE id = ?", (description, id))
            self.con.commit()
            print(f"Описание элемента с id {id} обновлено.")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении описания: {e}")


    def get_item(self, id):
        try:
            self.cur.execute("""
                SELECT * FROM Items WHERE id = ?;
            """, (id,))
            
            item = self.cur.fetchone()

            if item:
                return {
                    "id": item[0],
                    "name": item[1],
                    "description": item[2],
                    "price": item[3],
                    "created_at": item[4]
                }
            else:
                print(f"Запись с id {id} не найдена.")
                return {}

        except sqlite3.Error as e:
            print(f"Ошибка при получении записи: {e}")
            return {}
        
    def delete_item(self, id=-1, name=''):
        try:
            if id > 0:
                self.cur.execute("DELETE FROM Items WHERE id = ?;", (id,))
                self.con.commit()
                print(f"Запись с id {id} удалена.")
            
            elif name != '':
                self.cur.execute("DELETE FROM Items WHERE name = ?;", (name,))
                self.con.commit()
                print(f"Запись с именем '{name}' удалена.")
            
            else:
                print("Неверные аргументы: укажите либо id, либо name.")

        except sqlite3.Error as e:
            print(f"Ошибка при удалении записи: {e}")
    def close(self):
        self.con.close()
if __name__ == '__main__':
    db = Database('main.db')
    db.close()