import os
import sys
import json
from PyQt5.QtWidgets import(
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Get the full path of the current script file
script_path = __file__

# Get the directory of the script
current_directory = os.path.dirname(script_path)
class ToDo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List App")
        self.setFixedSize(400,450)
        self.setWindowIcon(QIcon(os.path.join(current_directory,"list.png")))
        self.todo_file = os.path.join(current_directory,"tasks.json")
        self.tasks = []
        
        self.create_ui()
        self.load_tasks()
        
    def create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        input_layout = QHBoxLayout()
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter new task...")
        self.task_input.returnPressed.connect(self.add_task)
        
        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task)
        
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_button)
        main_layout.addLayout(input_layout)
        
        self.task_list = QListWidget()
        self.task_list.itemChanged.connect(self.update_task_status)
        self.task_list.itemDoubleClicked.connect(self.edit_task)
        main_layout.addWidget(self.task_list)
        
        button_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_task)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_tasks)
        
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(clear_btn)
        #button_layout.addWidget(save_btn)
        main_layout.addLayout(button_layout)
        
    def add_task(self):
        task_text = self.task_input.text().strip()
        
        if task_text:
            self.add_task_item(task_text, done=False)
            self.task_input.clear()
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Warning","Please enter a task before adding.")
    def add_task_item(self, text, done=False):
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        item.setCheckState(Qt.Checked if done else Qt.Unchecked)
        self.task_list.addItem(item)
        
    def update_task_status(self,item):
        self.save_tasks()
        
    def edit_task(self, item):
        pass
    
    def delete_task(self):
        selected = self.task_list.currentRow()
        
        if selected >= 0:
            self.task_list.takeItem(selected)
            self.save_tasks()
        else:
            QMessageBox.warning(self, "Warning", "Select a task to delete.")
    
    def clear_all(self):
        confirm = QMessageBox.question(
            self, "Confirm", "Clear all tasks?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.task_list.clear()
            self.save_tasks()
    
    def save_tasks(self):
        data = []
        
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            data.append({
                "text": item.text(),
                "done": item.checkState() == Qt.Checked
            })
        
        with open(self.todo_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_tasks(self):
        try:
            with open(self.todo_file, 'r') as f:
                self.tasks = json.load(f)
                for task in self.tasks:
                    self.add_task_item(task["text"], task["done"])
                    
        except FileNotFoundError:
            
            self.tasks = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDo()
    window.show()
    sys.exit(app.exec_())