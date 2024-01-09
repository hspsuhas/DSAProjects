import streamlit as st

# st.set_option('client.caching', False)

class ToDoList:
    def __init__(self):
        self.tasks = []

def add_task(todo_list, task):
    todo_list.tasks.append(task)
    st.success(f'Task "{task}" added.')

@st.cache(allow_output_mutation=True)
def get_todo_list():
    return ToDoList()

def view_tasks(todo_list):
    if not todo_list.tasks:
        st.info("No tasks available.")
    else:
        st.write("#### Tasks:")
        for i, task in enumerate(todo_list.tasks, 1):
            st.write(f'{i}. {task}')

def remove_task(todo_list, task_index):
    if 1 <= task_index <= len(todo_list.tasks):
        removed_task = todo_list.tasks.pop(task_index - 1)
        st.success(f'Task "{removed_task}" removed.')
    else:
        st.error("Invalid task index.")

def main():
    st.title("To-Do List using Array")

    todo_list = get_todo_list()

    option = st.sidebar.selectbox("#### Select an option:", ["Add Task", "View Tasks", "Remove Task"])

    if option == "Add Task":
        task = st.text_input("#### Enter the Task:", key="add_task_input")  # Unique key
        if st.button("Add Task"):
            add_task(todo_list, task)

    elif option == "View Tasks":
        view_tasks(todo_list)

    elif option == "Remove Task":
        task_index = st.number_input("#### Enter the task index to remove:", min_value=1, max_value=len(todo_list.tasks), step=1, key="remove_task_input")  # Unique key
        if st.button("Remove Task"):
            remove_task(todo_list, int(task_index))

if __name__ == "__main__":
    main()
