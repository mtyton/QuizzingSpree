
from flask import Blueprint
from flask.views import MethodView

from apps.base.views import BaseTemplateRenderMixin


bp = Blueprint('website', __name__)


class IndexView(BaseTemplateRenderMixin, MethodView):

    methods = ["GET"]
    template_name = "base/index.html"


bp.add_url_rule('/', view_func=IndexView.as_view('home'))
