# Task-Manager-application
This Python project is a command-line Task Manager application developed as part of the Samsung Innovation Campus program. The application allows users to efficiently manage their tasks by providing functionality to create, update, view, and delete tasks.

Features:
Task Management: Create tasks with a title, description, due date, and status (e.g., "incomplete", "completed", "in progress").
Organized Workflow: The application supports both personal and work tasks, with attributes like task category and task priority.
OOP Implementation: Utilizes Object-Oriented Programming concepts such as inheritance and polymorphism.
Error Handling: Implements exception handling .
Data Persistence: Tasks can be stored in a JSON file for persistence.

Classes:
TaskManager: Manages the collection of tasks.
Task: Represents a general task with common attributes.
PersonalTask: Inherits from Task, adds a category attribute.
WorkTask: Inherits from Task, adds a priority attribute.

Usage:
The main function provides a menu-driven interface where users can:
Add a new task
Delete a task
Edit a task
Mark Task as Completed
show work tasks
show personal tasks
show completed tasks
My Rating
search for Task
Recycle Bin
Quit the application