from task import Task
from database import TaskDatabase
import npyscreen
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

class RecordList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(RecordList, self).__init__(*args, **keywords)
        self.add_handlers({
                        "a": self.set_list_all_tasks, 
                        "d": self.set_list_todo_by_deadline,
                        "c": self.set_list_todo_by_planned,
                        "D": self.set_list_done,
                        "C": self.set_list_canceled,
                        "t": self.set_list_today,
                        "^D": self.when_delete_record,
                        "^A": self.when_add_record,
                        "^X": self.when_set_task_done,
                        "^Q": self.when_cancel_task
        })

    def actionHighlighted(self, act_on_this, keypress):
        self.parent.parentApp.getForm('EDITRECORDFM').value=act_on_this.id
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_delete_record(self, *args, **keywords):
        self.parent.parentApp.myDatabase.delete_task(self.values[self.cursor_line].id)
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        self.parent.display_list = all_tasks
        self.parent.update_list()

    def when_add_record(self, *args, **keywords):
        self.parent.parentApp.getForm('EDITRECORDFM').value = None
        self.parent.parentApp.switchForm('EDITRECORDFM')

    def when_set_task_done(self, *args, **keywords):
        task = self.values[self.cursor_line]
        task.status = 'done'
        task.date_done = datetime.today().strftime('%Y-%m-%d')
        self.parent.parentApp.myDatabase.update_task(task)
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        self.set_list_today()

    def when_cancel_task(self, *args, **keywords):
        task = self.values[self.cursor_line]
        task.status = 'canceled'
        task.date_canceled = datetime.today().strftime('%Y-%m-%d')
        self.parent.parentApp.myDatabase.update_task(task)
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        self.set_list_today()

    def set_list_todo_by_deadline(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        todo_tasks = [task for task in all_tasks if task.status == 'todo']
        todo_tasks_without_deadline = [task for task in todo_tasks if task.date_deadline is None or task.date_deadline == '']
        todo_tasks_with_deadline = [task for task in todo_tasks if task.date_deadline is not None and task.date_deadline != '']
        sorted_tasks_with_deadline = sorted(todo_tasks_with_deadline, key=lambda task: task.date_deadline)
        final_list = sorted_tasks_with_deadline + todo_tasks_without_deadline
        self.parent.display_list = final_list
        self.parent.update_list()

    def set_list_all_tasks(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda task: task.id, reverse=True)
        self.parent.display_list = sorted_tasks
        self.parent.update_list()

    def set_list_todo_by_planned(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        todo_tasks = [task for task in all_tasks if task.status == 'todo']
        todo_tasks_without_date_planned = [task for task in todo_tasks if task.date_planned is None or task.date_planned == '']
        todo_tasks_with_date_planned = [task for task in todo_tasks if task.date_planned is not None and task.date_planned != '']
        sorted_todo_tasks_by_planned = sorted(todo_tasks_with_date_planned, key=lambda task: task.date_planned)
        final_list = sorted_todo_tasks_by_planned + todo_tasks_without_date_planned
        self.parent.display_list = final_list
        self.parent.update_list()

    def set_list_done(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        done_tasks = [task for task in all_tasks if task.status == 'done']
        sorted_done = sorted(done_tasks, key=lambda task: task.date_done, reverse=True)
        self.parent.display_list = sorted_done
        self.parent.update_list()

    def set_list_canceled(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        canceled_tasks = [task for task in all_tasks if task.status == 'canceled']
        sorted_canceled = sorted(canceled_tasks, key=lambda task: task.date_canceled, reverse=True)
        self.parent.display_list = sorted_canceled
        self.parent.update_list()

    def set_list_today(self, *args, **keywords):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        tasks_with_deadline_or_date_planned = [task for task in all_tasks if (task.date_deadline is not None and 
                                                  task.date_deadline != '') or (task.date_planned is not None and 
                                                  task.date_planned != '')]
        today = datetime.today().strftime('%Y-%m-%d') 
        today_tasks = [task for task in tasks_with_deadline_or_date_planned 
            if task.status == 'todo' and ((task.date_deadline <= today and task.date_deadline is not None and task.date_deadline != '')
                       or (task.date_planned <= today and task.date_planned is not None and task.date_planned != ''))]
        today_tasks_sorted = sorted(today_tasks, key=lambda task: task.date_deadline)
        self.parent.display_list = today_tasks_sorted
        self.parent.update_list()

class MyActionController(npyscreen.ActionControllerSimple):
    def create(self):
        self.add_action('^quit', self.quit_application, False)
        self.add_action('^/.*', self.set_search, False)
        self.add_action('^today', self.export_today, False)

    def set_search(self, command_line, control_widget_proxy, live):
        search_term = command_line[1:].strip()
        filtered_list = [task for task in self.parent.display_list if search_term.lower() in task.description.lower() or search_term in task.tags.lower()]
        self.parent.display_list = filtered_list
        self.parent.update_list()

    def quit_application(self, command_line, control_widget_proxy, live):
        self.parent.parentApp.switchForm(None)

    def export_today(self, command_line, control_widget_proxy, live):
        all_tasks = self.parent.parentApp.myDatabase.get_all_tasks()
        tasks_with_deadline_or_date_planned = [task for task in all_tasks if (task.date_deadline is not None and 
                                                  task.date_deadline != '') or (task.date_planned is not None and 
                                                  task.date_planned != '')]
        today = datetime.today().strftime('%Y-%m-%d') 
        today_tasks = [task for task in tasks_with_deadline_or_date_planned 
            if task.status == 'todo' and ((task.date_deadline <= today and task.date_deadline is not None and task.date_deadline != '')
                       or (task.date_planned <= today and task.date_planned is not None and task.date_planned != ''))]
        today_tasks_sorted = sorted(today_tasks, key=lambda task: task.date_deadline)
        with open('today.md', 'a') as my_file:
            for task in today_tasks_sorted:
                my_file.write(f"- {task.description}\n")
        

class RecordListDisplay(npyscreen.FormMuttActive):
    MAIN_WIDGET_CLASS = RecordList
    ACTION_CONTROLLER = MyActionController

    def beforeEditing(self):
        all_tasks = self.parentApp.myDatabase.get_all_tasks()
        tasks_with_deadline_or_date_planned = [task for task in all_tasks if (task.date_deadline is not None and 
                                                  task.date_deadline != '') or (task.date_planned is not None and 
                                                  task.date_planned != '')]
        today = datetime.today().strftime('%Y-%m-%d') 
        today_tasks = [task for task in tasks_with_deadline_or_date_planned 
            if task.status == 'todo' and ((task.date_deadline <= today and task.date_deadline is not None and task.date_deadline != '')
                       or (task.date_planned <= today and task.date_planned is not None and task.date_planned != ''))]
        today_tasks_sorted = sorted(today_tasks, key=lambda task: task.date_deadline)
        self.display_list = today_tasks_sorted
        self.update_list()

    def update_list(self):
        self.wStatus1.value = "VIEWS: a: all tasks | d: todo by deadline | c: todo by planned | t: today | D: done | C: cancelled"
        self.wStatus2.value = "ACTIONS: ctrl-a: add | ctrl-d: delete | ctrl-x: set done | ctrl-q: cancel | enter: update task | command line + quit: quit | command line + /: search" 
        self.wMain.values = self.display_list
        self.wMain.display()


class EditRecord(npyscreen.ActionForm):
    def create(self):
        self.value = None
        self.wgDescription = self.add(npyscreen.TitleText, name = "Description: ")
        self.wgDate_deadline = self.add(npyscreen.TitleText, name = "Deadline: ")
        self.wgDate_planned = self.add(npyscreen.TitleText, name = "Planned date: ")
        self.wgTags = self.add(npyscreen.TitleText, name = "Tags: ")
        self.wgRefs = self.add(npyscreen.TitleText, name = "Refs: ")
        
        self.wgStatus = self.add(npyscreen.TitleFixedText, name = "Status: ")
        self.wgDate_done = self.add(npyscreen.TitleFixedText, name = "Date done: ")
        self.wgDate_canceled = self.add(npyscreen.TitleFixedText, name = "Date canceled: ")
        self.wgInfo = self.add(npyscreen.FixedText)
        self.wgInfo.value = "ctrl-s: save and go back to list | ctrl-q: go back without saving"
        self.add_handlers({"^S": self.save_task_and_go_back,
                           "^Q": self.go_back}) 


    def beforeEditing(self):
        if self.value:
            task = self.parentApp.myDatabase.get_one_task(self.value)
            self.name = f"Task id = {str(task.id)}"
            self.task_id = task.id
            self.wgDescription.value = str(task.description)
            self.wgDate_deadline.value = str(task.date_deadline)
            self.wgDate_planned.value = str(task.date_planned)
            self.wgTags.value = str(task.tags)
            self.wgRefs.value = str(task.refs)
            self.wgStatus.value = str(task.status)
            self.wgDate_done.value = str(task.date_done)
            self.wgDate_canceled.value = str(task.date_canceled)
        else:
            self.name = "New task"
            self.task_id = ''
            self.wgDescription.value = ''
            self.wgDate_deadline.value = ''
            self.wgDate_planned.value = ''
            self.wgTags.value = ''
            self.wgRefs.value = ''
            self.wgStatus.value = ''
            self.wgDate_done.value = ''
            self.wgDate_canceled.value = ''

    def on_ok(self):
        self.save_task_and_go_back(event=None)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

    def save_task_and_go_back(self, event):
        if self.task_id: # we are editing an existing task
            edited_task = Task(id=int(self.task_id), description=self.wgDescription.value, 
                               date_deadline=self.wgDate_deadline.value, date_planned=self.wgDate_planned.value,
                               date_done=self.wgDate_done.value, date_canceled=self.wgDate_canceled.value,
                               status=self.wgStatus.value, tags=self.wgTags.value, refs=self.wgRefs.value)
            self.parentApp.myDatabase.update_task(edited_task)
        else:
            added_task = Task(id=None, description=self.wgDescription.value, 
                               date_deadline=self.wgDate_deadline.value, date_planned=self.wgDate_planned.value,
                               date_done='', date_canceled='', status='todo', tags=self.wgTags.value, refs=self.wgRefs.value)
            self.parentApp.myDatabase.add_task(added_task)
        self.parentApp.switchFormPrevious()

    def go_back(self, event):
        self.parentApp.switchFormPrevious()

class TaskApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = TaskDatabase()
        self.addForm("MAIN", RecordListDisplay)
        self.addForm("EDITRECORDFM", EditRecord)

if __name__ == '__main__':
    # first configure logger
    logging.basicConfig(filename='todo.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p')
    myApp = TaskApplication()
    myApp.run()
