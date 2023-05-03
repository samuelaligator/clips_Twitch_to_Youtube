import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('TwitchClips.db')
        self.cur = self.conn.cursor()

    def create_table(self, table_name):
        print(f'creating the table {table_name}')
        create_table = f''' CREATE TABLE IF NOT EXISTS {table_name}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT)'''
        self.cur.execute(create_table)
        self.conn.commit()

    def delete_table(self, table_name):
        print(f"deleting the table {table_name}")
        self.cur.execute(f'''DROP TABLE IF EXISTS {table_name}''')
        self.conn.commit()

    def table_length(self, table_name):
        print(f"getting the size of the table {table_name}")
        return self.cur.execute(f'''SELECT COUNT(*) FROM {table_name}''').fetchone()[0]

    def select_data(self, column_name, table_name, other_arguments=""):
        print(f"selecting data from column {column_name} of table {table_name}")
        return self.cur.execute(
            f'''SELECT {column_name} FROM {table_name} {other_arguments}''').fetchall()

    def fill_StreamersName(self, streamer_name):
        print(f"filling the table StreamersName with the data : '{streamer_name}'")
        insert = '''INSERT INTO StreamersName (streamer) VALUES (?)'''
        self.cur.execute(insert, (streamer_name,))
        self.conn.commit()

    def fill_Clips(self, clips_informations):
        print("filling the table (Clips) with the most viewed clips of the last 30 days")
        insert = '''INSERT INTO Clips (title, views, category, streamer, author, link) VALUES (?, ?, ?, ?, ?, ?)'''
        self.cur.executemany(insert, clips_informations)
        self.conn.commit()

    def add_column(self, table_name, column_name, type_of_column):
        print(f"adding the column {column_name} into {table_name}")
        self.cur.execute(f'''ALTER TABLE {table_name} ADD COLUMN {column_name} {type_of_column.upper()} ''')
        self.conn.commit()

    def update(self, table_name, set_column, where_column, data1, data2):
        print(f"updating the column {set_column} with the data {data1} of {table_name}")
        update = f'''UPDATE {table_name} SET {set_column} = ? WHERE {where_column} = ?'''
        self.cur.execute(update, (data1, data2))
        self.conn.commit()
