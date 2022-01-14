import enum


class QuizDifficultyLevelEnum(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "HARD"


class QuestionTypeEnum(str, enum.Enum):
    SELECT = "select"
    SELECT_MULTIPLE = "select_multiple"
