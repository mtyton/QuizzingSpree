from flask_login import current_user
from flask_wtf import Form
from wtforms import (
    FieldList, StringField, SelectField, validators, TextAreaField,
    FormField, BooleanField, SelectMultipleField
)

from apps.quiz.models import QuizCategory, Quiz
from apps.quiz.taxonomies import QuestionTypeEnum


# TODO - create base form class

class AnswerCreationForm(Form):
    content = StringField(
        "Answer content",
        [validators.data_required(), validators.length(max=250)]
    )
    correct = BooleanField(
        u"Answer correctness", default=False
    )

    def get_processed_data(self) -> dict:
        """
        This method returns data processed by form,
        formatted in a way that it'll be provided into QuizFactory.
        """
        return {
            'content': self.content.data,
            'correct': self.correct.data
        }


class QuestionCreationForm(Form):
    question_type = SelectField(
        u"Question Type", choices=[
            (QuestionTypeEnum.SELECT.value, "Select"),
            (QuestionTypeEnum.SELECT_MULTIPLE.value, "Select multiple"),
        ], validators=[validators.data_required(), ]
    )
    content = StringField(
        "Question content",
        [validators.data_required(), validators.length(max=250)]
    )
    answers = FieldList(
        FormField(AnswerCreationForm, label='Answers'),
        min_entries=1, max_entries=6
    )

    def validate(self, extra_validators=None) -> bool:
        valid = super().validate(extra_validators)
        valid = valid & self.answers.validate(extra_validators)
        return valid

    def get_processed_data(self) -> dict:
        """
        This method returns data processed by form,
        formatted in a way that it'll be provided into QuizFactory.
        """
        return {
            'question_type': self.question_type.data,
            'content': self.content.data,
            'answers': [answer.get_processed_data() for answer in self.answers]
        }


class QuizCreationForm(Form):

    title = StringField(
        u'Quiz Title', [validators.data_required(), validators.length(max=150)]
    )

    category = SelectField(
        u'Quiz category', [validators.data_required(), ]
    )

    description = TextAreaField(
        u"Quiz description",
        [validators.data_required(), validators.length(max=150)]
    )

    questions = FieldList(
        FormField(QuestionCreationForm, label='Questions'),
        min_entries=1, max_entries=250
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [
            (q.id, q.category_name)
            for q in QuizCategory.query.order_by('category_name')
        ]

    def validate(self, extra_validators=None) -> bool:
        valid = super().validate(extra_validators)
        valid = valid & self.questions.validate(extra_validators)
        return valid

    def get_processed_data(self) -> dict:
        """
        This method returns data processed by form,
        formatted in a way that it'll be provided into QuizFactory.
        """
        return {
            'title': self.title.data,
            'author_id': current_user.id,
            'category_id': self.category.data,
            'description': self.description.data,
            'questions': [
                question.get_processed_data() for question in self.questions
            ]
        }


# solver forms


class BaseQuestionSolverForm(Form):

    answer = None

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        self.content = question.content
        super().__init__(*args, **kwargs)
        self.answer.choices = question.get_all_answers()


# now we have to implement each specific question type

class SelectQuestionSolverForm(BaseQuestionSolverForm):

    answer = SelectField(
        u'Answer', [validators.data_required(), ]
    )


class SelectMultipleQuestionSolverForm(BaseQuestionSolverForm):

    answer = SelectMultipleField(
        u'Answers', [validators.data_required(), ]
    )


class QuizSolverForm(Form):

    question_form_type_map = {
        QuestionTypeEnum.SELECT: SelectQuestionSolverForm,
        QuestionTypeEnum.SELECT_MULTIPLE: SelectMultipleQuestionSolverForm,
    }

    def _initialize_quiz(self, quiz: Quiz) -> None:
        for question in quiz.questions:
            form_class = self.question_form_type_map[question.question_type]
            self.questions.entries.append(
                form_class(**{'question': question})
            )
        print(self.questions.entries)

    def __init__(self, quiz: Quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._initialize_quiz(quiz)

    questions = FieldList(
        FormField(BaseQuestionSolverForm, label='Questions'),
        min_entries=0, max_entries=250
    )
