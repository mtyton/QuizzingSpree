from flask import Blueprint

from apps.base.views import BasePermissionCheckMethodView


bp = Blueprint('quiz', __name__)


class QuizListView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_list.html"


bp.add_url_rule('/quiz-list', view_func=QuizListView.as_view('quiz_list'))
