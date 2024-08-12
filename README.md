# Introduction

Task Manager for the terminal. With this application you can manage your todo list using the terminal, so without using your mouse. The application uses the npyscreen module in Python and a sqlite3 database.

This is still a work in progress.

# Requirements

A recent version of Python.

The module npyscreen.

# Views - key bindings

In the list mode (a list of tasks is visible) you can use the following keys to view another list:

- a: all tasks 
- d: all tasks with the status 'todo' ordered by deadline (earliest first, then empty date deadline) -
- all tasks with statusc 'todo' order by date planned (earliest first, empty dates at end
- t: today. All tasks due to today. This means tasks that have a deadline on the current date or earlier, or that have a date planned on the current day or earlier.
- D: al tasks with status done, order by date done in reverse order
- C: all tasks with status 'cancelled'

# Actions - key bindings

In the list mode (a list of tasks is visible) you can use the following keys to perform an action on the highlighted tasks 

- ctrl-a: add a new tasks
- ctrl-d: delete the current tasks 
- ctrl-x: set the current task in status 'done'. The date done is automatically filled in. 
- ctrl-q: cancel the current tasks (= set in status 'canceled'). The date canceled is automatically filled in.
- enter: update the current task. A form will appear.
- d: delete the current tasks. In strictly taken not necessary as you can cancel a task.

# Command line commands

The application also has a command line, which you can access (and leave) by pressing <TAB>.

The following commands are active:

- / + Pattern: filter the list on this pattern. The search looks at the fields description and tags.
- quit: quit the appliation.
- today: appends today's tasks to the file today.md in the current directory, so that you can plan your day in detail in a text file.

# Edit a task

When you add a new tasks or edit a task, you can save that task in two ways:

- press the OK button.
- press ctrl-s

You can cancel the editing in two ways:

- press the cancel button
- press ctrl-q

