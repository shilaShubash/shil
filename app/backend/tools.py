"""
Tools and template management for the OT Mentor AI.

Implements the 18-field template, Template Filler tool, and Context Evaluator.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


# Template field definitions
TEMPLATE_FIELDS = {
    # Therapist Profile
    "therapist_role": {"critical": True, "category": "therapist"},
    "years_experience": {"critical": True, "category": "therapist"},
    "area_specialization": {"critical": False, "category": "therapist"},
    "therapist_setting": {"critical": True, "category": "therapist"},

    # Patient Profile
    "patient_age": {"critical": True, "category": "patient"},
    "patient_gender": {"critical": False, "category": "patient"},
    "diagnosis": {"critical": True, "category": "patient"},
    "cultural_background": {"critical": True, "category": "patient"},
    "marital_status": {"critical": True, "category": "patient"},
    "educational_framework": {"critical": False, "category": "patient"},
    "occupational_framework": {"critical": False, "category": "patient"},
    "hobbies_leisure": {"critical": False, "category": "patient"},

    # Treatment Context
    "treatment_setting": {"critical": True, "category": "treatment"},
    "duration_acquaintance": {"critical": False, "category": "treatment"},
    "treatment_type": {"critical": False, "category": "treatment"},

    # The Dilemma
    "main_difficulty": {"critical": True, "category": "dilemma"},
    "related_behaviors": {"critical": False, "category": "dilemma"},
    "impact_daily_function": {"critical": True, "category": "dilemma"},
}


# Critical fields (marked with * in prompt)
CRITICAL_FIELDS = [k for k, v in TEMPLATE_FIELDS.items() if v["critical"]]


@dataclass
class Template:
    """18-field context template for case information."""

    # Therapist Profile
    therapist_role: Optional[str] = None
    years_experience: Optional[str] = None
    area_specialization: Optional[str] = None
    therapist_setting: Optional[str] = None

    # Patient Profile
    patient_age: Optional[str] = None
    patient_gender: Optional[str] = None
    diagnosis: Optional[str] = None
    cultural_background: Optional[str] = None
    marital_status: Optional[str] = None
    educational_framework: Optional[str] = None
    occupational_framework: Optional[str] = None
    hobbies_leisure: Optional[str] = None

    # Treatment Context
    treatment_setting: Optional[str] = None
    duration_acquaintance: Optional[str] = None
    treatment_type: Optional[str] = None

    # The Dilemma
    main_difficulty: Optional[str] = None
    related_behaviors: Optional[str] = None
    impact_daily_function: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def update_from_dict(self, updates: Dict[str, Any]) -> None:
        """Update template fields from dictionary."""
        for key, value in updates.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_filled_count(self) -> int:
        """Count number of filled fields."""
        return sum(1 for v in self.__dict__.values() if v is not None)

    def get_critical_filled_count(self) -> int:
        """Count number of filled critical fields."""
        return sum(
            1 for k in CRITICAL_FIELDS
            if getattr(self, k) is not None
        )

    def get_additional_filled_count(self) -> int:
        """Count number of filled non-critical fields."""
        return self.get_filled_count() - self.get_critical_filled_count()


def evaluate_context(template: Template) -> tuple[bool, str]:
    """
    Context Evaluator: Check if template is sufficiently complete for phase transition.

    Transition Criteria:
    - ALL 5 critical fields filled AND at least 7 additional fields = 12/18 minimum

    Args:
        template: The current template state

    Returns:
        Tuple of (should_transition: bool, status_message: str)
    """
    total_fields = len(TEMPLATE_FIELDS)
    filled_count = template.get_filled_count()
    critical_filled = template.get_critical_filled_count()
    additional_filled = template.get_additional_filled_count()
    total_critical = len(CRITICAL_FIELDS)

    # Check transition criteria
    all_critical_filled = critical_filled == total_critical
    enough_additional = additional_filled >= 7
    min_total_met = filled_count >= 12

    should_transition = all_critical_filled and enough_additional and min_total_met

    # Generate status message
    if should_transition:
        status_msg = (
            f"✓ Context complete: {filled_count}/{total_fields} fields filled "
            f"({critical_filled}/{total_critical} critical, {additional_filled} additional). "
            "Ready for scenario retrieval."
        )
    else:
        missing = []
        if not all_critical_filled:
            missing.append(
                f"{total_critical - critical_filled} critical field(s)"
            )
        if not enough_additional:
            missing.append(
                f"need {7 - additional_filled} more additional field(s)"
            )

        status_msg = (
            f"Context gathering: {filled_count}/{total_fields} fields filled "
            f"({critical_filled}/{total_critical} critical, {additional_filled} additional). "
            f"Missing: {', '.join(missing)}."
        )

    return should_transition, status_msg


def generate_conversation_summary(template: Template) -> str:
    """
    Generate a natural language summary from the template for RAG retrieval.

    Args:
        template: Filled template

    Returns:
        Natural language summary for embedding and retrieval
    """
    parts = []

    # Therapist context
    if template.therapist_role:
        exp = f", {template.years_experience} experience" if template.years_experience else ""
        spec = f", specializing in {template.area_specialization}" if template.area_specialization else ""
        setting = f" working in {template.therapist_setting}" if template.therapist_setting else ""
        parts.append(f"Therapist: {template.therapist_role}{exp}{spec}{setting}")

    # Patient profile
    patient_parts = []
    if template.patient_age:
        patient_parts.append(f"{template.patient_age} year old")
    if template.patient_gender:
        patient_parts.append(template.patient_gender)
    if patient_parts:
        parts.append(f"Patient: {' '.join(patient_parts)}")

    if template.diagnosis:
        parts.append(f"Diagnosis: {template.diagnosis}")

    if template.cultural_background:
        parts.append(f"Cultural background: {template.cultural_background}")

    if template.marital_status:
        parts.append(f"Family structure: {template.marital_status}")

    # Treatment context
    if template.treatment_setting:
        parts.append(f"Setting: {template.treatment_setting}")

    if template.treatment_type:
        parts.append(f"Treatment type: {template.treatment_type}")

    # The dilemma
    if template.main_difficulty:
        parts.append(f"Main challenge: {template.main_difficulty}")

    if template.impact_daily_function:
        parts.append(f"Impact on daily function: {template.impact_daily_function}")

    if template.related_behaviors:
        parts.append(f"Related behaviors: {template.related_behaviors}")

    return "\n".join(parts)
