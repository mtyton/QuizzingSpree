from flask import render_template, redirect, url_for, flash
from flask.views import MethodView
from flask.typing import ResponseReturnValue, t
from typing import List

from apps.base.permissions import BasePermission


class BaseTemplateRenderMixin(object):

    template_name = None

    def get_context(self) -> dict:
        """
        This method should simply returns page context.
        :return:
        """
        return {}

    def get(self):
        """
        Basic get method, it'll always render the defined template.
        If template has not been defined, it'll rise an error.
        :return:
        """
        assert self.template_name is not None
        return render_template(self.template_name, **self.get_context())


class BasePermissionCheckMethodView(BaseTemplateRenderMixin, MethodView):

    # TODO - allow define this in config
    DEFAULT_PERMISSIONS_FAIL_URL_NAME: str = 'website.home'

    # permissions lack messages
    DEFAULT_PERMISSION_LACK_MESSAGE: str = "You are currently not " \
                                           "allowed to enter this view"
    permission_lack_message: str = None

    permissions_fail_url_name: str = None
    permissions: List[BasePermission] = []

    def _check_permissions(self) -> bool:
        """
        This method is simply invoking, validation method of each permission.
        :return:
        """
        for permission in self.permissions:
            if not permission.check_permission():
                return False
        return True

    def _get_fail_redirection(self):
        """
        This method provides the proper redirection response in case, any
        of permissions check have failed.
        :return:
        """
        if not self.permission_lack_message:
            self.permission_lack_message = self.DEFAULT_PERMISSION_LACK_MESSAGE

        flash(self.permission_lack_message, "error")

        try:
            assert self.permissions_fail_url_name is not None
        except AssertionError:
            return redirect(
                url_for(self.DEFAULT_PERMISSIONS_FAIL_URL_NAME), code=301
            )
        else:
            return redirect(url_for(self.permissions_fail_url_name), code=301)

    def dispatch_request(
            self, *args: t.Any, **kwargs: t.Any
    ) -> ResponseReturnValue:
        """
        By overriding the dispatch_request method, we're allowed to
        check permissions before default method dispatching, will begin.
        :param args:
        :param kwargs:
        :return:
        """

        if not self._check_permissions():
            return self._get_fail_redirection()

        return super().dispatch_request(*args, **kwargs)
