import json

class Task:
        
        def __init__(self, name=None, catagory=None):
            if name and catagory:
                 self.__task_name = name
                 self.__task_catagory = catagory
            else:
                self.__task_name = input("Enter a name for your new task: ")
                self.__task_catagory = input("Enter a catagory for your task: ")
            
        def show_tasks(self):
             print(f"""
--------------------------------
Task name: {self.__task_name}
Catagory: {self.__task_catagory}
---------------------------------
""")

        def tasks_to_dict(self):
             return {
                  "Task name" : self.__task_name,
                  "Task catagory" : self.__task_catagory
             }
        
        def update_task_info(self):
            print("""
                What do you want to update?
                1) Task name
                2) Task catagory
                """)
            choose_option = input("Enter a number to chooose an option above: ")
            if choose_option == "1":
                 new_value = input("Enter a new name for your task: ")
                 self.__task_name = new_value
            elif choose_option == "2":
                new_value = input("Enter a new catagory for your task: ")
                self.__task_catagory = new_value
            
        def get_name(self):
             return self.__task_name

        def get_catagory(self):
            return self.__task_catagory

            
class Tasks:
        def __init__(self):
            self.__tasks = []

        def auto_add_task(self):
            self.load_json()
            while True:
                task = Task()
                if any(t.get_name().lower().strip() == task.get_name().lower().strip() and t.get_catagory().lower().strip() == task.get_catagory().lower().strip() for t in self.__tasks):
                    print(f"{task.get_name()} in catagory {task.get_catagory()} already exists!")
                else:
                    self.__tasks.append(task)
                    self.save_json()
                    self.save_task_history(task, action="Added")
                    print(f"Your {task.get_name()} in catagory {task.get_catagory()} been saved!")

                more_tasks = input("Do you want to add more task? (yes/no):")
                if more_tasks.lower() != "yes":
                    break


        def auto_remove_task(self):
            task = input("Enter the name of the task that you wish to remove: ").lower()
            self.load_json()
            for i in self.__tasks:
                 if i.get_name().lower() == task: 
                    self.save_task_history(i, action="Removed")
                    self.__tasks.remove(i)
                    self.save_json()
                    print("Task removed")
                    return
            print("There isn't any task by that name!")                   

        def save_json(self):
             data = [t.tasks_to_dict() for t in self.__tasks]
             with open("tasks.json", "w") as f:
                  json.dump(data, f, indent=4)

        def load_json(self):
            with open("tasks.json", "r") as f:
                data =  json.load(f)
                self.__tasks = []
                for t in data:
                    restored_tasks = Task(t["Task name"], t["Task catagory"])
                    self.__tasks.append(restored_tasks)

        def update_task(self):
            task_name = input("Enter the name of the task that you wish to update: ")
            self.load_json()
            for i in self.__tasks:
                if i.get_name() == task_name:
                    i.update_task_info()
                    self.save_json()
                    self.save_task_history(i, action="Updated")
                    print("Task has updated!")
                    return
            print("Task not found")
        
        def save_task_history(self, task, action=None):
            try:
                with open("history.json", "r") as f:
                    history = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                history = []
            entry = (task.tasks_to_dict())
            entry["action"] = action
            history.append(entry)

            with open("history.json", "w") as f:
                json.dump(history, f, indent=4)
        
        def load_task_history(self):
            try:
                with open("history.json", "r") as f:
                    history = json.load(f)
                    History = []
                    for i in history:
                        restored_history = Task(i["Task name"], i["Task catagory"])
                        action = i.get("action", "Added")
                        History.append((restored_history, action))
                    return History
            except FileNotFoundError:
                    print("No item in your history yet")

        def show_history(self):
            history_list = self.load_task_history()
            for i, action in history_list:
                print(f"----{action.upper()}----")
                i.show_tasks()

        
        def search_task(self):
            task_name = input("Enter the name of the task: ")
            self.load_json()
            for i in self.__tasks:
                if i.get_name().lower().strip() == task_name:
                    print("----------------------")
                    print("You have searched for:")
                    i.show_tasks()
                    return
            print("Task not found!")
                
                  
        def show_tasks(self):
            self.load_json()
            for t in self.__tasks:
                t.show_tasks()


print(""" 
    ---Welcome to your todo-list app---
    1) Add Task
    2) Remove Task
    3) Update task
    4) Tasks History
    5) Search Task
    6) All tasks
    ------------------
    """)

my_tasks = Tasks()
navigation = input("Choose a option by entering a number from 1 to 6: ")

if navigation == "1":
        try:
            my_tasks.auto_add_task()
        except ValueError:
            print("invaild value!")

elif navigation == "2":
    try:
        my_tasks.auto_remove_task()
    except ValueError:
         print("There aren't any tasks")

elif navigation == "3":
    try:
        my_tasks.update_task()
        my_tasks.show_tasks()
    except ValueError:
         print("There aren't any tasks")

elif navigation == "4":
    try:
        my_tasks.show_history()
    except ValueError:
        print("There aren't any tasks")

elif navigation == "5":
    try:
        my_tasks.search_task()
    except ValueError:
        print("There aren't any tasks")

elif navigation == "6":
    try:
        print("---------------")
        print("Your tasks are:")
        my_tasks.show_tasks()
    except ValueError:
        print("There aren't any tasks")

else:
    print("Invalid option")