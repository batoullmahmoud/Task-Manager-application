import json
from datetime import datetime

# read file , load data
tasks_file = open("tasks.json",'r')
tasks_list = json.load(tasks_file)
tasks_file.close()

Users_info = open("data.json", 'r')
info = json.load(Users_info)
Users_info.close()

class Task:
    def __init__(self,id, title, description, dueDate, status,type):
        self.id = id
        self.title = title
        self.description = description
        self.dueDate = datetime.strptime(dueDate, '%d/%m/%Y')
        self.status = status
        self.type = type

    def get_dict(self):
        dict_obj = {
            "ID": self.id,
            "title": self.title,
            "description": self.description,
            "dueDate": self.dueDate.strftime('%d/%m/%Y') if self.dueDate else None,
            "type": self.type,
            "status": self.status,
        }
        return dict_obj

# inheritance  & polymorphism : inheritance , override
class PersonalTask(Task):
    def __init__(self,id ,title, description, dueDate, status,type, category):
        super().__init__(id,title, description, dueDate, status,type)
        self.category = category

    # override
    def get_dict(self):
        dict_obj = super().get_dict()
        dict_obj["category"] = self.category
        return dict_obj

    def showType(self):
        return "personal"

class WorkTask(Task):
    def __init__(self,id, title, description, dueDate, status,type, taskPriority):
        super().__init__(id,title, description, dueDate, status,type)
        self.taskPriority = taskPriority

    def get_dict(self):
        dict_obj = super().get_dict()
        dict_obj["Task Priority"] = self.taskPriority
        return dict_obj

    def showType(self):
        return "work"

