from flask import Blueprint

from apps.base.views import BasePermissionCheckMethodView
from apps.quiz.forms import QuizCreationForm


bp = Blueprint('quiz', __name__)


class QuizListView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_list.html"


class QuizCreatorReadView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_create.html"

    def get_context(self) -> dict:
        return {
            'form': QuizCreationForm()
        }


bp.add_url_rule('/quiz-list', view_func=QuizListView.as_view('quiz_list'))
bp.add_url_rule(
    '/quiz-create', view_func=QuizCreatorReadView.as_view('quiz_create')
)
