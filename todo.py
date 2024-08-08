from task import Task
from database import TaskDatabase
import npyscreen

class RecordList(npyscreen.MultiLineAction):
    pass

class RecordListDisplay(npyscreen.FormMutt):
    MAIN_WIDGET_CLASS = RecordList
    
    def beforeEditing(self):
        self.update_list()

    def update_list(self):
        self.wStatus1.value = "a: all tasks | d: todo by deadline | p: todo by planned | t: today | D: done | C: cancelled"
        self.wStatus2.value = "ctrl-a: add | ctrl-d: delete | ctrl-x: set done | ctrl-c: cancel | enter: update task | :q = quit"
        self.wMain.values = self.parentApp.myDatabase.get_all_tasks()
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
