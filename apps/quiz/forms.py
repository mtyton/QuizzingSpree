from flask_login import current_user
from flask_wtf import Form
from wtforms import (
    FieldList, StringField, SelectField, validators, TextAreaField,
    FormField, BooleanField, SelectMultipleField
)
from wtforms.widgets import Select

from apps.quiz.models import QuizCategory, Quiz, Answer
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


class QuestionSolverForm(Form):

    answer = SelectMultipleField(
        "Answer", validators=[validators.DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        self.question = kwargs.get('obj', None)
        self.content = self.question.content
        super().__init__(*args, **kwargs)
        # This variable defines if current Select Field may
        # have multiple answers
        multiple = False

        if self.question.question_type is QuestionTypeEnum.SELECT_MULTIPLE:
            multiple = True

        self.answer.widget = Select(multiple=multiple)
        # add proper choices to fields
        choices = []
        for answer in self.question.answers:
            choices.append((str(answer.id), answer.content))
        self.answer.choices = choices

    def get_processed_data(self) -> dict:
        return {
            'question': self.question,
            'answers': self.answer.data
        }


class QuizSolverForm(Form):

    def __init__(self, quiz: Quiz, *args, **kwargs):
        kwargs['data'] = {}
        kwargs['data']['questions'] = [q for q in quiz.questions]
        super().__init__(*args, **kwargs)

    def validate(self, extra_validators=None) -> bool:
        """
        This method validates the form, it's done simply by
        validating all subforms
        """
        return self.questions.validate(extra_validators)

    questions = FieldList(
        FormField(QuestionSolverForm, label='Questions'),
        min_entries=0, max_entries=250
    )

    def get_processed_data(self) -> dict:
        return {
            'questions': [
                question.get_processed_data() for question in self.questions
            ]
        }
