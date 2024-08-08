import sqlite3
from task import Task

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

    def create_task(self, my_task: Task):
        sql_insert_statement = f"""INSERT INTO tasks 
                                        (description, date_deadline, date_planned, 
                                         date_done, date_canceled, status, tags, refs)
                                values (?, ?, ?, ?, ?, ?, ?, ?);
                                """
        task = (my_task.description, my_task.date_deadline,  
                my_task.date_planned, my_task.date_done, my_task.date_canceled,
                my_task.status, my_task.tags, my_task.refs)
        try: 
            with sqlite3.connect(self.db_filename) as my_connection:
                my_cursor = my_connection.cursor()
                my_cursor.execute(sql_insert_statement, task)
                my_connection.commit()
        except sqlite3.Error as e:
            print("Error while inserting into database: ")
            print(e)


    def delete_task(self, task_id: int):
        sql_delete_statement = f"DELETE FROM tasks WHERE id=?;"
        try:
            with sqlite3.connect(self.db_filename) as my_connection:
                my_cursor = my_connection.cursor()
                my_cursor.execute(sql_delete_statement, (task_id,))
                my_connection.commit()
        except sqlite3.Error as e:
            print("Eror while deleting task from database:")
            print(e)

    def update_task(self, my_task: Task):
        sql_update_statement = """UPDATE tasks
        SET description = ?, date_deadline=?, 
        date_planned=?, date_done=?, date_canceled=?,
        status=?, tags=?,refs=?
        WHERE id=?
        """
        update_task_tuple=(my_task.description, my_task.date_deadline,
                           my_task.date_planned, my_task.date_done,
                           my_task.date_canceled, my_task.status, 
                           my_task.tags, my_task.refs, my_task.id)
        try:
            with sqlite3.connect(self.db_filename) as my_connection:
                my_cursor = my_connection.cursor()
                my_cursor.execute(sql_update_statement, update_task_tuple)
                my_connection.commit()
        except sqlite3.Error as e:
            print("Error while updating task: ")
            print(e)

    def convert_tuple_to_task(self, task_tuple: tuple) -> Task:
        my_task = Task(task_tuple[0], task_tuple[1], task_tuple[2], task_tuple[3],
                       task_tuple[4], task_tuple[5], task_tuple[6], task_tuple[7], 
                       task_tuple[8])
        return my_task

    def get_all_tasks(self) -> list[Task]:
        sql_select_all_statement="SELECT * FROM tasks;"
        rows = []
        try:
            with sqlite3.connect(self.db_filename) as my_connection:
                my_cursor = my_connection.cursor()
                my_cursor.execute(sql_select_all_statement)
                rows = my_cursor.fetchall()
        except sqlite3.Error as e:
            print("Error while retrieving all tasks from database: ", e)
        # rows is a list of tuples, we will convert this to a row of Task objects
        task_list = [self.convert_tuple_to_task(task_tuple) for task_tuple in rows]
        return task_list


if __name__ == '__main__':
    my_database = TaskDatabase("test_todo.sqlite3")
    first_task = Task(id=None, description="gras maaien", date_deadline='2024-08-07',
                   date_planned='2024-08-07', date_done=None, date_canceled=None, 
                   status='todo', tags=None, refs=None)
    second_task = Task(id=None, description='brood halen', date_deadline=None,
                       date_planned='2024-08-07', date_done=None, date_canceled=None,
                       status='todo', tags='#thuis', refs=None)
    my_database.create_task(first_task)
    my_database.create_task(second_task)
    my_database.delete_task(1)
    second_task.tags = '#thuis #persoonlijk'
    second_task.id = 2
    my_database.update_task(second_task)
    third_task = Task(id=None, description='vrijstelling onderozken van Farouk. Gemaild begin juli. Al een kort antwoord gegeven. Dossier moet nog verder onderzocht worden', date_deadline=None,
                       date_planned='2024-08-07', date_done=None, date_canceled=None,
                       status='todo', tags='#thuis', refs=None)
    my_database.create_task(third_task)
    all_tasks = my_database.get_all_tasks()
    for task in all_tasks:
        print(task)
