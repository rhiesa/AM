import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QWizard, QWizardPage, QLineEdit, QTextEdit, QFormLayout, QPushButton, QDialog, QTreeWidget, QTreeWidgetItem, QHBoxLayout
)

class ProjectSetupWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Risk Assessment Project Setup Wizard")
        self.addPage(self.create_project_info_page())
        self.addPage(self.create_company_info_page())
        # Add more pages as needed for template, limits, etc.

    def create_project_info_page(self):
        page = QWizardPage()
        page.setTitle("Project Information")
        layout = QFormLayout()
        self.project_name = QLineEdit()
        self.project_desc = QTextEdit()
        layout.addRow("Assessment Name:", self.project_name)
        layout.addRow("Assessment Description:", self.project_desc)
        page.setLayout(layout)
        return page

    def create_company_info_page(self):
        page = QWizardPage()
        page.setTitle("Company and Machine Information")
        layout = QFormLayout()
        self.company_name = QLineEdit()
        self.facility_location = QLineEdit()
        self.machine_id = QLineEdit()
        self.lifecycle_stage = QLineEdit()
        layout.addRow("Company Name:", self.company_name)
        layout.addRow("Facility Location:", self.facility_location)
        layout.addRow("Machine/Product ID:", self.machine_id)
        layout.addRow("Lifecycle Stage:", self.lifecycle_stage)
        page.setLayout(layout)
        return page

class MainWindow(QMainWindow):
    def __init__(self, project_info=None):
        super().__init__()
        self.setWindowTitle("Risk Assessment Tool")
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_identify_hazards_tab(), "Identify Hazards")
        self.tabs.addTab(self.create_assess_risk_tab(), "Assess and Reduce Risk")
        self.tabs.addTab(self.create_control_system_tab(), "Control System Assessment")
        self.tabs.addTab(self.create_alternative_method_tab(), "Alternative Method")
        self.setCentralWidget(self.tabs)

    def create_identify_hazards_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["User/Role", "Task", "Hazard"])
        layout.addWidget(self.tree)

        btn_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("Add User")
        self.add_task_btn = QPushButton("Add Task")
        self.add_hazard_btn = QPushButton("Add Hazard")
        btn_layout.addWidget(self.add_user_btn)
        btn_layout.addWidget(self.add_task_btn)
        btn_layout.addWidget(self.add_hazard_btn)
        layout.addLayout(btn_layout)

        # Connect buttons to stub methods
        self.add_user_btn.clicked.connect(self.add_user)
        self.add_task_btn.clicked.connect(self.add_task)
        self.add_hazard_btn.clicked.connect(self.add_hazard)

        tab.setLayout(layout)
        return tab

    def add_user(self):
        user_item = QTreeWidgetItem(["New User", "", ""])
        self.tree.addTopLevelItem(user_item)

    def add_task(self):
        selected = self.tree.currentItem()
        if selected and selected.parent() is None:
            task_item = QTreeWidgetItem(["", "New Task", ""])
            selected.addChild(task_item)
            selected.setExpanded(True)

    def add_hazard(self):
        selected = self.tree.currentItem()
        if selected and selected.parent() and selected.parent().parent() is None:
            hazard_item = QTreeWidgetItem(["", "", "New Hazard"])
            selected.addChild(hazard_item)
            selected.setExpanded(True)

    def create_assess_risk_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("(Risk assessment table will go here)"))
        tab.setLayout(layout)
        return tab

    def create_control_system_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("(Control system assessment form will go here)"))
        tab.setLayout(layout)
        return tab

    def create_alternative_method_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("(Alternative method checklist will go here)"))
        tab.setLayout(layout)
        return tab

def main():
    app = QApplication(sys.argv)
    wizard = ProjectSetupWizard()
    if wizard.exec_() == QDialog.Accepted:
        # Collect project info from wizard
        project_info = {
            'name': wizard.project_name.text(),
            'description': wizard.project_desc.toPlainText(),
            'company': wizard.company_name.text(),
            'location': wizard.facility_location.text(),
            'machine_id': wizard.machine_id.text(),
            'lifecycle_stage': wizard.lifecycle_stage.text(),
        }
        window = MainWindow(project_info)
        window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main() 