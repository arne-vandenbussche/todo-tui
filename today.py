from time import strftime
from database import TaskDatabase
from rich.console import Console
from rich.table import Table
from datetime import date

today = date.today().strftime('%A %d %B %Y')
my_tasks_db = TaskDatabase()
my_tasks_for_today = my_tasks_db.tasks_for_today()
table = Table(title=f"Taken voor vandaag {today}") 
table.add_column("Beschrijving", justify="left")
table.add_column("Deadline", justify="center")
table.add_column("Gepland", justify= "center")

for task in my_tasks_for_today:
    table.add_row(task.description, task.date_deadline, task.date_planned)    

console = Console()
console.print(table)
