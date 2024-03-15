from models import Task, User, session
from datetime import datetime

def create_task(current_user, data):
    if not data or 'name' not in data or 'due_date' not in data or 'priority' not in data:
        return "Missing required data"

    task = Task(name=data['name'], due_date=data['due_date'], priority=data['priority'], user = current_user, access_token = current_user.access_token)
    session.add(task)
    session.commit()
    return "Task has been created"

def update_task(current_user, task_id, data):
    task = session.get(Task, task_id)
    if not task:
        return "Task not found"
    if task.user_id != current_user.id:
        return "You are not authorized to update this task"

    if not data:
        return "Missing request data"
    
    if 'name' in data:
        task.name = data['name']
    if 'due_date' in data:
        task.due_date = data['due_date']
    if 'priority' in data:
        task.priority = data['priority']

    session.commit()
    return "Task has been updated"

def delete_task(current_user, task_id):
    task = session.get(Task, task_id)
    if not task:
        return "Task not found"
    if task.user_id != current_user.id:
        return "You are not authorized to delete this task"

    session.delete(task)
    session.commit()
    return 'Task has been deleted successfully'

def read_task(current_user, task_id):
    print(task_id)
    task = session.get(Task, task_id)
    if not task:
        return "Task not found"
    if task.user_id != current_user.id:
        return "You are not authorized to view this task"

    return {'id': task.id, 'name': task.name, 'due_date': task.due_date.strftime('%Y-%m-%d %H:%M:%S'), 'priority': task.priority}

# def main():
#     try:
#         print("\nInside Routes.py\n")
#         connection = session.connection()
#         print("PostgreSQL session is started")

#         curr_user = session.get(User, 1)
#         print(curr_user.email)

        # # test read
        # print(read_task(curr_user,1)) # worked

        # # test update
        # print(update_task(curr_user, 2, {'name':"Test Task 2 updtd"})) # worked

        # # test create
        # print(create_task(curr_user, {'name':"New Task",'due_date':datetime(2024, 8, 12), "priority" : 10})) #worked

        # # test delete
        # print(delete_task(curr_user, 5))
        
#     except Exception as e:
#         print(f"The error '{e}' occurred")

#     finally:
#         session.close()
#         print("PostgreSQL session is closed\n")


# if __name__ == "__main__":
#     main()