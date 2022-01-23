from flask import (
    Blueprint, Response, redirect, url_for, request,
    flash
)

from apps.base.views import (
    BasePermissionCheckMethodView, PostFailureRenderMixin
)
from apps.quiz.forms import QuizCreationForm, QuizSolverForm
from apps.quiz.quiz_factory import QuizFactory
from apps.quiz.models import Quiz
from apps.auth.permissions import IsAuthenticatedPermission


bp = Blueprint('quiz', __name__)


class QuizListView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_list.html"


class QuizSolverView(BasePermissionCheckMethodView):

    template_name = "quiz/quiz_solve.html"
    permissions = [IsAuthenticatedPermission(), ]

    def get_context(self, *args, **kwargs) -> dict:
        quiz = Quiz.query.filter_by(id=kwargs.get('quiz_id')).first()
        form = QuizSolverForm(quiz=quiz)
        return {
            'quiz': quiz,
            'form': form
        }

    def post(self, *args, **kwargs):
        quiz = Quiz.query.filter_by(id=kwargs.get('quiz_id')).first()
        form = QuizSolverForm(quiz=quiz, formdata=request.form)
        if form.validate():
            data = form.get_processed_data()

        # send this data to tutor, and redirect user


class QuizCreatorReadView(
    PostFailureRenderMixin, BasePermissionCheckMethodView
):

    template_name = "quiz/quiz_create.html"

    permissions_fail_url_name = "auth.login"
    permission_lack_message = "You have to be logged in to create a quiz"
    permissions = [IsAuthenticatedPermission(), ]

    def get_context(self, *args, **kwargs) -> dict:
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
bp.add_url_rule(
    '/quiz-solve/<quiz_id>/', view_func=QuizSolverView.as_view('quiz_solve')
)
