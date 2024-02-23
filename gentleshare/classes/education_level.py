from enum import Enum


class EducationLevel(Enum):
    """The various school education levels"""

    ELEMENTARY = "elementary"
    MIDDLE = "middle"
    HIGH = "high"
    UNIVERSITY = "university"

    @property
    def display_name(self) -> str:
        return {
            EducationLevel.ELEMENTARY: "Elementary school",
            EducationLevel.MIDDLE: "Middle school",
            EducationLevel.HIGH: "High school",
            EducationLevel.UNIVERSITY: "University",
        }[self]
