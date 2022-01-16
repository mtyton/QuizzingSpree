from flask import Blueprint, Response, redirect, url_for, request

from apps.base.views import BasePermissionCheckMethodView
from apps.quiz.forms import QuizCreationForm
from apps.quiz.quiz_factory import QuizFactory


bp = Blueprint('quiz', __name__)


class QuizListView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_list.html"


class QuizCreatorReadView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_create.html"

    def get_context(self) -> dict:
        return {
            'form': QuizCreationForm()
        }

    def post(self) -> Response:
        # TODO - add permission check
        print(request.form)
        form = QuizCreationForm(request.form)
        processed_data = form.get_processed_data()

        factory = QuizFactory()
        # quiz = factory.create_quiz(processed_data)

        return redirect(url_for('website.home'), code=302)


bp.add_url_rule('/quiz-list', view_func=QuizListView.as_view('quiz_list'))
bp.add_url_rule(
    '/quiz-create', view_func=QuizCreatorReadView.as_view('quiz_create')
)
