# To-Do List using Streamlit

A simple To-Do List application built with Streamlit, showcasing basic CRUD (Create, Read, Update, Delete) operations. The application allows users to add tasks, view existing tasks, and remove tasks.

## Features

- **Add Task:** Easily add new tasks to the to-do list.
- **View Tasks:** View the list of existing tasks.
- **Remove Task:** Remove a specific task by providing its index.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/downloads/) installed on your machine.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hspsuhas/ToDo-List.git
   ```
2. Navigate to the project directory:

   ```bash
   cd ToDo-List

   ```   

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```   

### Running the app

Execute the following command to run the Streamlit app:

   ```bash
   streamlit run app.py --client.showErrorDetails=false
   ```   

Visit the provided URL (usually http://localhost:8501) in your web browser to interact with the To-Do List application.

## Usage

1. Add Task:

- Enter a task in the text input field.
- Click the "Add Task" button.

2. View Tasks:

- Select "View Tasks" from the sidebar.

3. Remove Task:

- Select "Remove Task" from the sidebar.
- Enter the task index you want to remove.
- Click the "Remove Task" button.

## Deployed Site

https://t0d0-list.streamlit.app/