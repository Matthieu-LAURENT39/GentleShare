from enum import Enum


class EducationLevel(Enum):
    """The various school education levels"""

    ELEMENTARY = "elementary"
    MIDDLE = "middle"
    HIGH = "high"
    UNIVERSITY = "university"

    @property
    def display_name(self) -> str:
        """The display name of the education level"""
        return {
            EducationLevel.ELEMENTARY: "École primaire",
            EducationLevel.MIDDLE: "Collège",
            EducationLevel.HIGH: "Lycée",
            EducationLevel.UNIVERSITY: "Université",
        }[self]
