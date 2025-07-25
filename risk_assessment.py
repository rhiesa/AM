from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional

class Severity(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

class Likelihood(Enum):
    RARE = auto()
    OCCASIONAL = auto()
    FREQUENT = auto()

class EnergyType(Enum):
    MECHANICAL = "Mechanical"
    ELECTRICAL = "Electrical"
    HYDRAULIC = "Hydraulic"
    PNEUMATIC = "Pneumatic"
    THERMAL = "Thermal"
    CHEMICAL = "Chemical"
    GRAVITATIONAL = "Gravitational"
    OTHER = "Other"

def calculate_risk_level(severity: Severity, likelihood: Likelihood) -> str:
    """
    Simple risk matrix:
    - If either severity or likelihood is HIGH/FREQUENT, risk is 'High'.
    - If both are LOW/RARE, risk is 'Low'.
    - Otherwise, risk is 'Medium'.
    """
    if severity == Severity.HIGH or likelihood == Likelihood.FREQUENT:
        return "High"
    elif severity == Severity.LOW and likelihood == Likelihood.RARE:
        return "Low"
    else:
        return "Medium"

@dataclass
class AlternativeMethodPlan:
    justification: str = ""
    procedure: str = ""
    engineering_controls: str = ""
    training_requirements: str = ""
    verification_steps: str = ""
    approvals: str = ""

@dataclass
class Hazard:
    description: str
    energy_type: EnergyType
    severity: Severity
    likelihood: Likelihood
    initial_risk_level: Optional[str] = None
    controls: List[str] = field(default_factory=list)
    residual_risk_level: Optional[str] = None

    def __post_init__(self):
        # Set initial risk level based on severity and likelihood
        self.initial_risk_level = calculate_risk_level(self.severity, self.likelihood)
        # If no controls are applied yet, residual risk is same as initial
        if not self.controls:
            self.residual_risk_level = self.initial_risk_level

    def apply_controls(self, controls: List[str], new_severity: Severity, new_likelihood: Likelihood):
        self.controls = controls
        self.residual_risk_level = calculate_risk_level(new_severity, new_likelihood)

@dataclass
class Task:
    name: str
    description: str = ""
    is_alternative_method: bool = False
    hazards: List[Hazard] = field(default_factory=list)
    alt_method_plan: Optional[AlternativeMethodPlan] = None

    def add_hazard(self, hazard: Hazard):
        self.hazards.append(hazard)

    def mark_alternative_method(self, plan: AlternativeMethodPlan):
        self.is_alternative_method = True
        self.alt_method_plan = plan

@dataclass
class Project:
    name: str
    description: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        self.tasks.append(task)

def generate_report(project: Project) -> str:
    lines = []
    lines.append(f"# Risk Assessment Report\n")
    lines.append(f"**Project Name:** {project.name}")
    lines.append(f"**Description:** {project.description}\n")
    for t_idx, task in enumerate(project.tasks, 1):
        task_label = f"Task {t_idx}: {task.name}"
        if task.is_alternative_method:
            task_label += " [Alternative Method Task]"
        lines.append(task_label)
        if task.description:
            lines.append(f"  Description: {task.description}")
        for h_idx, hazard in enumerate(task.hazards, 1):
            lines.append(f"    Hazard {h_idx}: {hazard.description}")
            lines.append(f"      Energy Type: {hazard.energy_type.value}")
            lines.append(f"      Severity: {hazard.severity.name.title()}")
            lines.append(f"      Likelihood: {hazard.likelihood.name.title()}")
            lines.append(f"      Initial Risk Level: {hazard.initial_risk_level}")
            if hazard.controls:
                lines.append(f"      Controls Applied:")
                for ctrl in hazard.controls:
                    lines.append(f"        - {ctrl}")
            lines.append(f"      Residual Risk Level: {hazard.residual_risk_level}")
        if task.alt_method_plan:
            plan = task.alt_method_plan
            lines.append(f"    Alternative Method Details:")
            lines.append(f"      Justification: {plan.justification}")
            lines.append(f"      Procedure: {plan.procedure}")
            lines.append(f"      Engineering Controls: {plan.engineering_controls}")
            lines.append(f"      Training Requirements: {plan.training_requirements}")
            lines.append(f"      Verification Steps: {plan.verification_steps}")
            lines.append(f"      Approvals: {plan.approvals}")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    print("--- Risk Assessment Project Setup ---")
    project_name = input("Enter project name: ")
    project_desc = input("Enter project description: ")
    project = Project(name=project_name, description=project_desc)

    while True:
        print("\n--- Add a Task ---")
        task_name = input("Task name: ")
        task_desc = input("Task description: ")
        alt_method_input = input("Is this task an Alternative Method task (not full lockout)? (y/n): ").strip().lower()
        is_alt_method = alt_method_input == 'y'
        task = Task(name=task_name, description=task_desc, is_alternative_method=is_alt_method)

        # Add hazards to the task
        while True:
            print("\nAdd a hazard for this task:")
            hazard_desc = input("Hazard description: ")
            print("Select energy type:")
            for i, et in enumerate(EnergyType, 1):
                print(f"  {i}. {et.value}")
            et_choice = int(input("Enter number: "))
            energy_type = list(EnergyType)[et_choice - 1]

            print("Select severity:")
            for i, sev in enumerate(Severity, 1):
                print(f"  {i}. {sev.name.title()}")
            sev_choice = int(input("Enter number: "))
            severity = list(Severity)[sev_choice - 1]

            print("Select likelihood:")
            for i, lh in enumerate(Likelihood, 1):
                print(f"  {i}. {lh.name.title()}")
            lh_choice = int(input("Enter number: "))
            likelihood = list(Likelihood)[lh_choice - 1]

            hazard = Hazard(
                description=hazard_desc,
                energy_type=energy_type,
                severity=severity,
                likelihood=likelihood
            )
            task.add_hazard(hazard)

            more_hazards = input("Add another hazard to this task? (y/n): ").strip().lower()
            if more_hazards != 'y':
                break

        # If alternative method, gather plan details
        if is_alt_method:
            print("\n--- Alternative Method Plan Details ---")
            justification = input("Justification for not locking out: ")
            procedure = input("Procedure for the task: ")
            engineering_controls = input("Engineering controls used: ")
            training_requirements = input("Employee training/qualifications: ")
            verification_steps = input("Verification steps: ")
            approvals = input("Approvals required: ")
            plan = AlternativeMethodPlan(
                justification=justification,
                procedure=procedure,
                engineering_controls=engineering_controls,
                training_requirements=training_requirements,
                verification_steps=verification_steps,
                approvals=approvals
            )
            task.mark_alternative_method(plan)

        project.add_task(task)
        more_tasks = input("Add another task? (y/n): ").strip().lower()
        if more_tasks != 'y':
            break

    print("\nData entry complete. (Report generation will be implemented next.)")
    print("\n--- Generated Report ---\n")
    print(generate_report(project)) 