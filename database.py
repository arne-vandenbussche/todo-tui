import sqlite3

class TaskDatabase:
    def __init__(self, filename="todo.sqlite3"):
        self.db_filename = filename
        db_connection = sqlite3.connect(self.db_filename)
        my_cursor = db_connection.cursor()
        sql_create_statement = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            date_deadline DATE,
            date_planned DATE,
            date_done DATE,
            date_canceled DATE,
            status TEXT CHECK (status in ('todo', 'done', 'canceled')),
            tags TEXT, -- tags single words starting with #
            refs TEXT -- references (mail, files, sites) where you can find more info about the task
        );
        """
        my_cursor.execute(sql_create_statement)
        db_connection.commit()
        db_connection.close()

    def create_task(self):
        pass


if __name__ == '__main__':
    my_database = TaskDatabase("test_todo.sqlite3")


