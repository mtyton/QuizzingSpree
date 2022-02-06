from flask import (
    Blueprint, Response, redirect, url_for, request,
    flash
)
from werkzeug.datastructures import ImmutableDict
from apps.base.views import (
    BasePermissionCheckMethodView, PostFailureRenderMixin
)
from apps.quiz.forms import QuizCreationForm, QuizSolverForm
from apps.quiz.quiz_factory import QuizFactory
from apps.auth.permissions import IsAuthenticatedPermission
from apps.quiz.models import Quiz
from apps.quiz.evaluator import QuizEvaluator


bp = Blueprint('quiz', __name__)


class QuizListView(BasePermissionCheckMethodView):
    QUIZZES_PER_PAGE = 2
    template_name = "quiz/quiz_list.html"

    def get_context(self) -> dict:
        page = request.args.get('page', default=1, type=int)
        pagination = Quiz.query.paginate(page, self.QUIZZES_PER_PAGE)

        return {
            'pagination': pagination,
        }


class QuizSolverView(PostFailureRenderMixin, BasePermissionCheckMethodView):

    template_name = "quiz/quiz_solve.html"
    permissions = [IsAuthenticatedPermission(), ]

    def get_context(self, *args, **kwargs) -> dict:
        quiz = Quiz.query.filter_by(id=kwargs.get('quiz_id')).first()
        form = QuizSolverForm(quiz=quiz)
        return {
            'quiz': quiz,
            'form': form
        }

    def _preprocess_form_data(self, data):
        new_data = {}
        for key, value in data.items():
            new_data[key] = int(value)
        return ImmutableDict(
            [(key, value) for key, value in new_data.items()]
        )

    def post(self, *args, **kwargs):
        quiz = Quiz.query.filter_by(id=kwargs.get('quiz_id')).first()
        # fromdata = self._preprocess_form_data(request.form)
        form = QuizSolverForm(quiz=quiz, formdata=request.form)
        if not form.validate():
            flash("Something went wrong during validation!", "error")
            return self._unsuccessful_post_response({'form': form})

        data = form.get_processed_data()
        QuizEvaluator.evaluate(quiz, data)
        flash("You have successfully finished the quiz!", "success")
        return redirect(url_for("auth.my_account"))


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
