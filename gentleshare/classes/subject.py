from enum import Enum


class Subject(Enum):
    """Enum class for the subjects that can be taught in the school."""

    MATHS = "maths"
    FRENCH = "french"
    SPANISH = "spanish"
    ENGLISH = "english"
    PHYSICS = "physics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    HISTORY = "history"
    GEOGRAPHY = "geography"
    ECONOMY = "economy"

    @property
    def display_name(self) -> str:
        return {
            Subject.MATHS: "Maths",
            Subject.FRENCH: "Français",
            Subject.SPANISH: "Espagnol",
            Subject.ENGLISH: "Anglais",
            Subject.PHYSICS: "Physique",
            Subject.CHEMISTRY: "Chimie",
            Subject.BIOLOGY: "Biologie",
            Subject.HISTORY: "Histoire",
            Subject.GEOGRAPHY: "Géographie",
            Subject.ECONOMY: "Économie",
        }[self]
