import os
import sys
import json
from PyQt5.QtWidgets import(
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem, QMessageBox,
    QProgressBar
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
        self.setFixedSize(420,500)
        self.setWindowIcon(QIcon(os.path.join(current_directory,"list.png")))
        self.todo_file = os.path.join(current_directory,"tasks.json")
        self.tasks = []
        self.current_filter = "All"
        
        self.create_ui()
        self.load_tasks()
        self.update_progress()
        
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
        
        #--- Filter ----
        filter_layout = QHBoxLayout()
        self.all_btn = QPushButton("All")
        self.active_btn = QPushButton("Active")
        self.completed_btn = QPushButton("Completed")
        
        for btn in [self.all_btn, self.active_btn, self.completed_btn]:
            btn.setCheckable(True)
            btn.clicked.connect(self.filter_tasks)
        
        self.all_btn.setChecked(True)
        
        filter_layout.addWidget(self.all_btn)
        filter_layout.addWidget(self.active_btn)
        filter_layout.addWidget(self.completed_btn)
        main_layout.addLayout(filter_layout)
        
        #---- Task List ----
        self.task_list = QListWidget()
        self.task_list.itemChanged.connect(self.on_task_change)
        main_layout.addWidget(self.task_list)
        
        #---- Progress Bar ----
        self.progress = QProgressBar()
        self.progress.setFormat("Completed: %p%")
        main_layout.addWidget(self.progress)
        
        #---- Control Buttons ----

        button_layout = QHBoxLayout()
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_task)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
    
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(clear_btn)
        main_layout.addLayout(button_layout)
        
    def add_task(self):
        task_text = self.task_input.text().strip()
        
        if task_text:
            self.tasks.append({"text": task_text, "done": False})
            self.task_input.clear()
            self.save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning","Please enter a task before adding.")
            
    def on_task_change(self, item):
        index = self.task_list.row(item)
        visible_tasks = self.get_filtered_tasks()
        real_task = visible_tasks[index]
        print(real_task)
        for task in self.tasks:
            if task["text"] == real_task["text"]:
                task["text"] = item.text()
                task["done"] = item.checkState() == Qt.Checked
                break
        self.save_tasks()
        self.update_progress()
        
    def delete_task(self):
        selected = self.task_list.currentRow()
        if selected >= 0:
            visible_tasks = self.get_filtered_tasks()
            task_to_remove = visible_tasks[selected]
            self.tasks.remove(task_to_remove)
            self.save_tasks()
            self.update_task_list()
        else:
            QMessageBox.warning(self, "Warning", "Select a task to delete.")
                            
    def clear_all(self):
        confirm = QMessageBox.question(
            self, "Confirm", "Clear all tasks?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.tasks = []
            self.save_tasks()
            self.update_task_list()
            self.update_progress()
            
    def filter_tasks(self):
        sender = self.sender()
        self.all_btn.setChecked(False)
        self.active_btn.setChecked(False)
        self.completed_btn.setChecked(False)
        sender.setChecked(True)
        self.current_filter = sender.text()
        self.update_task_list()
    
    def get_filtered_tasks(self):
        if self.current_filter == "Active":
            return [t for t in self.tasks if not t["done"]]
        elif self.current_filter == "Completed":
            return [t for t in self.tasks if t["done"]]
        
        return self.tasks

    def update_task_list(self):
        self.task_list.clear()
        for task in self.get_filtered_tasks():
            item = QListWidgetItem(task["text"])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
            item.setCheckState(Qt.Checked if task["done"] else Qt.Unchecked)
            self.task_list.addItem(item)
        self.update_progress()
    
    def update_progress(self):
        if not self.tasks:
            self.progress.setValue(0)
            return
        done = len([t for t in self.tasks if t["done"]])
        percent = int((done / len(self.tasks)) * 100)
        self.progress.setValue(percent)
        
    def save_tasks(self):
        with open(self.todo_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    def load_tasks(self):
        try:
            with open(self.todo_file, 'r') as f:
                self.tasks = json.load(f)
                self.update_task_list()
                    
        except FileNotFoundError:
    
            self.tasks = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDo()
    window.show()
    sys.exit(app.exec_())