class TaskManager():
    def __init__(self,id,Tasks=[]):
        self.id = id
        self.Tasks = Tasks
        self.lost_task_counter = 0
        self.lost_tasks = []
        self.deleted_tasks = []

    def createTask(self,obj):
        task_data = obj.get_dict()
        self.Tasks.append(task_data)
        print("Task added successfully!")

    def deleteTask(self, in_title):
        for task in self.Tasks:
            if self.id == task["ID"] and in_title == task["title"] and task not in self.deleted_tasks:
                if task["type"] == WorkTask.showType(task):  # type == work
                    if "Task Priority" in task:
                        deleted_priority = int(task.get("Task Priority", 0))

                        # Check if there are other tasks with the same priority
                        same_priority_count = sum(1 for taskk in self.Tasks if taskk.get("Task Priority") == deleted_priority and taskk != task)  # taskk => not deleted
                        # Only decrease priority if no other task has the same priority
                        if same_priority_count == 0:
                            self.decrease_work_task_priority(deleted_priority)
                self.deleted_tasks.append(task)
                self.Tasks.remove(task)
                print("Task successfully moved to the recycle bin!")
                return
        print("Task not found")

    def updateSpecific(self, in_title, edit_val, update_input):
        for task in self.Tasks:
            if task["ID"] == self.id and in_title == task["title"] and task not in self.lost_tasks:
                if edit_val == "Task Priority" and task["type"] != WorkTask.showType(task):
                    print(task["title"], "is not a work task!")
                    return
                elif edit_val == "category" and task["type"] != PersonalTask.showType(task):
                    print(task["title"], "is not a personal task!")
                    return

                task[edit_val] = update_input
                print(f"Task's {edit_val} is updated successfully!")
                return

        print("Task is not found or You don't have permission to update, or You already lost.")


    def calculate_countdown(self, task):
        now = datetime.now()
        if isinstance(task, dict):
            due_date = datetime.strptime(task["dueDate"], '%d/%m/%Y')
        else:  # object (work , personal)
            due_date = task.dueDate
        countdown = due_date - now
        return countdown

    def User_Rate(self):
        self.lost_task_counter = 0
        self.lost_tasks = []

        for task in self.Tasks:
            if task["ID"] == self.id and task["status"] != "completed":
                countdown = self.calculate_countdown(task)
                if task not in self.lost_tasks and countdown.total_seconds() <= 0:
                    self.lost_tasks.append(task)
                    self.lost_task_counter += 1

        if self.lost_task_counter > 0 and  self.lost_task_counter < 5:
            print("You have", self.lost_task_counter, "lost tasks:")
            for lost_task in self.lost_tasks:
                print(lost_task["title"], lost_task["dueDate"])
        elif self.lost_task_counter >= 5:
            print("Your rate is really bad. You have", self.lost_task_counter, "lost tasks")
            for lost_task in self.lost_tasks:
                print(lost_task["title"], lost_task["dueDate"])
        else:
            print("You are doing well, good job! 😊")

    def search_task_by_title(self, task_title):
        for task in self.Tasks:
            if task["ID"] == self.id and task["title"] == task_title:
                print("Title:", task["title"])
                print("Description:", task["description"])
                print("Status:", task["status"])
                print("Due Date:", task["dueDate"])
                return

        print("You don't have permissions on task or Task with title", task_title, " not found.")



    def mark_as_completed(self, task_title):
        for task in self.Tasks:
            if task["ID"] == self.id and task["title"] == task_title and task not in self.lost_tasks:
                if task["type"] == WorkTask.showType(task):
                    task["status"] = 'completed'
                    if "Task Priority" in task:
                        task_priority = int(task["Task Priority"])
                        self.decrease_work_task_priority(task_priority)
                    print("Work Task marked as completed")
                    return
                else:
                    task["status"] = 'completed'
                    print("Personal Task marked as completed")
                    return

        print("Task not found or you don't have permission to mark it as completed, or You already lost.")

    def display_work_tasks(self):
        user_tasks = [task for task in self.Tasks if
                      task["ID"] == self.id and task["type"] == WorkTask.showType(task) and task[
                          "status"] != "completed"]
        user_work_tasks = []

        for task in user_tasks:
            if "Task Priority" in task:  # Check if "Task Priority" exists in the task
                task["Task Priority"] = int(task["Task Priority"])  # Convert "Task Priority" to integer

            user_work_tasks.append(task)

        sorted_work_tasks = sorted(user_work_tasks,
                                   key=lambda task: task.get("Task Priority", 0))  # Sort by "Task Priority"

        if sorted_work_tasks:
            for task in sorted_work_tasks:
                countdown = self.calculate_countdown(task)
                if countdown.total_seconds() > 0:
                    print(task["title"], "\nPriority:", task.get("Task Priority", None), "\nDate:",
                          task['dueDate'], "\nStatus:", task["status"],
                          "\nDescription:", task["description"])
                else:
                    self.lost_tasks.append(task)
        else:
            print("There aren't any tasks to show")

    def display_personal_tasks(self):
        user_tasks = [task for task in self.Tasks if
                      task["ID"] == self.id and task["type"] == PersonalTask.showType(task) and task[
                          "status"] != "completed"]
        user_personal_tasks = []

        for task in user_tasks:
            user_personal_tasks.append(task)

        sorted_personal_tasks = sorted(user_personal_tasks, key=lambda task: task["dueDate"])
        if sorted_personal_tasks:
            for task in sorted_personal_tasks:
                countdown = self.calculate_countdown(task)
                if countdown.total_seconds() > 0:
                    print(task["title"], "\nDate:", task['dueDate'], "\nCategory:",
                          task["category"], "\nStatus:", task["status"],
                          "\nDescription:", task["description"], "\n")
                else:
                    self.lost_tasks.append(task)

        else:
            print("there aren't any tasks to show")

    def display_completed_tasks(self):
        completed_tasks = [task for task in self.Tasks if task["ID"] == self.id and task["status"] == "completed"]

        if not completed_tasks:
            print("No completed tasks found.")
            return

        for task in completed_tasks:
            if task["type"] == "work":
                print("Work task:\n", "Priority:", task["Task Priority"], "\n", task["title"], "\nDate:",
                      task['dueDate'], "\nStatus:", task["status"],
                      "\nDescription:", task["description"])
            elif task["type"] == "personal":
                print("Personal task:\n", task["title"], "\nDate:", task['dueDate'], "\nCategory:", task["category"],
                      "\nStatus:", task["status"],
                      "\nDescription:", task["description"], "\n")

    def decrease_work_task_priority(self, deleted_priority):
        deleted_priority = int(deleted_priority)
        for task in self.Tasks:
            if "Task Priority" in task and task["type"] == "work":
                task_priority = int(task["Task Priority"])
                if task_priority > deleted_priority:
                    task["Task Priority"] = task_priority - 1

    def Recycle_Bin(self):
        choice = None
        titlee = None

        for task in self.deleted_tasks:
            if task["ID"] == self.id:
                print(task["title"])

        if self.deleted_tasks:
            titlee = input("Enter title of task you want to see or return: ")
            choice = input("Return task/see details: ").lower()
        else:
            print("Nothing in Recycle Bin")
            return

        for task in self.deleted_tasks:
            if task["title"] == titlee and task["ID"] == self.id:
                if choice == 'return':
                    self.Tasks.append(task)
                    self.deleted_tasks.remove(task)
                    print("Task returned successfully!")
                elif choice == 'see':
                    print(task["title"], "\n", task["description"], "\n", task["dueDate"], "\n", task["status"], "\n",
                          task["type"])
                return

        print("Task is not found or You don't have permission to update, or You already lost.")

    def getReminder(self):
        count = 0
        for task in self.Tasks:
            if task["ID"] == self.id:
                if task["status"] != "completed" and self.calculate_countdown(task).total_seconds() <= 86400 and self.calculate_countdown(task).total_seconds()>0: #day
                    count += 1
        print(f"you have {count} remaining tasks to complete.")
        if count != 0:
            show = input("Do yo  want to show it? [y/n]")
            for task in self.Tasks:
                if task["ID"] == self.id and task["status"] != "completed" and self.calculate_countdown(task).total_seconds() <= 86400 and self.calculate_countdown(
                        task).total_seconds() > 0:
                    if show == 'y':
                        print("[", task["title"], "]--->", task["dueDate"])
                    else:
                        print("OK")


