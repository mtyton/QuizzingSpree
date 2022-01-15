import enum


class QuizDifficultyLevelEnum(enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "HARD"


class QuestionTypeEnum(enum.Enum):
    SELECT = "select"
    SELECT_MULTIPLE = "select_multiple"
