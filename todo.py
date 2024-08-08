from task import Task
from database import TaskDatabase
import npyscreen

class RecordList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(RecordList, self).__init__(*args, **keywords)
        self.add_handlers({
                        "a": self.set_list_all_tasks, 
                        "d": self.set_list_todo_by_deadline,
                        "c": self.set_list_todo_by_planned
        })

    def set_list_todo_by_deadline(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        todo_tasks = [task for task in all_tasks if task.status == 'todo']
        sorted_todo_tasks_by_deadline = sorted(todo_tasks, key=lambda task: task.date_deadline, reverse=True)
        self.parent.display_list = sorted_todo_tasks_by_deadline
        self.parent.update_list()

    def set_list_all_tasks(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda task: task.id, reverse=True)
        self.parent.display_list = sorted_tasks
        self.parent.update_list()

    def set_list_todo_by_planned(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        todo_tasks = [task for task in all_tasks if task.status == 'todo']
        sorted_todo_tasks_by_planned = sorted(todo_tasks, key=lambda task: task.date_planned, reverse=True)
        self.parent.display_list = sorted_todo_tasks_by_planned
        self.parent.update_list()


class RecordListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = RecordList
    
    def beforeEditing(self):
        self.display_list = self.parentApp.myDatabase.get_all_tasks()
        self.update_list()

    def update_list(self):
        self.wStatus1.value = "a: all tasks | d: todo by deadline | c: todo by planned | t: today | D: done | C: cancelled"
        self.wStatus2.value = "ctrl-a: add | ctrl-d: delete | ctrl-x: set done | ctrl-c: cancel | enter: update task | :q = quit"
        self.wMain.values = self.display_list
        self.wMain.display()


class EditRecord(npyscreen.ActionForm):
    pass

class TaskApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = TaskDatabase()
        self.addForm("MAIN", RecordListDisplay)
        self.addForm("EDITRECDORDFM", EditRecord)

if __name__ == '__main__':
    myApp = TaskApplication()
    myApp.run()