def Register():
    latest_id = max([user["Id"] for user in info]) if info else 0
    ID = latest_id + 1

    name = str(input("Name: "))
    while not name:
        print("Please enter Your name")
        name = str(input("Name: "))

    password = str(input("Password: "))
    while not password:
        print("Please enter your password")
        password = str(input("Password: "))

    email = input("E-mail: ")
    while "@gmail.com" not in email:
        print("invalid input, Please enter a valid email with (@gmail.com)")
        email = input("E-mail: ")

    data = {
        "Id": ID,
        "Name": name,
        "Password": password,
        "E-mail": email
    }

    info.append(data)
    print("you Registered successfully, your ID is:", ID)


def login():
    try:
        idd = int(input("Enter your  ID: "))
        password = str(input("Enter your password: "))
    except ValueError:
        print("Invalid input.")
    except IndexError:
        print("this account doesn't exist.")

    for user in info:
        if user["Id"] == idd and user["Password"] == password:
            print("Welcome back ", user["Name"])
            print("_______________ Welcome back ", user["Name"], "_______________")
            return True,idd

    print("incorrect data, try again")  # user not in list
    return False,None


def main():

    while True:

        print("If you already have an account, please enter 'login'")
        print("If you don't have an account, please enter 'register'")
        print("to Exit , enter exit. ")

        option = input("Enter your Choice: ")

        if option.lower() == "login":
            print("_______________ Welcome to Login page _______________")

            login_succ, idd = login()
            if login_succ:
                task_manager = TaskManager(idd,tasks_list)

                rem = input("Do you want to see remaining tasks? [y/n]").lower()
                if rem == 'y':
                    task_manager.getReminder()

                option = -1
                while option != 11:
                    print("\nTask Manager Menu:")
                    print("1. Add Task")
                    print("2. Delete Task")
                    print("3. Edit a task ")
                    print("4. Mark Task as Completed")
                    print("5. show work tasks")
                    print("6. show personal tasks")
                    print("7. show completed tasks")
                    print("8. My Rating")
                    print("9. search for Task")
                    print("10.Recycle Bin")
                    print("11. Exit")
                    try:
                        option = int(input("Enter your choice : "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                    if option == 1:
                        # add task
                        title = input("Enter task title: ")
                        description = input("Enter task description: ")
                        due_date = input("Enter due date in format (dd/mm/yyyy): ")
                        status = input("Enter task status (completed,incomplete, in progress): ")
                        type = input("Enter task type (work,personal): ").lower()

                        if type == "personal":
                            category = input("Enter task category (family,sport,..): ")
                            personal_obj = PersonalTask(idd,title, description, due_date, status ,type,category)
                            task_manager.createTask(personal_obj)
                        elif type == "work":
                            priority = input("Enter the task priority  : ")
                            work_obj = WorkTask(idd,title, description, due_date, status ,type, priority)
                            task_manager.createTask(work_obj)
                        else:
                            print("Invalid choice. Please enter personal or work.")

                    elif option == 2:
                        # delete
                        t_title = input("Enter Task title : ")
                        task_manager.deleteTask(t_title)

                    elif option == 3:
                        # edit
                        edit_choice = None
                        while(True):
                            print("\nThe Update Menu:")
                            print("[1] update Title")
                            print("[2] update description")
                            print("[3] update Due Date")
                            print("[4] update status")
                            print("[5] update Task Priority")
                            print("[6] update category")
                            print("[7] close")
                            try:
                                edit_choice = int(input("choose an operation : "))
                            except ValueError:
                                print("Invalid input. Please enter a number.")
                            except UnboundLocalError:
                                print("UnboundLocalError: 'edit_choice' was referenced before assignment.")
                            if edit_choice == 7:
                                break
                            else:
                                input_title = input("Enter the title of the task which you want to update : ")
                                if edit_choice == 1:
                                    update_in = input("Enter the new title : ")
                                    task_manager.updateSpecific(input_title, "title", update_in)
                                elif edit_choice == 2:
                                    update_in = input("Enter the new description : ")
                                    task_manager.updateSpecific(input_title, "description", update_in)
                                elif edit_choice == 3:
                                    update_in = input("Enter the new Due Date : ")
                                    task_manager.updateSpecific(input_title, "dueDate", update_in)
                                elif edit_choice == 4:
                                    update_in = input("Enter the new status (completed,incomplete, in progress): ")
                                    task_manager.updateSpecific(input_title, "status", update_in)
                                elif edit_choice == 5:
                                    update_in = input("Enter the new Task Priority: ")
                                    task_manager.updateSpecific(input_title, "Task Priority", update_in)
                                elif edit_choice == 6:
                                    update_in = input("Enter the new category: ")
                                    task_manager.updateSpecific(input_title, "category", update_in)
                                else:
                                    print("invalid choice! please try again.")


                    elif option == 4:
                        title = input("Enter task title: ")
                        task_manager.mark_as_completed(title)

                    elif option == 5:
                        print("Work Tasks:")
                        task_manager.display_work_tasks()

                    elif option == 6:
                        print("Personal Tasks:")
                        task_manager.display_personal_tasks()
                    elif option == 7:
                        task_manager.display_completed_tasks()
                    elif option == 8:
                        task_manager.User_Rate()
                    elif option == 9:
                        title = input("Enter task title: ")
                        task_manager.search_task_by_title(title)

                    elif option == 10:
                        task_manager.Recycle_Bin()
                    elif option == 11:
                        break
                    else:
                        print("Invalid choice. Please try again.")

        elif option.lower() == "register":
            print("_______________ Welcome to Sign Up page _______________")
            Register()

        elif option.lower() == "exit":
            break
        else:
            print("invalid choice. Please try again.")

    # write , update file
    tasks_file = open("tasks.json", "w")
    json.dump(tasks_list, tasks_file, indent=4)
    tasks_file.close()

    Users_info = open("data.json", 'w')
    json.dump(info, Users_info, indent=4)
    Users_info.close()


if __name__ == "__main__":
   main()
