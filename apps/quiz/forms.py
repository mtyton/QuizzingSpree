from flask_login import current_user
from flask_wtf import Form
from wtforms import (
    FieldList, StringField, SelectField, validators, TextAreaField,
    FormField, BooleanField
)

from apps.quiz.models import QuizCategory
from apps.quiz.taxonomies import QuestionTypeEnum


# TODO - create base form class

class AnswerForm(Form):
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


class QuestionForm(Form):
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
        FormField(AnswerForm, label='Answers'),
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
        FormField(QuestionForm, label='Questions'),
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
