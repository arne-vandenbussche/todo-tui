from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: Optional[int]
    description: str
    date_deadline: Optional[str]
    date_planned: Optional[str]
    date_done: Optional[str]
    date_canceled: Optional[str]
    status: Optional[str]
    tags: Optional[str]
    refs: Optional[str]

if __name__ == '__main__':
    my_task = Task(id=None, description="gras maaien", date_deadline='2024-08-07',
                   date_planned='2024-08-07', date_done=None, date_canceled=None, 
                   status='todo', tags=None, refs=None)
    print(my_task)

