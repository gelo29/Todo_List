import sys
import json
from PyQt5.QtWidgets import(
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QMessageBox
)

from PyQt5.QtCore import Qt

class ToDo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📝 To-Do List App")
        self.setFixedSize(400,400)
        
        self.todo_file = "tasks.json"
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
        button_layout.addWidget(save_btn)
        
        main_layout.addLayout(button_layout)
    def add_task(self):
        task_text = self.task_input.text().strip()
        
        if task_text:
            self.task_list.addItem(task_text)
            self.task_input.clear()
            self.tasks.append(task_text)
        else:
            QMessageBox.warning(self, "Warning","Please enter a task before adding.")
    
    def delete_task(self):
        selected = self.task_list.currentRow()
        
        if selected >= 0:
            item = self.task_list.takeItem(selected)
            self.tasks.remove(item.text())
        else:
            QMessageBox.warning(self, "Warning", "Select a task to delete.")
    
    def clear_all(self):
        confirm = QMessageBox.question(
            self, "Confirm", "Clear all tasks?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.task_list.clear()
            self.tasks.clear()
    
    def save_tasks(self):
        with open(self.todo_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)
        QMessageBox.information(self,"Saved", "Tasks saved successfully!")
    
    def load_tasks(self):
        try:
            with open(self.todo_file, 'r') as f:
                self.tasks = json.load(f)
                self.task_list.addItems(self.tasks)
        except FileNotFoundError:
            self.tasks = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDo()
    window.show()
    sys.exit(app.exec_())