import sys
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QWizard, QWizardPage, QLineEdit, QTextEdit, QFormLayout, QPushButton, QDialog, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QHeaderView, QInputDialog, QMessageBox, QFileDialog, QDialogButtonBox, QListWidget, QListWidgetItem, QCheckBox
)
from PyQt5.QtCore import Qt

class StartupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Risk Assessment Tool")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Welcome to Risk Assessment Tool")
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin: 40px; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Buttons
        new_btn = QPushButton("Create New Assessment")
        new_btn.setStyleSheet("font-size: 24px; padding: 20px; margin: 20px; background-color: #4CAF50; color: white; border: none; border-radius: 10px;")
        new_btn.clicked.connect(self.create_new)
        
        load_btn = QPushButton("Load Existing Assessment")
        load_btn.setStyleSheet("font-size: 24px; padding: 20px; margin: 20px; background-color: #2196F3; color: white; border: none; border-radius: 10px;")
        load_btn.clicked.connect(self.load_existing)
        
        layout.addWidget(new_btn)
        layout.addWidget(load_btn)
        
        self.setLayout(layout)
        
        self.choice = None
    
    def create_new(self):
        self.choice = "new"
        self.accept()
    
    def load_existing(self):
        self.choice = "load"
        self.accept()

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
        self.project_info = project_info or {}
        self.current_file = None
        self.setWindowTitle("Risk Assessment Tool")
        
        # Make window much larger
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add save/load buttons at the top with larger text
        file_layout = QHBoxLayout()
        save_btn = QPushButton("Save Assessment")
        save_as_btn = QPushButton("Save As...")
        load_btn = QPushButton("Load Assessment")
        
        # Style the buttons with larger text
        button_style = "font-size: 24px; padding: 20px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;"
        save_btn.setStyleSheet(button_style)
        save_as_btn.setStyleSheet(button_style)
        load_btn.setStyleSheet(button_style)
        
        save_btn.clicked.connect(self.save_assessment)
        save_as_btn.clicked.connect(self.save_assessment_as)
        load_btn.clicked.connect(self.load_assessment)
        
        file_layout.addWidget(save_btn)
        file_layout.addWidget(save_as_btn)
        file_layout.addWidget(load_btn)
        file_layout.addStretch()
        layout.addLayout(file_layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("font-size: 24px; QTabBar::tab { font-size: 24px; padding: 20px; margin: 8px; }")
        self.tab_widget.addTab(self.create_identify_hazards_tab(), "Identify Hazards")
        self.tab_widget.addTab(self.create_assess_risk_tab(), "Assess and Reduce Risk")
        self.tab_widget.addTab(self.create_control_system_tab(), "Control System Assessment")
        self.tab_widget.addTab(self.create_alternative_method_tab(), "Alternative Method")
        
        layout.addWidget(self.tab_widget)

    def create_identify_hazards_tab(self):
        tab = QWidget()
        layout = QHBoxLayout()
        
        # Left pane: User/Task Tree
        left_pane = QVBoxLayout()
        left_label = QLabel("Users/Roles and Tasks:")
        left_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        left_pane.addWidget(left_label)
        
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["User/Role", "Task", "Hazard"])
        self.tree.setEditTriggers(QTreeWidget.DoubleClicked | QTreeWidget.SelectedClicked)
        self.tree.setStyleSheet("font-size: 24px; QHeaderView::section { font-size: 24px; font-weight: bold; padding: 15px; }")
        left_pane.addWidget(self.tree)
        
        # Tree buttons
        tree_btn_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("Add User")
        self.add_task_btn = QPushButton("Add Task")
        self.delete_btn = QPushButton("Delete")
        
        button_style = "font-size: 24px; padding: 20px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;"
        self.add_user_btn.setStyleSheet(button_style)
        self.add_task_btn.setStyleSheet(button_style)
        self.delete_btn.setStyleSheet(button_style)
        
        tree_btn_layout.addWidget(self.add_user_btn)
        tree_btn_layout.addWidget(self.add_task_btn)
        tree_btn_layout.addWidget(self.delete_btn)
        left_pane.addLayout(tree_btn_layout)
        
        self.add_user_btn.clicked.connect(self.add_user)
        self.add_task_btn.clicked.connect(self.add_task)
        self.delete_btn.clicked.connect(self.delete_item)
        
        # Middle pane: Hazard Categories
        middle_pane = QVBoxLayout()
        middle_label = QLabel("Hazard Categories:")
        middle_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        middle_pane.addWidget(middle_label)
        
        self.category_list = QListWidget()
        self.category_list.setStyleSheet("font-size: 24px; padding: 10px;")
        self.populate_hazard_categories()
        middle_pane.addWidget(self.category_list)
        
        # Category buttons
        cat_btn_layout = QHBoxLayout()
        add_cat_btn = QPushButton("Add Category")
        edit_cat_btn = QPushButton("Edit Category")
        delete_cat_btn = QPushButton("Delete Category")
        
        add_cat_btn.setStyleSheet(button_style)
        edit_cat_btn.setStyleSheet(button_style)
        delete_cat_btn.setStyleSheet(button_style)
        
        cat_btn_layout.addWidget(add_cat_btn)
        cat_btn_layout.addWidget(edit_cat_btn)
        cat_btn_layout.addWidget(delete_cat_btn)
        middle_pane.addLayout(cat_btn_layout)
        
        # Right pane: Hazards
        right_pane = QVBoxLayout()
        right_label = QLabel("Hazards:")
        right_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        right_pane.addWidget(right_label)
        
        self.hazards_table = QTableWidget()
        self.hazards_table.setColumnCount(3)
        self.hazards_table.setHorizontalHeaderLabels(["Hazard", "Cause/Failure", "Selected"])
        self.hazards_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hazards_table.setStyleSheet("font-size: 24px; QHeaderView::section { font-size: 24px; font-weight: bold; padding: 15px; }")
        right_pane.addWidget(self.hazards_table)
        
        # Hazards buttons
        haz_btn_layout = QHBoxLayout()
        add_haz_btn = QPushButton("Add Hazard")
        edit_haz_btn = QPushButton("Edit Hazard")
        delete_haz_btn = QPushButton("Delete Hazard")
        add_to_task_btn = QPushButton("Add Selected to Task")
        add_all_to_task_btn = QPushButton("Add All Selected to Task")
        clear_selections_btn = QPushButton("Clear Selections")
        
        add_haz_btn.setStyleSheet(button_style)
        edit_haz_btn.setStyleSheet(button_style)
        delete_haz_btn.setStyleSheet(button_style)
        add_to_task_btn.setStyleSheet(button_style)
        add_all_to_task_btn.setStyleSheet(button_style)
        clear_selections_btn.setStyleSheet(button_style)
        
        haz_btn_layout.addWidget(add_haz_btn)
        haz_btn_layout.addWidget(edit_haz_btn)
        haz_btn_layout.addWidget(delete_haz_btn)
        haz_btn_layout.addWidget(add_to_task_btn)
        haz_btn_layout.addWidget(add_all_to_task_btn)
        haz_btn_layout.addWidget(clear_selections_btn)
        right_pane.addLayout(haz_btn_layout)
        
        # Selection summary
        self.selection_summary = QLabel("No hazards selected")
        self.selection_summary.setStyleSheet("font-size: 20px; font-weight: bold; color: #0066cc; margin: 10px; padding: 10px; background-color: #f0f8ff; border: 1px solid #ccc; border-radius: 5px;")
        right_pane.addWidget(self.selection_summary)
        
        # Connect signals
        self.category_list.currentItemChanged.connect(self.on_category_selected)
        add_to_task_btn.clicked.connect(self.add_selected_hazards_to_task)
        add_all_to_task_btn.clicked.connect(self.add_all_selected_hazards_to_task)
        clear_selections_btn.clicked.connect(self.clear_hazard_selections)
        add_haz_btn.clicked.connect(self.add_custom_hazard)
        edit_haz_btn.clicked.connect(self.edit_custom_hazard)
        delete_haz_btn.clicked.connect(self.delete_custom_hazard)
        
        # Initialize selection memory
        self.hazard_selections = {}  # Store selections per category
        self.current_category = None
        
        # Add panes to main layout
        left_widget = QWidget()
        left_widget.setLayout(left_pane)
        left_widget.setMinimumWidth(400)
        
        middle_widget = QWidget()
        middle_widget.setLayout(middle_pane)
        middle_widget.setMinimumWidth(300)
        
        right_widget = QWidget()
        right_widget.setLayout(right_pane)
        right_widget.setMinimumWidth(500)
        
        layout.addWidget(left_widget)
        layout.addWidget(middle_widget)
        layout.addWidget(right_widget)
        
        tab.setLayout(layout)
        return tab

    def populate_hazard_categories(self):
        """Populate the hazard categories with predefined industrial categories"""
        categories = [
            "All Categories",
            "Mechanical",
            "Electrical/Electronic", 
            "Slips/Trips/Falls",
            "Ergonomics/Human Factors",
            "Fire and Explosions",
            "Heat/Temperature",
            "Noise/Vibration",
            "Ingress/Egress",
            "Material Handling",
            "Environmental/Industrial Hygiene",
            "Ventilation/Confined Space",
            "Chemical",
            "Fluid/Pressure",
            "Wastes (Lean)",
            "Other"
        ]
        
        for category in categories:
            item = QListWidgetItem(category)
            self.category_list.addItem(item)

    def get_hazards_for_category(self, category):
        """Return predefined hazards for each category"""
        hazards = {
            "Mechanical": [
                ("Crushing", "Moving parts, heavy equipment, presses"),
                ("Cutting/Severing", "Sharp edges, blades, shears, saws"),
                ("Drawing-in/Trapping/Entanglement", "Rotating parts, conveyors, gears"),
                ("Pinch Point", "Between moving and stationary parts"),
                ("Unexpected Start", "Equipment startup, stored energy release"),
                ("Break Up During Operation", "Flying debris, component failure"),
                ("Machine Instability", "Overturning, tipping, falling equipment"),
                ("Impact", "Dropped parts, falling objects, collisions"),
                ("Abrasion", "Grinding, sanding, surface contact"),
                ("Puncture", "Sharp objects, pointed tools, fasteners")
            ],
            "Electrical/Electronic": [
                ("Electric Shock", "Exposed wiring, faulty equipment, wet conditions"),
                ("Arc Flash", "Electrical faults, short circuits, switching operations"),
                ("Electromagnetic Interference", "Radio frequency, magnetic fields"),
                ("Static Electricity", "Friction, dry conditions, synthetic materials"),
                ("Electrical Fire", "Overheating, short circuits, overload"),
                ("Battery Explosion", "Lithium batteries, overcharging, damage"),
                ("Control System Failure", "Software bugs, hardware failure, power loss"),
                ("Electrocution", "High voltage contact, ground faults"),
                ("Electrical Burns", "Arc flash, contact burns, thermal effects")
            ],
            "Slips/Trips/Falls": [
                ("Slips", "Wet floors, oil, grease, loose materials"),
                ("Trips", "Uneven surfaces, cables, tools, debris"),
                ("Falls from Height", "Ladders, platforms, elevated work areas"),
                ("Falls on Same Level", "Slippery surfaces, obstacles, poor lighting"),
                ("Falls Through Openings", "Floor openings, unguarded edges"),
                ("Stairway Falls", "Wet steps, poor lighting, missing handrails"),
                ("Ladder Falls", "Unstable footing, overreaching, improper use")
            ],
            "Ergonomics/Human Factors": [
                ("Repetitive Motion", "Assembly work, typing, tool operation"),
                ("Awkward Postures", "Bending, reaching, twisting, kneeling"),
                ("Heavy Lifting", "Manual material handling, equipment moving"),
                ("Forceful Exertions", "Pushing, pulling, gripping, pressing"),
                ("Vibration", "Hand tools, equipment operation, vehicle operation"),
                ("Eye Strain", "Poor lighting, screen work, detailed tasks"),
                ("Mental Fatigue", "Long shifts, complex tasks, decision making"),
                ("Stress", "High workload, time pressure, responsibility")
            ],
            "Fire and Explosions": [
                ("Fire", "Hot work, electrical faults, flammable materials"),
                ("Explosion", "Dust, gases, pressure vessels, chemical reactions"),
                ("Flash Fire", "Flammable vapors, ignition sources"),
                ("Thermal Burns", "Hot surfaces, steam, molten metal"),
                ("Smoke Inhalation", "Fire, welding fumes, chemical vapors"),
                ("Structural Collapse", "Fire damage, explosion damage")
            ],
            "Heat/Temperature": [
                ("Heat Stress", "Hot environments, heavy work, protective clothing"),
                ("Thermal Burns", "Hot surfaces, steam, molten metal, welding"),
                ("Cold Stress", "Cold environments, refrigeration, outdoor work"),
                ("Frostbite", "Extreme cold, wet conditions, poor protection"),
                ("Heat Exhaustion", "High temperatures, physical exertion"),
                ("Heat Stroke", "Severe heat stress, dehydration")
            ],
            "Noise/Vibration": [
                ("Hearing Loss", "Loud equipment, impact noise, continuous exposure"),
                ("Hand-Arm Vibration", "Power tools, equipment operation"),
                ("Whole Body Vibration", "Vehicle operation, machinery operation"),
                ("Tinnitus", "Loud noise exposure, acoustic trauma"),
                ("Communication Interference", "Background noise, hearing protection")
            ],
            "Ingress/Egress": [
                ("Entrapment", "Confined spaces, equipment access, emergency exits"),
                ("Access Difficulties", "Poor lighting, narrow passages, obstacles"),
                ("Emergency Egress", "Blocked exits, poor signage, panic"),
                ("Vehicle Access", "Loading docks, traffic, blind spots"),
                ("Equipment Access", "Maintenance access, operator stations")
            ],
            "Material Handling": [
                ("Manual Handling", "Lifting, carrying, pushing, pulling"),
                ("Mechanical Handling", "Cranes, forklifts, conveyors, hoists"),
                ("Storage Hazards", "Stacking, racking, falling materials"),
                ("Transportation", "Vehicle movement, loading, unloading"),
                ("Packaging", "Sharp edges, heavy packages, unstable loads")
            ],
            "Environmental/Industrial Hygiene": [
                ("Dust Exposure", "Grinding, sanding, material handling"),
                ("Fume Exposure", "Welding, painting, chemical processes"),
                ("Vapor Exposure", "Solvents, cleaning agents, process chemicals"),
                ("Mist Exposure", "Coolants, lubricants, process fluids"),
                ("Gas Exposure", "Compressed gases, process gases, exhaust"),
                ("Biological Hazards", "Mold, bacteria, organic materials")
            ],
            "Ventilation/Confined Space": [
                ("Oxygen Deficiency", "Confined spaces, gas displacement"),
                ("Toxic Atmosphere", "Chemical vapors, process gases, decomposition"),
                ("Flammable Atmosphere", "Gas accumulation, vapor buildup"),
                ("Engulfment", "Loose materials, flowing substances"),
                ("Entrapment", "Narrow passages, equipment, structural elements")
            ],
            "Chemical": [
                ("Chemical Burns", "Acids, bases, corrosive materials"),
                ("Chemical Inhalation", "Vapors, gases, dusts, mists"),
                ("Chemical Ingestion", "Contamination, poor hygiene"),
                ("Chemical Injection", "High pressure, sharp objects"),
                ("Allergic Reactions", "Sensitizers, allergens, irritants"),
                ("Carcinogenic Exposure", "Known carcinogens, long-term exposure")
            ],
            "Fluid/Pressure": [
                ("High Pressure", "Hydraulic systems, pneumatic systems, pressure vessels"),
                ("Fluid Injection", "High pressure fluids, hydraulic systems"),
                ("Pressure Vessel Failure", "Overpressure, corrosion, fatigue"),
                ("Fluid Leaks", "Hydraulic oil, coolant, process fluids"),
                ("Vacuum Hazards", "Vacuum systems, implosion, collapse")
            ],
            "Wastes (Lean)": [
                ("Waste Accumulation", "Excess inventory, scrap, unused materials"),
                ("Storage Issues", "Poor organization, space constraints"),
                ("Disposal Hazards", "Waste handling, disposal processes"),
                ("Recycling Hazards", "Sorting, processing, material handling")
            ],
            "Other": [
                ("Weather Conditions", "Rain, snow, wind, extreme temperatures"),
                ("Lighting Issues", "Poor lighting, glare, shadows"),
                ("Housekeeping", "Poor organization, clutter, debris"),
                ("Maintenance", "Equipment failure, repair activities"),
                ("Training", "Inadequate training, skill gaps, inexperience")
            ]
        }
        
        if category == "All Categories":
            all_hazards = []
            for cat_hazards in hazards.values():
                all_hazards.extend(cat_hazards)
            return all_hazards
        else:
            return hazards.get(category, [])

    def on_category_selected(self, current, previous):
        """Handle category selection and populate hazards table with remembered selections"""
        if current is None:
            return
            
        # Save current selections before switching
        if self.current_category:
            self.save_current_selections()
            
        category = current.text()
        self.current_category = category
        hazards = self.get_hazards_for_category(category)
        
        self.hazards_table.setRowCount(0)
        for hazard_name, cause in hazards:
            row = self.hazards_table.rowCount()
            self.hazards_table.insertRow(row)
            
            # Hazard name
            self.hazards_table.setItem(row, 0, QTableWidgetItem(hazard_name))
            
            # Cause/Failure (editable)
            cause_item = QTableWidgetItem(cause)
            self.hazards_table.setItem(row, 1, cause_item)
            
            # Selected checkbox with remembered state
            checkbox = QCheckBox()
            checkbox.setStyleSheet("font-size: 24px;")
            
            # Restore selection if it exists
            if category in self.hazard_selections:
                if hazard_name in self.hazard_selections[category]:
                    checkbox.setChecked(True)
            
            # Connect checkbox to update summary
            checkbox.stateChanged.connect(self.update_selection_summary)
            
            self.hazards_table.setCellWidget(row, 2, checkbox)
        
        # Update summary after populating
        self.update_selection_summary()

    def update_selection_summary(self):
        """Update the selection summary display"""
        total_selected = 0
        category_breakdown = []
        
        for category, selected_hazards in self.hazard_selections.items():
            if category != "All Categories" and selected_hazards:
                count = len(selected_hazards)
                total_selected += count
                category_breakdown.append(f"{category}: {count}")
        
        if total_selected == 0:
            self.selection_summary.setText("No hazards selected")
        else:
            summary_text = f"Total Selected: {total_selected}"
            if category_breakdown:
                summary_text += f" ({', '.join(category_breakdown)})"
            self.selection_summary.setText(summary_text)

    def save_current_selections(self):
        """Save current checkbox selections for the current category"""
        if not self.current_category:
            return
            
        if self.current_category not in self.hazard_selections:
            self.hazard_selections[self.current_category] = set()
            
        # Clear previous selections for this category
        self.hazard_selections[self.current_category].clear()
        
        # Save current selections
        for row in range(self.hazards_table.rowCount()):
            checkbox = self.hazards_table.cellWidget(row, 2)
            if checkbox and checkbox.isChecked():
                hazard_name = self.hazards_table.item(row, 0).text()
                self.hazard_selections[self.current_category].add(hazard_name)
        
        # Update summary
        self.update_selection_summary()

    def clear_hazard_selections(self):
        """Clear all checkbox selections in the current category"""
        for row in range(self.hazards_table.rowCount()):
            checkbox = self.hazards_table.cellWidget(row, 2)
            if checkbox:
                checkbox.setChecked(False)
        
        # Clear from memory
        if self.current_category in self.hazard_selections:
            self.hazard_selections[self.current_category].clear()
        
        # Update summary
        self.update_selection_summary()

    def add_selected_hazards_to_task(self):
        """Add selected hazards to the currently selected task with visual feedback"""
        current_item = self.tree.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a task first.")
            return
            
        # Find the task item (if we're on a hazard, go up to task)
        task_item = current_item
        if task_item.parent() is None:  # It's a user
            QMessageBox.warning(self, "Warning", "Please select a task, not a user.")
            return
            
        task_name = task_item.text(1)
        
        # Get selected hazards from current category
        selected_hazards = []
        for row in range(self.hazards_table.rowCount()):
            checkbox = self.hazards_table.cellWidget(row, 2)
            if checkbox and checkbox.isChecked():
                hazard_name = self.hazards_table.item(row, 0).text()
                cause = self.hazards_table.item(row, 1).text()
                selected_hazards.append((hazard_name, cause))
        
        if not selected_hazards:
            QMessageBox.warning(self, "Warning", "Please select at least one hazard.")
            return
            
        # Add hazards to the task with visual feedback
        added_count = 0
        for hazard_name, cause in selected_hazards:
            # Check if hazard already exists for this task
            hazard_exists = False
            for i in range(task_item.childCount()):
                existing_hazard = task_item.child(i)
                if existing_hazard.text(2) == f"{hazard_name} - {cause}":
                    hazard_exists = True
                    break
            
            if not hazard_exists:
                hazard_item = QTreeWidgetItem(task_item)
                hazard_item.setText(2, f"{hazard_name} - {cause}")
                added_count += 1
        
        # Clear selections after adding
        for row in range(self.hazards_table.rowCount()):
            checkbox = self.hazards_table.cellWidget(row, 2)
            if checkbox:
                checkbox.setChecked(False)
        
        # Clear from memory
        if self.current_category in self.hazard_selections:
            self.hazard_selections[self.current_category].clear()
                
        if added_count > 0:
            QMessageBox.information(self, "Success", f"Added {added_count} new hazards to task: {task_name}")
        else:
            QMessageBox.information(self, "Info", "All selected hazards were already added to this task.")

    def add_all_selected_hazards_to_task(self):
        """Add all selected hazards from all categories to the currently selected task"""
        current_item = self.tree.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "Please select a task first.")
            return
            
        # Find the task item
        task_item = current_item
        if task_item.parent() is None:  # It's a user
            QMessageBox.warning(self, "Warning", "Please select a task, not a user.")
            return
            
        task_name = task_item.text(1)
        
        # Collect all selected hazards from all categories
        all_selected_hazards = []
        for category, selected_hazards in self.hazard_selections.items():
            if category != "All Categories":
                category_hazards = self.get_hazards_for_category(category)
                for hazard_name, cause in category_hazards:
                    if hazard_name in selected_hazards:
                        all_selected_hazards.append((hazard_name, cause))
        
        if not all_selected_hazards:
            QMessageBox.warning(self, "Warning", "No hazards selected from any category.")
            return
            
        # Add all selected hazards to the task
        added_count = 0
        for hazard_name, cause in all_selected_hazards:
            # Check if hazard already exists for this task
            hazard_exists = False
            for i in range(task_item.childCount()):
                existing_hazard = task_item.child(i)
                if existing_hazard.text(2) == f"{hazard_name} - {cause}":
                    hazard_exists = True
                    break
            
            if not hazard_exists:
                hazard_item = QTreeWidgetItem(task_item)
                hazard_item.setText(2, f"{hazard_name} - {cause}")
                added_count += 1
        
        # Clear all selections
        self.hazard_selections.clear()
        self.clear_hazard_selections()
                
        QMessageBox.information(self, "Success", f"Added {added_count} hazards from all categories to task: {task_name}")

    def add_user(self):
        user_item = QTreeWidgetItem(["New User", "", ""])
        user_item.setFlags(user_item.flags() | Qt.ItemIsEditable)
        self.tree.addTopLevelItem(user_item)
        self.tree.setCurrentItem(user_item)
        self.tree.editItem(user_item, 0)

    def add_task(self):
        current_item = self.tree.currentItem()
        if current_item and current_item.parent() is None:  # User item
            # Add task to the current user
            task_item = QTreeWidgetItem(current_item)
            task_item.setText(1, "New Task")
            task_item.setFlags(task_item.flags() | Qt.ItemIsEditable)
            self.tree.setCurrentItem(task_item)
            self.tree.editItem(task_item, 1)
        elif current_item and current_item.parent() and current_item.parent().parent() is None:  # Task item
            # If we're on a task, add another task to the same user
            user_item = current_item.parent()
            task_item = QTreeWidgetItem(user_item)
            task_item.setText(1, "New Task")
            task_item.setFlags(task_item.flags() | Qt.ItemIsEditable)
            self.tree.setCurrentItem(task_item)
            self.tree.editItem(task_item, 1)
        elif current_item and current_item.parent() and current_item.parent().parent() and current_item.parent().parent().parent() is None:  # Hazard item
            # If we're on a hazard, add another task to the same user
            user_item = current_item.parent().parent()
            task_item = QTreeWidgetItem(user_item)
            task_item.setText(1, "New Task")
            task_item.setFlags(task_item.flags() | Qt.ItemIsEditable)
            self.tree.setCurrentItem(task_item)
            self.tree.editItem(task_item, 1)
        else:
            # If no user selected, create a new user first
            self.add_user()

    def add_hazard(self):
        current_item = self.tree.currentItem()
        if current_item and current_item.parent() and current_item.parent().parent() is None:  # Task item
            # Add hazard to the current task
            hazard_item = QTreeWidgetItem(current_item)
            hazard_item.setText(2, "New Hazard")
            hazard_item.setFlags(hazard_item.flags() | Qt.ItemIsEditable)
            self.tree.setCurrentItem(hazard_item)
            self.tree.editItem(hazard_item, 2)
        elif current_item and current_item.parent() is None:  # User item
            # Create task first, then hazard
            self.add_task()
        elif current_item and current_item.parent() and current_item.parent().parent() and current_item.parent().parent().parent() is None:  # Hazard item
            # If we're on a hazard, add another hazard to the same task
            task_item = current_item.parent()
            hazard_item = QTreeWidgetItem(task_item)
            hazard_item.setText(2, "New Hazard")
            hazard_item.setFlags(hazard_item.flags() | Qt.ItemIsEditable)
            self.tree.setCurrentItem(hazard_item)
            self.tree.editItem(hazard_item, 2)
        else:
            # If no task selected, create a new user and task first
            self.add_user()

    def delete_item(self):
        current_item = self.tree.currentItem()
        if current_item:
            if current_item.parent() is None:  # User item
                self.tree.takeTopLevelItem(self.tree.indexOfTopLevelItem(current_item))
            else:
                parent = current_item.parent()
                parent.removeChild(current_item)

    def create_assess_risk_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Risk Assessment Table
        self.risk_table = QTableWidget()
        self.risk_table.setColumnCount(13)
        self.risk_table.setHorizontalHeaderLabels([
            "Item ID", "User/Role", "Task", "Hazard Category", "Hazard", "Cause/Failure Mode",
            "Initial Severity", "Initial Probability", "Initial Risk Level",
            "Risk Reduction Measures", "Residual Severity", "Residual Probability", "Residual Risk Level"
        ])
        self.risk_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.risk_table.setStyleSheet("font-size: 24px; QHeaderView::section { font-size: 24px; font-weight: bold; padding: 15px; }")
        layout.addWidget(self.risk_table)

        # Risk Reduction Methods Section
        methods_group = QWidget()
        methods_layout = QVBoxLayout()
        
        methods_label = QLabel("What risk reduction method(s) have been or will be applied?")
        methods_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        methods_layout.addWidget(methods_label)
        
        methods_text_layout = QHBoxLayout()
        self.risk_reduction_text = QTextEdit()
        self.risk_reduction_text.setMaximumHeight(100)
        self.risk_reduction_text.setStyleSheet("font-size: 20px; padding: 10px;")
        methods_text_layout.addWidget(self.risk_reduction_text)
        
        methods_btn = QPushButton("Edit Risk Reduction Methods...")
        methods_btn.setStyleSheet("font-size: 20px; padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")
        methods_btn.clicked.connect(self.show_risk_reduction_methods)
        methods_text_layout.addWidget(methods_btn)
        
        transfer_btn = QPushButton("Transfer to Selected Row")
        transfer_btn.setStyleSheet("font-size: 20px; padding: 15px; margin: 10px; background-color: #4CAF50; color: white; border: 2px solid #45a049; border-radius: 10px;")
        transfer_btn.clicked.connect(self.transfer_risk_reduction_methods)
        methods_text_layout.addWidget(transfer_btn)
        
        methods_layout.addLayout(methods_text_layout)
        methods_group.setLayout(methods_layout)
        layout.addWidget(methods_group)

        # Bottom controls
        bottom_layout = QHBoxLayout()
        
        # Risk Matrix Section
        matrix_group = QWidget()
        matrix_layout = QVBoxLayout()
        
        matrix_label = QLabel("Risk Scoring System:")
        matrix_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        matrix_layout.addWidget(matrix_label)
        
        # Create risk matrix display
        matrix_table = QTableWidget()
        matrix_table.setRowCount(4)
        matrix_table.setColumnCount(4)
        matrix_table.setHorizontalHeaderLabels(["", "Very Likely", "Likely", "Unlikely", "Remote"])
        matrix_table.setVerticalHeaderLabels(["Catastrophic", "Serious", "Moderate", "Minor"])
        matrix_table.setMaximumHeight(200)
        matrix_table.setStyleSheet("font-size: 20px; QHeaderView::section { font-size: 20px; font-weight: bold; padding: 10px; }")
        
        # Color the matrix cells
        matrix_colors = [
            ["High", "High", "High", "Medium"],
            ["High", "High", "Medium", "Low"],
            ["High", "Medium", "Low", "Low"],
            ["Medium", "Low", "Low", "Low"]
        ]
        
        for row in range(4):
            for col in range(4):
                item = QTableWidgetItem(matrix_colors[row][col])
                item.setTextAlignment(Qt.AlignCenter)
                
                # Color coding
                if matrix_colors[row][col] == "High":
                    item.setBackground(Qt.red)
                    item.setForeground(Qt.white)
                elif matrix_colors[row][col] == "Medium":
                    item.setBackground(Qt.yellow)
                elif matrix_colors[row][col] == "Low":
                    item.setBackground(Qt.green)
                    item.setForeground(Qt.white)
                
                matrix_table.setItem(row, col, item)
        
        matrix_layout.addWidget(matrix_table)
        matrix_group.setLayout(matrix_layout)
        bottom_layout.addWidget(matrix_group)
        
        # Navigation and action buttons
        controls_group = QWidget()
        controls_layout = QVBoxLayout()
        
        view_risk_btn = QPushButton("View Risk Scoring System")
        view_risk_btn.setStyleSheet("font-size: 20px; padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")
        controls_layout.addWidget(view_risk_btn)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        prev_col_btn = QPushButton("←")
        prev_row_btn = QPushButton("↑")
        next_col_btn = QPushButton("→")
        next_row_btn = QPushButton("↓")
        
        nav_style = "font-size: 20px; padding: 15px; margin: 5px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;"
        prev_col_btn.setStyleSheet(nav_style)
        prev_row_btn.setStyleSheet(nav_style)
        next_col_btn.setStyleSheet(nav_style)
        next_row_btn.setStyleSheet(nav_style)
        
        nav_layout.addWidget(prev_col_btn)
        nav_layout.addWidget(prev_row_btn)
        nav_layout.addWidget(next_col_btn)
        nav_layout.addWidget(next_row_btn)
        controls_layout.addLayout(nav_layout)
        
        help_btn = QPushButton("Help")
        help_btn.setStyleSheet("font-size: 20px; padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")
        controls_layout.addWidget(help_btn)
        
        controls_group.setLayout(controls_layout)
        bottom_layout.addWidget(controls_group)
        
        layout.addLayout(bottom_layout)

        refresh_btn = QPushButton("Refresh from Hazard Tree")
        refresh_btn.setStyleSheet("font-size: 24px; padding: 20px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;")
        refresh_btn.clicked.connect(self.refresh_risk_table)
        layout.addWidget(refresh_btn)

        tab.setLayout(layout)
        return tab

    def show_risk_reduction_methods(self):
        """Show hierarchical risk reduction methods dialog"""
        dialog = RiskReductionMethodsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_methods = dialog.get_selected_methods()
            self.risk_reduction_text.setPlainText(", ".join(selected_methods))

    def transfer_risk_reduction_methods(self):
        """Transfer selected risk reduction methods to the currently selected row"""
        current_row = self.risk_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a row in the risk assessment table first.")
            return
        
        methods_text = self.risk_reduction_text.toPlainText()
        if not methods_text.strip():
            QMessageBox.warning(self, "Warning", "Please select some risk reduction methods first.")
            return
        
        # Transfer the methods to the "Risk Reduction Measures" column (column 9)
        self.risk_table.setItem(current_row, 9, QTableWidgetItem(methods_text))
        
        QMessageBox.information(self, "Success", f"Risk reduction methods transferred to row {current_row + 1}")
        
        # Clear the text area for next use
        self.risk_reduction_text.clear()

    def refresh_risk_table(self):
        self.risk_table.setRowCount(0)
        item_id = 1
        
        for i in range(self.tree.topLevelItemCount()):
            user_item = self.tree.topLevelItem(i)
            user_name = user_item.text(0)
            for j in range(user_item.childCount()):
                task_item = user_item.child(j)
                task_name = task_item.text(1)
                for k in range(task_item.childCount()):
                    hazard_item = task_item.child(k)
                    hazard_text = hazard_item.text(2)
                    
                    # Parse hazard text to extract category and cause
                    if " - " in hazard_text:
                        hazard_name, cause = hazard_text.split(" - ", 1)
                        # Try to determine category from hazard name
                        hazard_category = self.determine_hazard_category(hazard_name)
                    else:
                        hazard_name = hazard_text
                        cause = ""
                        hazard_category = "Other"
                    
                    row = self.risk_table.rowCount()
                    self.risk_table.insertRow(row)
                    
                    # Item ID
                    self.risk_table.setItem(row, 0, QTableWidgetItem(f"{item_id}"))
                    
                    # User/Role
                    self.risk_table.setItem(row, 1, QTableWidgetItem(user_name))
                    
                    # Task
                    self.risk_table.setItem(row, 2, QTableWidgetItem(task_name))
                    
                    # Hazard Category
                    self.risk_table.setItem(row, 3, QTableWidgetItem(hazard_category))
                    
                    # Hazard
                    self.risk_table.setItem(row, 4, QTableWidgetItem(hazard_name))
                    
                    # Cause/Failure Mode
                    self.risk_table.setItem(row, 5, QTableWidgetItem(cause))
                    
                    # Initial Severity (combo box)
                    init_sev_cb = QComboBox()
                    init_sev_cb.addItems(["Catastrophic", "Serious", "Moderate", "Minor"])
                    init_sev_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                    init_sev_cb.currentIndexChanged.connect(lambda _, r=row: self.update_initial_risk_level(r))
                    self.risk_table.setCellWidget(row, 6, init_sev_cb)
                    
                    # Initial Probability (combo box)
                    init_prob_cb = QComboBox()
                    init_prob_cb.addItems(["Very Likely", "Likely", "Unlikely", "Remote"])
                    init_prob_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                    init_prob_cb.currentIndexChanged.connect(lambda _, r=row: self.update_initial_risk_level(r))
                    self.risk_table.setCellWidget(row, 7, init_prob_cb)
                    
                    # Initial Risk Level (calculated)
                    self.risk_table.setItem(row, 8, QTableWidgetItem(""))
                    
                    # Risk Reduction Measures (editable)
                    self.risk_table.setItem(row, 9, QTableWidgetItem(""))
                    
                    # Residual Severity (combo box)
                    res_sev_cb = QComboBox()
                    res_sev_cb.addItems(["Catastrophic", "Serious", "Moderate", "Minor"])
                    res_sev_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                    res_sev_cb.currentIndexChanged.connect(lambda _, r=row: self.update_residual_risk_level(r))
                    self.risk_table.setCellWidget(row, 10, res_sev_cb)
                    
                    # Residual Probability (combo box)
                    res_prob_cb = QComboBox()
                    res_prob_cb.addItems(["Very Likely", "Likely", "Unlikely", "Remote"])
                    res_prob_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                    res_prob_cb.currentIndexChanged.connect(lambda _, r=row: self.update_residual_risk_level(r))
                    self.risk_table.setCellWidget(row, 11, res_prob_cb)
                    
                    # Residual Risk Level (calculated)
                    self.risk_table.setItem(row, 12, QTableWidgetItem(""))
                    
                    # Set default risk levels
                    self.update_initial_risk_level(row)
                    self.update_residual_risk_level(row)
                    
                    item_id += 1

    def determine_hazard_category(self, hazard_name):
        """Determine hazard category based on hazard name"""
        hazard_name_lower = hazard_name.lower()
        
        if any(word in hazard_name_lower for word in ["crushing", "cutting", "drawing", "pinch", "impact", "abrasion", "puncture"]):
            return "Mechanical"
        elif any(word in hazard_name_lower for word in ["electric", "arc", "static", "battery", "control"]):
            return "Electrical/Electronic"
        elif any(word in hazard_name_lower for word in ["slip", "trip", "fall"]):
            return "Slips/Trips/Falls"
        elif any(word in hazard_name_lower for word in ["repetitive", "awkward", "lifting", "vibration", "strain"]):
            return "Ergonomics/Human Factors"
        elif any(word in hazard_name_lower for word in ["fire", "explosion", "thermal", "smoke"]):
            return "Fire and Explosions"
        elif any(word in hazard_name_lower for word in ["heat", "cold", "temperature", "frostbite"]):
            return "Heat/Temperature"
        elif any(word in hazard_name_lower for word in ["noise", "hearing", "tinnitus"]):
            return "Noise/Vibration"
        elif any(word in hazard_name_lower for word in ["ingress", "egress", "entrapment", "access"]):
            return "Ingress/Egress"
        elif any(word in hazard_name_lower for word in ["handling", "storage", "transport", "packaging"]):
            return "Material Handling"
        elif any(word in hazard_name_lower for word in ["dust", "fume", "vapor", "gas", "biological"]):
            return "Environmental/Industrial Hygiene"
        elif any(word in hazard_name_lower for word in ["ventilation", "confined", "oxygen", "toxic", "flammable"]):
            return "Ventilation/Confined Space"
        elif any(word in hazard_name_lower for word in ["chemical", "acid", "base", "corrosive", "allergic"]):
            return "Chemical"
        elif any(word in hazard_name_lower for word in ["pressure", "fluid", "hydraulic", "pneumatic", "vacuum"]):
            return "Fluid/Pressure"
        elif any(word in hazard_name_lower for word in ["waste", "disposal", "recycling"]):
            return "Wastes (Lean)"
        else:
            return "Other"

    def update_initial_risk_level(self, row):
        severity_cb = self.risk_table.cellWidget(row, 6)
        probability_cb = self.risk_table.cellWidget(row, 7)
        if not severity_cb or not probability_cb:
            return
        
        severity = severity_cb.currentText()
        probability = probability_cb.currentText()
        risk = self.calculate_risk_level(severity, probability)
        
        risk_item = QTableWidgetItem(risk)
        # Color code the risk level
        if risk == "High":
            risk_item.setBackground(Qt.red)
            risk_item.setForeground(Qt.white)
        elif risk == "Medium":
            risk_item.setBackground(Qt.yellow)
        elif risk == "Low":
            risk_item.setBackground(Qt.green)
            risk_item.setForeground(Qt.white)
        
        self.risk_table.setItem(row, 8, risk_item)

    def update_residual_risk_level(self, row):
        res_sev_cb = self.risk_table.cellWidget(row, 10)
        res_prob_cb = self.risk_table.cellWidget(row, 11)
        if not res_sev_cb or not res_prob_cb:
            return
        
        severity = res_sev_cb.currentText()
        probability = res_prob_cb.currentText()
        risk = self.calculate_risk_level(severity, probability)
        
        risk_item = QTableWidgetItem(risk)
        # Color code the risk level
        if risk == "High":
            risk_item.setBackground(Qt.red)
            risk_item.setForeground(Qt.white)
        elif risk == "Medium":
            risk_item.setBackground(Qt.yellow)
        elif risk == "Low":
            risk_item.setBackground(Qt.green)
            risk_item.setForeground(Qt.white)
        
        self.risk_table.setItem(row, 12, risk_item)

    def calculate_risk_level(self, severity, probability):
        """Calculate risk level based on severity and probability using the matrix"""
        severity_map = {"Catastrophic": 0, "Serious": 1, "Moderate": 2, "Minor": 3}
        probability_map = {"Very Likely": 0, "Likely": 1, "Unlikely": 2, "Remote": 3}
        
        sev_idx = severity_map.get(severity, 1)
        prob_idx = probability_map.get(probability, 1)
        
        # Risk matrix
        matrix = [
            ["High", "High", "High", "Medium"],
            ["High", "High", "Medium", "Low"],
            ["High", "Medium", "Low", "Low"],
            ["Medium", "Low", "Low", "Low"]
        ]
        
        return matrix[sev_idx][prob_idx]

    def save_assessment(self):
        """Save the current assessment to the current file"""
        if hasattr(self, 'current_file') and self.current_file:
            self.save_assessment_to_file(self.current_file)
        else:
            self.save_assessment_as()

    def save_assessment_as(self):
        """Save the current assessment to a new file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Assessment", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.current_file = file_path
            self.save_assessment_to_file(file_path)

    def save_assessment_to_file(self, file_path):
        """Save assessment data to a JSON file"""
        try:
            data = {
                'project_info': self.project_info,
                'hazard_data': self.get_hazard_data(),
                'risk_assessment_data': self.get_risk_assessment_data(),
                'control_system_data': self.get_control_system_data(),
                'alternative_method_data': self.get_alternative_method_data(),
                'risk_reduction_text': self.risk_reduction_text.toPlainText() if hasattr(self, 'risk_reduction_text') else ""
            }
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            QMessageBox.information(self, "Success", f"Assessment saved to {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save assessment: {str(e)}")

    def load_assessment(self):
        """Load an assessment from a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Assessment", "", "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.current_file = file_path
            self.load_assessment_from_file(file_path)

    def load_assessment_from_file(self, file_path):
        """Load assessment data from a JSON file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            self.project_info = data.get('project_info', {})
            self.load_hazard_data(data.get('hazard_data', []))
            self.load_risk_assessment_data(data.get('risk_assessment_data', []))
            self.load_control_system_data(data.get('control_system_data', []))
            self.load_alternative_method_data(data.get('alternative_method_data', []))
            
            if hasattr(self, 'risk_reduction_text') and 'risk_reduction_text' in data:
                self.risk_reduction_text.setPlainText(data['risk_reduction_text'])
            
            QMessageBox.information(self, "Success", f"Assessment loaded from {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load assessment: {str(e)}")

    def get_hazard_data(self):
        """Extract hazard data from the tree widget"""
        data = []
        for i in range(self.tree.topLevelItemCount()):
            user_item = self.tree.topLevelItem(i)
            user_data = {
                'user': user_item.text(0),
                'tasks': []
            }
            for j in range(user_item.childCount()):
                task_item = user_item.child(j)
                task_data = {
                    'task': task_item.text(1),
                    'hazards': []
                }
                for k in range(task_item.childCount()):
                    hazard_item = task_item.child(k)
                    task_data['hazards'].append(hazard_item.text(2))
                user_data['tasks'].append(task_data)
            data.append(user_data)
        return data

    def load_hazard_data(self, data):
        """Load hazard data into the tree widget"""
        self.tree.clear()
        for user_data in data:
            user_item = QTreeWidgetItem(self.tree)
            user_item.setText(0, user_data['user'])
            for task_data in user_data['tasks']:
                task_item = QTreeWidgetItem(user_item)
                task_item.setText(1, task_data['task'])
                for hazard in task_data['hazards']:
                    hazard_item = QTreeWidgetItem(task_item)
                    hazard_item.setText(2, hazard)

    def get_risk_assessment_data(self):
        """Extract risk assessment data from the table"""
        data = []
        for row in range(self.risk_table.rowCount()):
            row_data = {}
            for col in range(self.risk_table.columnCount()):
                item = self.risk_table.item(row, col)
                if item:
                    row_data[f'col_{col}'] = item.text()
                else:
                    widget = self.risk_table.cellWidget(row, col)
                    if widget and hasattr(widget, 'currentText'):
                        row_data[f'col_{col}'] = widget.currentText()
                    else:
                        row_data[f'col_{col}'] = ""
            data.append(row_data)
        return data

    def load_risk_assessment_data(self, data):
        """Load risk assessment data into the table"""
        self.risk_table.setRowCount(0)
        for row_data in data:
            row = self.risk_table.rowCount()
            self.risk_table.insertRow(row)
            for col in range(self.risk_table.columnCount()):
                value = row_data.get(f'col_{col}', "")
                self.risk_table.setItem(row, col, QTableWidgetItem(value))

    def get_control_system_data(self):
        """Extract control system data from the table"""
        data = []
        for row in range(self.control_table.rowCount()):
            row_data = {}
            for col in range(self.control_table.columnCount()):
                item = self.control_table.item(row, col)
                if item:
                    row_data[f'col_{col}'] = item.text()
                else:
                    widget = self.control_table.cellWidget(row, col)
                    if widget and hasattr(widget, 'currentText'):
                        row_data[f'col_{col}'] = widget.currentText()
                    else:
                        row_data[f'col_{col}'] = ""
            data.append(row_data)
        return data

    def load_control_system_data(self, data):
        """Load control system data into the table"""
        self.control_table.setRowCount(0)
        for row_data in data:
            row = self.control_table.rowCount()
            self.control_table.insertRow(row)
            for col in range(self.control_table.columnCount()):
                value = row_data.get(f'col_{col}', "")
                self.control_table.setItem(row, col, QTableWidgetItem(value))

    def get_alternative_method_data(self):
        """Extract alternative method data from the table"""
        data = []
        for row in range(self.alt_method_table.rowCount()):
            row_data = {}
            for col in range(self.alt_method_table.columnCount()):
                item = self.alt_method_table.item(row, col)
                if item:
                    row_data[f'col_{col}'] = item.text()
                else:
                    widget = self.alt_method_table.cellWidget(row, col)
                    if widget and hasattr(widget, 'currentText'):
                        row_data[f'col_{col}'] = widget.currentText()
                    else:
                        row_data[f'col_{col}'] = ""
            data.append(row_data)
        return data

    def load_alternative_method_data(self, data):
        """Load alternative method data into the table"""
        self.alt_method_table.setRowCount(0)
        for row_data in data:
            row = self.alt_method_table.rowCount()
            self.alt_method_table.insertRow(row)
            for col in range(self.alt_method_table.columnCount()):
                value = row_data.get(f'col_{col}', "")
                self.alt_method_table.setItem(row, col, QTableWidgetItem(value))

    def add_custom_hazard(self):
        """Add a custom hazard to the current category"""
        current_category = self.category_list.currentItem()
        if current_category is None:
            QMessageBox.warning(self, "Warning", "Please select a category first.")
            return
            
        category_name = current_category.text()
        if category_name == "All Categories":
            QMessageBox.warning(self, "Warning", "Please select a specific category, not 'All Categories'.")
            return
            
        # Get custom hazard input
        hazard_name, ok = QInputDialog.getText(self, "Add Custom Hazard", "Enter hazard name:")
        if ok and hazard_name:
            cause, ok2 = QInputDialog.getText(self, "Add Custom Hazard", "Enter cause/failure mode:")
            if ok2:
                # Add to the hazards table
                row = self.hazards_table.rowCount()
                self.hazards_table.insertRow(row)
                self.hazards_table.setItem(row, 0, QTableWidgetItem(hazard_name))
                self.hazards_table.setItem(row, 1, QTableWidgetItem(cause))
                
                checkbox = QCheckBox()
                checkbox.setStyleSheet("font-size: 24px;")
                self.hazards_table.setCellWidget(row, 2, checkbox)

    def edit_custom_hazard(self):
        """Edit the selected hazard in the hazards table"""
        current_row = self.hazards_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a hazard to edit.")
            return
            
        hazard_name = self.hazards_table.item(current_row, 0).text()
        cause = self.hazards_table.item(current_row, 1).text()
        
        new_hazard_name, ok = QInputDialog.getText(self, "Edit Hazard", "Enter hazard name:", text=hazard_name)
        if ok:
            new_cause, ok2 = QInputDialog.getText(self, "Edit Hazard", "Enter cause/failure mode:", text=cause)
            if ok2:
                self.hazards_table.setItem(current_row, 0, QTableWidgetItem(new_hazard_name))
                self.hazards_table.setItem(current_row, 1, QTableWidgetItem(new_cause))

    def delete_custom_hazard(self):
        """Delete the selected hazard from the hazards table"""
        current_row = self.hazards_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a hazard to delete.")
            return
            
        hazard_name = self.hazards_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete '{hazard_name}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hazards_table.removeRow(current_row)

    def create_control_system_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.control_table = QTableWidget()
        self.control_table.setColumnCount(8)
        self.control_table.setHorizontalHeaderLabels([
            "Safety Function", "Associated Hazard", "Initial Risk", "Final Risk", 
            "Required Category", "Actual Category", "Control Type", "Verification"
        ])
        self.control_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.control_table.setStyleSheet("font-size: 24px; QHeaderView::section { font-size: 24px; font-weight: bold; padding: 15px; }")
        layout.addWidget(self.control_table)
        
        # Category Calculator Section
        calc_layout = QHBoxLayout()
        calc_label = QLabel("Category Calculator:")
        calc_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 15px;")
        self.category_calc_cb = QComboBox()
        self.category_calc_cb.addItems([
            "Select Risk Level for Category Guidance",
            "Low Risk → Category 1",
            "Medium Risk → Category 2-3", 
            "High Risk → Category 3-4"
        ])
        self.category_calc_cb.setStyleSheet("font-size: 24px; padding: 15px; margin: 10px; border: 2px solid #ccc; border-radius: 8px;")
        calc_layout.addWidget(calc_label)
        calc_layout.addWidget(self.category_calc_cb)
        layout.addLayout(calc_layout)
        
        btn_layout = QHBoxLayout()
        add_control_btn = QPushButton("Add Control System")
        edit_control_btn = QPushButton("Edit Control System")
        delete_control_btn = QPushButton("Delete Control System")
        refresh_hazards_btn = QPushButton("Refresh Hazards")
        auto_populate_btn = QPushButton("Auto-Populate from Risk Assessment")
        
        # Style buttons with larger text
        button_style = "font-size: 24px; padding: 20px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;"
        add_control_btn.setStyleSheet(button_style)
        edit_control_btn.setStyleSheet(button_style)
        delete_control_btn.setStyleSheet(button_style)
        refresh_hazards_btn.setStyleSheet(button_style)
        auto_populate_btn.setStyleSheet(button_style)
        
        btn_layout.addWidget(add_control_btn)
        btn_layout.addWidget(edit_control_btn)
        btn_layout.addWidget(delete_control_btn)
        btn_layout.addWidget(refresh_hazards_btn)
        btn_layout.addWidget(auto_populate_btn)
        layout.addLayout(btn_layout)
        
        add_control_btn.clicked.connect(self.add_control_system)
        edit_control_btn.clicked.connect(self.edit_control_system)
        delete_control_btn.clicked.connect(self.delete_control_system)
        refresh_hazards_btn.clicked.connect(self.refresh_control_hazards)
        auto_populate_btn.clicked.connect(self.auto_populate_control_systems)
        
        tab.setLayout(layout)
        return tab

    def auto_populate_control_systems(self):
        # Clear existing control systems
        self.control_table.setRowCount(0)
        
        # Get all hazards from the risk assessment table
        for row in range(self.risk_table.rowCount()):
            user_role = self.risk_table.item(row, 1).text() if self.risk_table.item(row, 1) else ""
            task = self.risk_table.item(row, 2).text() if self.risk_table.item(row, 2) else ""
            hazard = self.risk_table.item(row, 4).text() if self.risk_table.item(row, 4) else ""
            initial_risk = self.risk_table.item(row, 8).text() if self.risk_table.item(row, 8) else ""
            final_risk = self.risk_table.item(row, 12).text() if self.risk_table.item(row, 12) else ""
            
            if user_role and task and hazard:
                # Create a new control system row
                control_row = self.control_table.rowCount()
                self.control_table.insertRow(control_row)
                
                # Safety Function (default based on hazard)
                safety_function = f"Control for {hazard}"
                self.control_table.setItem(control_row, 0, QTableWidgetItem(safety_function))
                
                # Associated Hazard (combo box with the specific hazard selected)
                hazard_cb = QComboBox()
                self.populate_hazard_combo(hazard_cb)
                # Find and select the matching hazard
                hazard_text = f"{user_role} - {task} - {hazard}"
                index = hazard_cb.findText(hazard_text)
                if index >= 0:
                    hazard_cb.setCurrentIndex(index)
                self.control_table.setCellWidget(control_row, 1, hazard_cb)
                
                # Initial Risk Level
                self.control_table.setItem(control_row, 2, QTableWidgetItem(initial_risk))
                
                # Final Risk Level
                self.control_table.setItem(control_row, 3, QTableWidgetItem(final_risk))
                
                # Required Category (default based on final risk)
                req_cat_cb = QComboBox()
                req_cat_cb.addItems(["Category 1", "Category 2", "Category 3", "Category 4"])
                req_cat_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                if final_risk == "High":
                    req_cat_cb.setCurrentIndex(3)  # Category 4
                elif final_risk == "Medium":
                    req_cat_cb.setCurrentIndex(2)  # Category 3
                else:
                    req_cat_cb.setCurrentIndex(0)  # Category 1
                self.control_table.setCellWidget(control_row, 4, req_cat_cb)
                
                # Actual Category (default to same as required)
                act_cat_cb = QComboBox()
                act_cat_cb.addItems(["Category 1", "Category 2", "Category 3", "Category 4"])
                act_cat_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                act_cat_cb.setCurrentIndex(req_cat_cb.currentIndex())
                self.control_table.setCellWidget(control_row, 5, act_cat_cb)
                
                # Control Type (default to "Interlock")
                type_cb = QComboBox()
                type_cb.addItems(["Interlock", "Light Curtain", "Emergency Stop", "Pressure Sensitive Mat", "Two-Hand Control", "Custom"])
                type_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                type_cb.setCurrentIndex(0)  # Default to "Interlock"
                type_cb.currentTextChanged.connect(lambda text, r=control_row: self.handle_custom_control_type(text, r))
                self.control_table.setCellWidget(control_row, 6, type_cb)
                
                # Verification (empty)
                self.control_table.setItem(control_row, 7, QTableWidgetItem(""))

    def add_control_system(self):
        row = self.control_table.rowCount()
        self.control_table.insertRow(row)
        
        # Safety Function (editable text)
        self.control_table.setItem(row, 0, QTableWidgetItem(""))
        
        # Associated Hazard (combo box)
        hazard_cb = QComboBox()
        self.populate_hazard_combo(hazard_cb)
        hazard_cb.setStyleSheet("font-size: 24px; padding: 8px;")
        self.control_table.setCellWidget(row, 1, hazard_cb)
        
        # Initial Risk Level (empty)
        self.control_table.setItem(row, 2, QTableWidgetItem(""))
        
        # Final Risk Level (empty)
        self.control_table.setItem(row, 3, QTableWidgetItem(""))
        
        # Required Category (combo box)
        req_cat_cb = QComboBox()
        req_cat_cb.addItems(["Category 1", "Category 2", "Category 3", "Category 4"])
        req_cat_cb.setStyleSheet("font-size: 24px; padding: 8px;")
        self.control_table.setCellWidget(row, 4, req_cat_cb)
        
        # Actual Category (combo box)
        act_cat_cb = QComboBox()
        act_cat_cb.addItems(["Category 1", "Category 2", "Category 3", "Category 4"])
        act_cat_cb.setStyleSheet("font-size: 24px; padding: 8px;")
        self.control_table.setCellWidget(row, 5, act_cat_cb)
        
        # Control Type (combo box with Custom option)
        type_cb = QComboBox()
        type_cb.addItems(["Interlock", "Light Curtain", "Emergency Stop", "Pressure Sensitive Mat", "Two-Hand Control", "Custom"])
        type_cb.setStyleSheet("font-size: 24px; padding: 8px;")
        type_cb.currentTextChanged.connect(lambda text, r=row: self.handle_custom_control_type(text, r))
        self.control_table.setCellWidget(row, 6, type_cb)
        
        # Verification (editable text)
        self.control_table.setItem(row, 7, QTableWidgetItem(""))

    def handle_custom_control_type(self, text, row):
        """Handle custom control type selection"""
        if text == "Custom":
            custom_text, ok = QInputDialog.getText(self, "Custom Control Type", "Enter custom control type:")
            if ok and custom_text:
                # Update the combo box with the new custom option
                new_cb = QComboBox()
                new_cb.addItems(["Interlock", "Light Curtain", "Emergency Stop", "Pressure Sensitive Mat", "Two-Hand Control", "Custom", custom_text])
                new_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                new_cb.setCurrentText(custom_text)
                new_cb.currentTextChanged.connect(lambda text, r=row: self.handle_custom_control_type(text, r))
                self.control_table.setCellWidget(row, 6, new_cb)

    def edit_control_system(self):
        # Implementation for editing control system
        pass

    def delete_control_system(self):
        # Implementation for deleting control system
        pass

    def refresh_control_hazards(self):
        # Refresh all hazard combo boxes in the control table
        pass

    def populate_hazard_combo(self, combo_box):
        """Populate a combo box with all hazards from the tree"""
        combo_box.clear()
        for i in range(self.tree.topLevelItemCount()):
            user_item = self.tree.topLevelItem(i)
            user_name = user_item.text(0)
            for j in range(user_item.childCount()):
                task_item = user_item.child(j)
                task_name = task_item.text(1)
                for k in range(task_item.childCount()):
                    hazard_item = task_item.child(k)
                    hazard_name = hazard_item.text(2)
                    combo_box.addItem(f"{user_name} - {task_name} - {hazard_name}")

    def create_alternative_method_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Alternative Method Table
        self.alt_method_table = QTableWidget()
        self.alt_method_table.setColumnCount(9)
        self.alt_method_table.setHorizontalHeaderLabels([
            "Task", "Associated Hazard", "Risk Assessment Complete", "Justification", "Procedure", 
            "Engineering Controls", "Training Requirements", "Verification Steps", "Approvals"
        ])
        self.alt_method_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.alt_method_table.setStyleSheet("font-size: 24px; QHeaderView::section { font-size: 24px; font-weight: bold; padding: 15px; }")
        layout.addWidget(self.alt_method_table)
        
        # Buttons
        btn_layout = QHBoxLayout()
        add_alt_method_btn = QPushButton("Add Alternative Method")
        edit_alt_method_btn = QPushButton("Edit Alternative Method")
        delete_alt_method_btn = QPushButton("Delete Alternative Method")
        refresh_hazards_btn = QPushButton("Refresh Hazards")
        auto_populate_alt_btn = QPushButton("Auto-Populate from Risk Assessment")
        validate_btn = QPushButton("Validate A/M Compliance")
        generate_report_btn = QPushButton("Generate PDF Report")
        
        # Style buttons with larger text
        button_style = "font-size: 24px; padding: 20px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;"
        add_alt_method_btn.setStyleSheet(button_style)
        edit_alt_method_btn.setStyleSheet(button_style)
        delete_alt_method_btn.setStyleSheet(button_style)
        refresh_hazards_btn.setStyleSheet(button_style)
        auto_populate_alt_btn.setStyleSheet(button_style)
        validate_btn.setStyleSheet(button_style)
        generate_report_btn.setStyleSheet(button_style)
        
        btn_layout.addWidget(add_alt_method_btn)
        btn_layout.addWidget(edit_alt_method_btn)
        btn_layout.addWidget(delete_alt_method_btn)
        btn_layout.addWidget(refresh_hazards_btn)
        btn_layout.addWidget(auto_populate_alt_btn)
        btn_layout.addWidget(validate_btn)
        btn_layout.addWidget(generate_report_btn)
        layout.addLayout(btn_layout)
        
        add_alt_method_btn.clicked.connect(self.add_alternative_method)
        edit_alt_method_btn.clicked.connect(self.edit_alternative_method)
        delete_alt_method_btn.clicked.connect(self.delete_alternative_method)
        refresh_hazards_btn.clicked.connect(self.refresh_alt_method_hazards)
        auto_populate_alt_btn.clicked.connect(self.auto_populate_alternative_methods)
        validate_btn.clicked.connect(self.validate_alternative_methods)
        generate_report_btn.clicked.connect(self.generate_pdf_report)
        
        tab.setLayout(layout)
        return tab

    def add_alternative_method(self):
        row = self.alt_method_table.rowCount()
        self.alt_method_table.insertRow(row)
        
        # Task (editable text)
        self.alt_method_table.setItem(row, 0, QTableWidgetItem(""))
        
        # Associated Hazard (combo box)
        hazard_cb = QComboBox()
        self.populate_hazard_combo(hazard_cb)
        hazard_cb.setStyleSheet("font-size: 24px; padding: 8px;")
        self.alt_method_table.setCellWidget(row, 1, hazard_cb)
        
        # Risk Assessment Complete (combo box)
        risk_assessment_cb = QComboBox()
        risk_assessment_cb.addItems(["Yes", "No", "In Progress"])
        risk_assessment_cb.setStyleSheet("font-size: 24px; padding: 8px;")
        self.alt_method_table.setCellWidget(row, 2, risk_assessment_cb)
        
        # Justification (editable text)
        self.alt_method_table.setItem(row, 3, QTableWidgetItem(""))
        
        # Procedure (editable text)
        self.alt_method_table.setItem(row, 4, QTableWidgetItem(""))
        
        # Engineering Controls (editable text)
        self.alt_method_table.setItem(row, 5, QTableWidgetItem(""))
        
        # Training Requirements (editable text)
        self.alt_method_table.setItem(row, 6, QTableWidgetItem(""))
        
        # Verification Steps (editable text)
        self.alt_method_table.setItem(row, 7, QTableWidgetItem(""))
        
        # Approvals (editable text)
        self.alt_method_table.setItem(row, 8, QTableWidgetItem(""))

    def edit_alternative_method(self):
        # Implementation for editing alternative method
        pass

    def delete_alternative_method(self):
        # Implementation for deleting alternative method
        pass

    def refresh_alt_method_hazards(self):
        # Refresh all hazard combo boxes in the alternative method table
        pass

    def validate_alternative_methods(self):
        """Validate alternative methods for compliance with ANSI Z244.1 requirements"""
        if self.alt_method_table.rowCount() == 0:
            QMessageBox.information(self, "Validation", "No alternative methods to validate.")
            return
        
        issues = []
        warnings = []
        
        for row in range(self.alt_method_table.rowCount()):
            row_num = row + 1
            
            # Check for missing required fields
            task = self.alt_method_table.item(row, 0).text() if self.alt_method_table.item(row, 0) else ""
            hazard = ""
            hazard_widget = self.alt_method_table.cellWidget(row, 1)
            if hazard_widget:
                hazard = hazard_widget.currentText()
            
            risk_complete = ""
            risk_widget = self.alt_method_table.cellWidget(row, 2)
            if risk_widget:
                risk_complete = risk_widget.currentText()
            
            justification = self.alt_method_table.item(row, 3).text() if self.alt_method_table.item(row, 3) else ""
            procedure = self.alt_method_table.item(row, 4).text() if self.alt_method_table.item(row, 4) else ""
            engineering_controls = self.alt_method_table.item(row, 5).text() if self.alt_method_table.item(row, 5) else ""
            training = self.alt_method_table.item(row, 6).text() if self.alt_method_table.item(row, 6) else ""
            verification = self.alt_method_table.item(row, 7).text() if self.alt_method_table.item(row, 7) else ""
            approvals = self.alt_method_table.item(row, 8).text() if self.alt_method_table.item(row, 8) else ""
            
            # Validation checks
            if not task:
                issues.append(f"Row {row_num}: Missing Task")
            if not hazard:
                issues.append(f"Row {row_num}: Missing Associated Hazard")
            if not justification:
                issues.append(f"Row {row_num}: Missing Justification for Alternative Method")
            if not procedure:
                issues.append(f"Row {row_num}: Missing Procedure")
            if not engineering_controls:
                issues.append(f"Row {row_num}: Missing Engineering Controls")
            if not training:
                issues.append(f"Row {row_num}: Missing Training Requirements")
            if not verification:
                issues.append(f"Row {row_num}: Missing Verification Steps")
            if not approvals:
                issues.append(f"Row {row_num}: Missing Approvals")
            
            # Risk assessment completion check
            if risk_complete != "Yes":
                warnings.append(f"Row {row_num}: Risk Assessment not marked as complete")
            
            # Content quality checks
            if justification and len(justification) < 20:
                warnings.append(f"Row {row_num}: Justification may be too brief")
            if procedure and len(procedure) < 30:
                warnings.append(f"Row {row_num}: Procedure may be too brief")
        
        # Create validation report
        report = "Alternative Method Validation Report\n"
        report += "=" * 40 + "\n\n"
        
        if not issues and not warnings:
            report += "✅ All alternative methods are compliant!\n\n"
            report += "All required fields are completed and risk assessments are marked as complete."
        else:
            if issues:
                report += "❌ CRITICAL ISSUES (Must be fixed):\n"
                for issue in issues:
                    report += f"  • {issue}\n"
                report += "\n"
            
            if warnings:
                report += "⚠️ WARNINGS (Should be addressed):\n"
                for warning in warnings:
                    report += f"  • {warning}\n"
                report += "\n"
            
            report += "ANSI Z244.1 Compliance Requirements:\n"
            report += "• All alternative methods must have complete documentation\n"
            report += "• Risk assessment must be completed before implementing A/M\n"
            report += "• Engineering controls must be specified\n"
            report += "• Training requirements must be documented\n"
            report += "• Verification steps must be established\n"
            report += "• Management approval must be obtained\n"
        
        # Show validation results
        msg = QMessageBox()
        msg.setWindowTitle("Alternative Method Validation")
        msg.setText(report)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("font-size: 16px;")
        msg.exec_()

    def auto_populate_alternative_methods(self):
        # Clear existing alternative methods
        self.alt_method_table.setRowCount(0)
        
        # Get all hazards from the risk assessment table
        for row in range(self.risk_table.rowCount()):
            user_role = self.risk_table.item(row, 1).text() if self.risk_table.item(row, 1) else ""
            task = self.risk_table.item(row, 2).text() if self.risk_table.item(row, 2) else ""
            hazard = self.risk_table.item(row, 4).text() if self.risk_table.item(row, 4) else ""
            initial_risk = self.risk_table.item(row, 8).text() if self.risk_table.item(row, 8) else ""
            final_risk = self.risk_table.item(row, 12).text() if self.risk_table.item(row, 12) else ""
            
            if user_role and task and hazard:
                # Create a new alternative method row
                alt_row = self.alt_method_table.rowCount()
                self.alt_method_table.insertRow(alt_row)
                
                # Task
                self.alt_method_table.setItem(alt_row, 0, QTableWidgetItem(task))
                
                # Associated Hazard (combo box)
                hazard_cb = QComboBox()
                self.populate_hazard_combo(hazard_cb)
                hazard_text = f"{user_role} - {task} - {hazard}"
                index = hazard_cb.findText(hazard_text)
                if index >= 0:
                    hazard_cb.setCurrentIndex(index)
                self.alt_method_table.setCellWidget(alt_row, 1, hazard_cb)
                
                # Risk Assessment Complete (default to "Yes")
                risk_assessment_cb = QComboBox()
                risk_assessment_cb.addItems(["Yes", "No", "In Progress"])
                risk_assessment_cb.setStyleSheet("font-size: 24px; padding: 8px;")
                risk_assessment_cb.setCurrentIndex(0)  # Yes
                self.alt_method_table.setCellWidget(alt_row, 2, risk_assessment_cb)
                
                # Justification (default text)
                justification = f"LOTO not feasible for {task} due to {hazard}. Alternative method provides equivalent protection."
                self.alt_method_table.setItem(alt_row, 3, QTableWidgetItem(justification))
                
                # Procedure (empty)
                self.alt_method_table.setItem(alt_row, 4, QTableWidgetItem(""))
                
                # Engineering Controls (empty)
                self.alt_method_table.setItem(alt_row, 5, QTableWidgetItem(""))
                
                # Training Requirements (empty)
                self.alt_method_table.setItem(alt_row, 6, QTableWidgetItem(""))
                
                # Verification Steps (empty)
                self.alt_method_table.setItem(alt_row, 7, QTableWidgetItem(""))
                
                # Approvals (empty)
                self.alt_method_table.setItem(alt_row, 8, QTableWidgetItem(""))

    def generate_pdf_report(self):
        """Generate a comprehensive PDF report of the entire assessment"""
        try:
            from reportlab.lib.pagesizes import letter, A4, landscape
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
            from datetime import datetime
            
            # Get file path for saving
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF Report", "", "PDF Files (*.pdf);;All Files (*)"
            )
            if not file_path:
                return
            
            if not file_path.endswith('.pdf'):
                file_path += '.pdf'
            
            # Create PDF document in landscape orientation
            doc = SimpleDocTemplate(file_path, pagesize=landscape(letter), 
                                  rightMargin=0.3*inch, leftMargin=0.3*inch, 
                                  topMargin=0.3*inch, bottomMargin=0.3*inch)
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=20,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=12,
                spaceAfter=10,
                spaceBefore=15,
                fontName='Helvetica-Bold'
            )
            normal_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=9,
                spaceAfter=4,
                fontName='Helvetica'
            )
            cell_style = ParagraphStyle(
                'CellStyle',
                parent=styles['Normal'],
                fontSize=8,
                spaceAfter=2,
                spaceBefore=2,
                fontName='Helvetica',
                alignment=TA_LEFT,
                wordWrap='CJK'  # Enable word wrapping
            )
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontSize=8,
                spaceAfter=2,
                spaceBefore=2,
                fontName='Helvetica-Bold',
                alignment=TA_CENTER,
                wordWrap='CJK'
            )
            
            # Title
            title = Paragraph("Risk Assessment Report", title_style)
            story.append(title)
            story.append(Spacer(1, 15))
            
            # Report Metadata Section
            story.append(Paragraph("Report Information", heading_style))
            
            # Get current date
            current_date = datetime.now().strftime("%m/%d/%Y")
            
            # Create metadata table
            metadata_data = [
                ["Application:", self.project_info.get('name', 'N/A') if hasattr(self, 'project_info') and self.project_info else 'N/A'],
                ["Description:", self.project_info.get('description', 'N/A') if hasattr(self, 'project_info') and self.project_info else 'N/A'],
                ["Product Identifier:", self.project_info.get('machine_id', 'N/A') if hasattr(self, 'project_info') and self.project_info else 'N/A'],
                ["Assessment Type:", "Detailed"],
                ["Limits:", "Risk assessment analysis"],
                ["Sources:", "Personnel experiences, ANSI B11 standards, machine documentation"],
                ["Risk Scoring System:", "ANSI B11.0 (TR3) Two Factor"],
                ["Guide Sentence:", "When doing [task], the [user] could be injured by the [hazard] due to the [failure mode]."],
                ["Analyst Name(s):", "Risk Assessment Team"],
                ["Company:", self.project_info.get('company', 'N/A') if hasattr(self, 'project_info') and self.project_info else 'N/A'],
                ["Facility Location:", self.project_info.get('facility', 'N/A') if hasattr(self, 'project_info') and self.project_info else 'N/A'],
                ["Date:", current_date]
            ]
            
            metadata_table = Table(metadata_data, colWidths=[2*inch, 6*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.grey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (1, 0), (1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('WORDWRAP', (0, 0), (-1, -1), True)
            ]))
            story.append(metadata_table)
            story.append(Spacer(1, 15))
            
            # Risk Assessment Table (Main Content)
            story.append(Paragraph("Risk Assessment Details", heading_style))
            
            if self.risk_table.rowCount() > 0:
                # Create comprehensive risk assessment table with Paragraph objects for text wrapping
                risk_data = []
                
                # Header row with Paragraph objects
                header_row = [
                    Paragraph("Item Id", header_style),
                    Paragraph("User / Task", header_style),
                    Paragraph("Hazard / Failure Mode", header_style),
                    Paragraph("Initial Assessment - Severity", header_style),
                    Paragraph("Initial Assessment - Probability", header_style),
                    Paragraph("Initial Assessment - Risk Level", header_style),
                    Paragraph("Risk Reduction Methods / Control System", header_style),
                    Paragraph("Final Assessment - Severity", header_style),
                    Paragraph("Final Assessment - Probability", header_style),
                    Paragraph("Final Assessment - Risk Level", header_style),
                    Paragraph("Status / Responsible / Comments / Reference", header_style)
                ]
                risk_data.append(header_row)
                
                for row in range(self.risk_table.rowCount()):
                    # Use the same approach as get_risk_assessment_data for consistency
                    row_data = {}
                    for col in range(self.risk_table.columnCount()):
                        item = self.risk_table.item(row, col)
                        if item:
                            row_data[f'col_{col}'] = item.text()
                        else:
                            widget = self.risk_table.cellWidget(row, col)
                            if widget and hasattr(widget, 'currentText'):
                                row_data[f'col_{col}'] = widget.currentText()
                            else:
                                row_data[f'col_{col}'] = ""
                    
                    # Extract values using the same logic as the save/load functions
                    item_id = row_data.get('col_0', "")
                    user_role = row_data.get('col_1', "")
                    task = row_data.get('col_2', "")
                    hazard_category = row_data.get('col_3', "")
                    hazard = row_data.get('col_4', "")
                    cause = row_data.get('col_5', "")
                    init_sev = row_data.get('col_6', "")
                    init_prob = row_data.get('col_7', "")
                    init_risk = row_data.get('col_8', "")
                    measures = row_data.get('col_9', "")
                    final_sev = row_data.get('col_10', "")
                    final_prob = row_data.get('col_11', "")
                    final_risk = row_data.get('col_12', "")
                    
                    # Format the data
                    user_task = f"{user_role} {task}" if user_role and task else f"{user_role}{task}"
                    hazard_failure = f"{hazard_category}: {hazard} {cause}".strip()
                    
                    # Status (placeholder - could be enhanced with actual status tracking)
                    status = "In Progress"
                    
                    # Create row with Paragraph objects for proper text wrapping
                    data_row = [
                        Paragraph(item_id, cell_style),
                        Paragraph(user_task, cell_style),
                        Paragraph(hazard_failure, cell_style),
                        Paragraph(init_sev, cell_style),
                        Paragraph(init_prob, cell_style),
                        Paragraph(init_risk, cell_style),
                        Paragraph(measures, cell_style),
                        Paragraph(final_sev, cell_style),
                        Paragraph(final_prob, cell_style),
                        Paragraph(final_risk, cell_style),
                        Paragraph(status, cell_style)
                    ]
                    risk_data.append(data_row)
                
                # Create table with fixed column widths for landscape orientation
                col_widths = [0.4*inch, 1.0*inch, 1.6*inch, 0.6*inch, 0.6*inch, 0.6*inch, 
                             1.8*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.9*inch]
                
                risk_table = Table(risk_data, colWidths=col_widths, repeatRows=1)
                risk_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                story.append(risk_table)
            else:
                story.append(Paragraph("No risk assessment data available", normal_style))
            
            story.append(PageBreak())
            
            # Control System Assessment Section
            story.append(Paragraph("Control System Assessment", heading_style))
            if self.control_table.rowCount() > 0:
                control_data = []
                
                # Header row
                control_header = [
                    Paragraph("Safety Function", header_style),
                    Paragraph("Associated Hazard", header_style),
                    Paragraph("Initial Risk", header_style),
                    Paragraph("Final Risk", header_style),
                    Paragraph("Required Category", header_style),
                    Paragraph("Actual Category", header_style),
                    Paragraph("Control Type", header_style),
                    Paragraph("Verification", header_style)
                ]
                control_data.append(control_header)
                
                for row in range(self.control_table.rowCount()):
                    # Use the same approach as get_control_system_data for consistency
                    row_data = {}
                    for col in range(self.control_table.columnCount()):
                        item = self.control_table.item(row, col)
                        if item:
                            row_data[f'col_{col}'] = item.text()
                        else:
                            widget = self.control_table.cellWidget(row, col)
                            if widget and hasattr(widget, 'currentText'):
                                row_data[f'col_{col}'] = widget.currentText()
                            else:
                                row_data[f'col_{col}'] = ""
                    
                    # Extract values using the same logic as the save/load functions
                    safety_function = row_data.get('col_0', "")
                    hazard = row_data.get('col_1', "")
                    initial_risk = row_data.get('col_2', "")
                    final_risk = row_data.get('col_3', "")
                    req_category = row_data.get('col_4', "")
                    act_category = row_data.get('col_5', "")
                    control_type = row_data.get('col_6', "")
                    verification = row_data.get('col_7', "")
                    
                    control_row = [
                        Paragraph(safety_function, cell_style),
                        Paragraph(hazard, cell_style),
                        Paragraph(initial_risk, cell_style),
                        Paragraph(final_risk, cell_style),
                        Paragraph(req_category, cell_style),
                        Paragraph(act_category, cell_style),
                        Paragraph(control_type, cell_style),
                        Paragraph(verification, cell_style)
                    ]
                    control_data.append(control_row)
                
                control_table = Table(control_data, colWidths=[1.3*inch, 1.8*inch, 0.7*inch, 0.7*inch, 
                                                              0.9*inch, 0.9*inch, 1.1*inch, 1.6*inch], repeatRows=1)
                control_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                story.append(control_table)
            else:
                story.append(Paragraph("No control system data available", normal_style))
            
            story.append(PageBreak())
            
            # Alternative Methods Section
            story.append(Paragraph("Alternative Methods Assessment", heading_style))
            if self.alt_method_table.rowCount() > 0:
                alt_data = []
                
                # Header row
                alt_header = [
                    Paragraph("Task", header_style),
                    Paragraph("Associated Hazard", header_style),
                    Paragraph("Risk Assessment Complete", header_style),
                    Paragraph("Justification", header_style),
                    Paragraph("Procedure", header_style),
                    Paragraph("Engineering Controls", header_style),
                    Paragraph("Training Requirements", header_style),
                    Paragraph("Verification Steps", header_style),
                    Paragraph("Approvals", header_style)
                ]
                alt_data.append(alt_header)
                
                for row in range(self.alt_method_table.rowCount()):
                    # Use the same approach as get_alternative_method_data for consistency
                    row_data = {}
                    for col in range(self.alt_method_table.columnCount()):
                        item = self.alt_method_table.item(row, col)
                        if item:
                            row_data[f'col_{col}'] = item.text()
                        else:
                            widget = self.alt_method_table.cellWidget(row, col)
                            if widget and hasattr(widget, 'currentText'):
                                row_data[f'col_{col}'] = widget.currentText()
                            else:
                                row_data[f'col_{col}'] = ""
                    
                    # Extract values using the same logic as the save/load functions
                    task = row_data.get('col_0', "")
                    hazard = row_data.get('col_1', "")
                    risk_complete = row_data.get('col_2', "")
                    justification = row_data.get('col_3', "")
                    procedure = row_data.get('col_4', "")
                    engineering_controls = row_data.get('col_5', "")
                    training = row_data.get('col_6', "")
                    verification = row_data.get('col_7', "")
                    approvals = row_data.get('col_8', "")
                    
                    alt_row = [
                        Paragraph(task, cell_style),
                        Paragraph(hazard, cell_style),
                        Paragraph(risk_complete, cell_style),
                        Paragraph(justification, cell_style),
                        Paragraph(procedure, cell_style),
                        Paragraph(engineering_controls, cell_style),
                        Paragraph(training, cell_style),
                        Paragraph(verification, cell_style),
                        Paragraph(approvals, cell_style)
                    ]
                    alt_data.append(alt_row)
                
                alt_table = Table(alt_data, colWidths=[0.8*inch, 1.8*inch, 0.8*inch, 1.2*inch, 1.2*inch, 
                                                       1.2*inch, 1.2*inch, 1.2*inch, 0.8*inch], repeatRows=1)
                alt_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('LEFTPADDING', (0, 0), (-1, -1), 4),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
                ]))
                story.append(alt_table)
            else:
                story.append(Paragraph("No alternative methods data available", normal_style))
            
            # Build PDF
            doc.build(story)
            
            QMessageBox.information(self, "Success", f"PDF report generated successfully: {file_path}")
            
        except ImportError:
            QMessageBox.critical(self, "Error", "ReportLab library not found. Please install it with: pip install reportlab")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate PDF report:\n{str(e)}")

class RiskReductionMethodsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Risk Reduction Methods")
        self.setMinimumSize(800, 600)
        self.setStyleSheet("font-size: 20px;")
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Select Risk Reduction Methods (Hierarchy of Controls):")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Tree widget for hierarchical methods
        self.methods_tree = QTreeWidget()
        self.methods_tree.setHeaderLabels(["Method", "Description"])
        self.methods_tree.setStyleSheet("font-size: 20px; QHeaderView::section { font-size: 20px; font-weight: bold; padding: 15px; }")
        self.populate_risk_reduction_methods()
        layout.addWidget(self.methods_tree)
        
        # Buttons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        
        btn_style = "font-size: 20px; padding: 15px; margin: 10px; background-color: #f0f0f0; border: 2px solid #ccc; border-radius: 10px;"
        ok_btn.setStyleSheet(btn_style)
        cancel_btn.setStyleSheet(btn_style)
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def populate_risk_reduction_methods(self):
        """Populate the hierarchical risk reduction methods"""
        methods = {
            "1 Eliminate by design": [
                "1.1 Prevent energy buildup",
                "1.2 Prevent energy release", 
                "1.3 Separate hazard/people in time or space",
                "1.4 Wire to electrical codes (NEC/IEC)",
                "1.5 Other design change"
            ],
            "2 Substitution": [
                "2.1 Replace with less hazardous material",
                "2.2 Replace with less hazardous process",
                "2.3 Replace with less hazardous equipment"
            ],
            "3 Guard against hazard": [
                "3.1 Fixed guards",
                "3.2 Interlocked guards",
                "3.3 Adjustable guards",
                "3.4 Self-adjusting guards",
                "3.5 Safety devices (light curtains, pressure mats)"
            ],
            "4 Warn of hazard": [
                "4.1 Warning signs and labels",
                "4.2 Warning lights and alarms",
                "4.3 Safety instructions and procedures"
            ],
            "5 Train user": [
                "5.1 Safety training programs",
                "5.2 Standard operating procedures",
                "5.3 Emergency response training",
                "5.4 Competency assessment"
            ],
            "6 Personal Protective Equipment (PPE)": [
                "6.1 Head protection (hard hats)",
                "6.2 Eye and face protection",
                "6.3 Hearing protection",
                "6.4 Respiratory protection",
                "6.5 Hand protection (gloves)",
                "6.6 Body protection (safety vests, coveralls)",
                "6.7 Foot protection (safety shoes)",
                "6.8 Fall protection equipment"
            ]
        }
        
        for category, submethods in methods.items():
            category_item = QTreeWidgetItem(self.methods_tree)
            category_item.setText(0, category)
            category_item.setCheckState(0, Qt.Unchecked)
            
            for submethod in submethods:
                sub_item = QTreeWidgetItem(category_item)
                sub_item.setText(0, submethod)
                sub_item.setCheckState(0, Qt.Unchecked)

    def get_selected_methods(self):
        """Get all selected methods from the tree"""
        selected = []
        
        def traverse_items(item):
            if item.checkState(0) == Qt.Checked:
                selected.append(item.text(0))
            for i in range(item.childCount()):
                traverse_items(item.child(i))
        
        for i in range(self.methods_tree.topLevelItemCount()):
            traverse_items(self.methods_tree.topLevelItem(i))
        
        return selected

def main():
    app = QApplication(sys.argv)
    
    # Show startup dialog
    startup_dialog = StartupDialog()
    if startup_dialog.exec_() == QDialog.Accepted:
        if startup_dialog.choice == "new":
            # Show project setup wizard for new assessment
            wizard = ProjectSetupWizard()
            if wizard.exec_() == QDialog.Accepted:
                project_info = {
                    'name': wizard.project_name.text(),
                    'description': wizard.project_desc.toPlainText(),
                    'company': wizard.company_name.text(),
                    'facility': wizard.facility_location.text(),
                    'machine_id': wizard.machine_id.text(),
                    'lifecycle_stage': wizard.lifecycle_stage.text()
                }
                main_window = MainWindow(project_info)
                main_window.show()
            else:
                sys.exit(0)
        elif startup_dialog.choice == "load":
            # Show file dialog to load existing assessment
            filename, _ = QFileDialog.getOpenFileName(
                None, "Load Assessment", "", "JSON Files (*.json);;All Files (*)"
            )
            if filename:
                main_window = MainWindow()
                main_window.load_assessment_from_file(filename)
                main_window.show()
            else:
                sys.exit(0)
    else:
        sys.exit(0)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 