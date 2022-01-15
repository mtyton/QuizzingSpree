from flask_wtf import Form
from wtforms import (
    FieldList, StringField, SelectField, validators, TextAreaField,
    FormField, BooleanField
)

from apps.quiz.models import QuizCategory
from apps.quiz.taxonomies import QuestionTypeEnum


class AnswerForm(Form):
    content = StringField(
        "Answer content",
        [validators.data_required(), validators.length(max=250)]
    )
    correct = BooleanField(
        u"Answer correctness", [validators.data_required(), ], default=False
    )


class QuestionForm(Form):
    question_type = SelectField(
        u"Question Type", choices=[
            (QuestionTypeEnum.SELECT, QuestionTypeEnum.SELECT),
            (QuestionTypeEnum.SELECT_MULTIPLE, QuestionTypeEnum.SELECT_MULTIPLE),
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
