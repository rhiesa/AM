import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QWizard, QWizardPage, QLineEdit, QTextEdit, QFormLayout, QPushButton, QDialog, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView
)
from PyQt5.QtCore import Qt

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
        self.tree.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.SelectedClicked)
        layout.addWidget(self.tree)

        btn_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("Add User")
        self.add_task_btn = QPushButton("Add Task")
        self.add_hazard_btn = QPushButton("Add Hazard")
        self.delete_btn = QPushButton("Delete")
        btn_layout.addWidget(self.add_user_btn)
        btn_layout.addWidget(self.add_task_btn)
        btn_layout.addWidget(self.add_hazard_btn)
        btn_layout.addWidget(self.delete_btn)
        layout.addLayout(btn_layout)

        # Connect buttons to stub methods
        self.add_user_btn.clicked.connect(self.add_user)
        self.add_task_btn.clicked.connect(self.add_task)
        self.add_hazard_btn.clicked.connect(self.add_hazard)
        self.delete_btn.clicked.connect(self.delete_item)

        tab.setLayout(layout)
        return tab

    def add_user(self):
        user_item = QTreeWidgetItem(["New User", "", ""])
        user_item.setFlags(user_item.flags() | Qt.ItemIsEditable)
        self.tree.addTopLevelItem(user_item)
        self.tree.editItem(user_item, 0)

    def add_task(self):
        selected = self.tree.currentItem()
        if selected and selected.parent() is None:
            task_item = QTreeWidgetItem(["", "New Task", ""])
            task_item.setFlags(task_item.flags() | Qt.ItemIsEditable)
            selected.addChild(task_item)
            selected.setExpanded(True)
            self.tree.editItem(task_item, 1)

    def add_hazard(self):
        selected = self.tree.currentItem()
        if selected and selected.parent() and selected.parent().parent() is None:
            hazard_item = QTreeWidgetItem(["", "", "New Hazard"])
            hazard_item.setFlags(hazard_item.flags() | Qt.ItemIsEditable)
            selected.addChild(hazard_item)
            selected.setExpanded(True)
            self.tree.editItem(hazard_item, 2)

    def delete_item(self):
        selected = self.tree.currentItem()
        if selected:
            parent = selected.parent()
            if parent:
                parent.removeChild(selected)
            else:
                idx = self.tree.indexOfTopLevelItem(selected)
                self.tree.takeTopLevelItem(idx)

    def create_assess_risk_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.risk_table = QTableWidget()
        self.risk_table.setColumnCount(10)
        self.risk_table.setHorizontalHeaderLabels([
            "User/Role", "Task", "Hazard", "Severity", "Likelihood", "Initial Risk Level",
            "Controls/Measures", "Residual Severity", "Residual Likelihood", "Residual Risk Level"
        ])
        self.risk_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.risk_table)

        refresh_btn = QPushButton("Refresh from Hazard Tree")
        refresh_btn.clicked.connect(self.refresh_risk_table)
        layout.addWidget(refresh_btn)

        tab.setLayout(layout)
        return tab

    def refresh_risk_table(self):
        self.risk_table.setRowCount(0)
        for i in range(self.tree.topLevelItemCount()):
            user_item = self.tree.topLevelItem(i)
            user_name = user_item.text(0)
            for j in range(user_item.childCount()):
                task_item = user_item.child(j)
                task_name = task_item.text(1)
                for k in range(task_item.childCount()):
                    hazard_item = task_item.child(k)
                    hazard_name = hazard_item.text(2)
                    row = self.risk_table.rowCount()
                    self.risk_table.insertRow(row)
                    self.risk_table.setItem(row, 0, QTableWidgetItem(user_name))
                    self.risk_table.setItem(row, 1, QTableWidgetItem(task_name))
                    self.risk_table.setItem(row, 2, QTableWidgetItem(hazard_name))
                    # Editable severity and likelihood (as combo boxes)
                    severity_cb = QComboBox()
                    severity_cb.addItems(["Low", "Medium", "High"])
                    severity_cb.currentIndexChanged.connect(lambda _, r=row: self.update_initial_risk_level(r))
                    self.risk_table.setCellWidget(row, 3, severity_cb)
                    likelihood_cb = QComboBox()
                    likelihood_cb.addItems(["Rare", "Occasional", "Frequent"])
                    likelihood_cb.currentIndexChanged.connect(lambda _, r=row: self.update_initial_risk_level(r))
                    self.risk_table.setCellWidget(row, 4, likelihood_cb)
                    # Initial Risk Level (to be calculated)
                    self.risk_table.setItem(row, 5, QTableWidgetItem(""))
                    # Controls/Measures (editable)
                    self.risk_table.setItem(row, 6, QTableWidgetItem(""))
                    # Residual Severity/Likelihood (combo boxes)
                    res_sev_cb = QComboBox()
                    res_sev_cb.addItems(["Low", "Medium", "High"])
                    res_sev_cb.currentIndexChanged.connect(lambda _, r=row: self.update_residual_risk_level(r))
                    self.risk_table.setCellWidget(row, 7, res_sev_cb)
                    res_lik_cb = QComboBox()
                    res_lik_cb.addItems(["Rare", "Occasional", "Frequent"])
                    res_lik_cb.currentIndexChanged.connect(lambda _, r=row: self.update_residual_risk_level(r))
                    self.risk_table.setCellWidget(row, 8, res_lik_cb)
                    # Residual Risk Level (to be calculated)
                    self.risk_table.setItem(row, 9, QTableWidgetItem(""))
                    # Set default risk levels
                    self.update_initial_risk_level(row)
                    self.update_residual_risk_level(row)

    def update_initial_risk_level(self, row):
        severity_cb = self.risk_table.cellWidget(row, 3)
        likelihood_cb = self.risk_table.cellWidget(row, 4)
        if not severity_cb or not likelihood_cb:
            return
        severity = severity_cb.currentText()
        likelihood = likelihood_cb.currentText()
        risk = self.calculate_risk_level(severity, likelihood)
        self.risk_table.setItem(row, 5, QTableWidgetItem(risk))

    def update_residual_risk_level(self, row):
        res_sev_cb = self.risk_table.cellWidget(row, 7)
        res_lik_cb = self.risk_table.cellWidget(row, 8)
        if not res_sev_cb or not res_lik_cb:
            return
        severity = res_sev_cb.currentText()
        likelihood = res_lik_cb.currentText()
        risk = self.calculate_risk_level(severity, likelihood)
        self.risk_table.setItem(row, 9, QTableWidgetItem(risk))

    def calculate_risk_level(self, severity, likelihood):
        # Simple risk matrix logic
        if severity == "High" or likelihood == "Frequent":
            return "High"
        elif severity == "Low" and likelihood == "Rare":
            return "Low"
        else:
            return "Medium"

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