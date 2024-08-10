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

    def __str__(self):
        s = f"{str(self.id):<4}| {self.description[:50]:<51}| d: {str(self.date_deadline):<11}| p: {str(self.date_planned):<11}| " 
        s = s + f"tags: {str(self.tags)[:40]:<41} | {str(self.status):<12}" 
        s = s + f"| done: {str(self.date_done):<11}| canceled: {str(self.date_canceled):<11} |"

        return s

if __name__ == '__main__':
    my_task = Task(id=None, description="gras maaien", date_deadline='2024-08-07',
                   date_planned='2024-08-07', date_done=None, date_canceled=None, 
                   status='todo', tags=None, refs=None)
    print(my_task)

