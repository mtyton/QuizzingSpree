from flask import (
    Blueprint, Response, redirect, url_for, request,
    flash
)

from apps.base.views import (
    BasePermissionCheckMethodView, PostFailureRenderMixin
)
from apps.quiz.forms import QuizCreationForm
from apps.quiz.quiz_factory import QuizFactory
from apps.auth.permissions import IsAuthenticatedPermission
from apps.quiz.models import Quiz


bp = Blueprint('quiz', __name__)


class QuizListView(BasePermissionCheckMethodView):
    QUIZZES_PER_PAGE = 2
    template_name = "quiz/quiz_list.html"

    def get_context(self) -> dict:
        quizzes = Quiz.query.all()
        max_page = int(len(quizzes) / self.QUIZZES_PER_PAGE)
        page = request.args.get('page', default=1, type=int)

        # Validate page number.
        page = max(1, page)
        page = min(max_page, page)
        first_quiz = (page - 1) * self.QUIZZES_PER_PAGE
        quizzes = quizzes[first_quiz:first_quiz + self.QUIZZES_PER_PAGE]

        return {
            'quizzes': quizzes,
            'pages': range(1, max_page + 1),
            'currentPage': page,
            'maxPage': max_page,
        }


class QuizCreatorReadView(
    PostFailureRenderMixin, BasePermissionCheckMethodView
):

    template_name = "quiz/quiz_create.html"

    permissions_fail_url_name = "auth.login"
    permission_lack_message = "You have to be logged in to create a quiz"
    permissions = [IsAuthenticatedPermission(), ]

    def get_context(self) -> dict:
        return {
            'form': QuizCreationForm()
        }

    def post(self) -> Response:
        form = QuizCreationForm(request.form)
        processed_data = form.get_processed_data()
        if not form.validate():
            flash("Something went wrong, check your form", "errors")
            return self._unsuccessful_post_response({'form': form})

        factory = QuizFactory()

        quiz = factory.create_quiz(processed_data)
        if not quiz and factory.errors:
            for error in factory.errors:
                # TODO add assign error to field
                flash(error.message, "errors")

            return self._unsuccessful_post_response({'form': form})

        flash(f"You quiz {quiz} has been successfully created", "success")
        return redirect(url_for('website.home'), code=302)


bp.add_url_rule('/quiz-list', view_func=QuizListView.as_view('quiz_list'))
bp.add_url_rule(
    '/quiz-create', view_func=QuizCreatorReadView.as_view('quiz_create')
)
