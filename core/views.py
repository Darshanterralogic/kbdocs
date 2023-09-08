import json

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from core.utils import (
    user_authenticate, user_login,
    base_context, get_template_context
)
from core.serializers import UserSerializer
from core.models import User, KBDocs


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


# NOTE: All the APIs can be squashed to lesser classes with ViewSets


class UserLoginApi(APIView):
    authentication_classes = ()
    permission_classes = ()

    error_codes = dict(
        e01="Missing required field: Employee ID",
        e02="Missing required field: Email",
        e03="Missing required field: password",
        e04="The Employee ID you provided is incorrect",
        e05="The Email you provided is incorrect",
        e99="Unknown error"
    )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if hasattr(request, "data") and request.data:
            post_data = request.data
        elif request.POST:
            post_data = request.POST
        else:
            post_data = {}

        error_code = "e99"

        if 'emp_id' not in post_data:
            error_code = "e01"
            return Response(dict(success=False, error=self.error_codes[error_code]))
        if "email" not in post_data:
            error_code = "e02"
            return Response(dict(success=False, error=self.error_codes[error_code]))
        if "password" not in post_data:
            error_code = "e03"
            return Response(dict(success=False, error=self.error_codes[error_code]))

        emp_id = request.data.get('emp_id')
        if not emp_id:
            return Response(dict(success=False, error="Employee ID cannot be empty"))

        email = request.data.get('email')
        if not email:
            return Response(dict(success=False, error="Email cannot be empty"))

        password = request.data.get('password')
        if not password:
            return Response(dict(success=False, error="Password cannot be empty"))

        user = user_authenticate(
            emp_id=emp_id, email=email
        )
        if not user:
            return Response(
                dict(success=False, error="User not found")
            )

        token = user_login(request, user)
        return Response(dict(success=True, tokens=token, user=UserSerializer(user).data))


class UserCreateApi(APIView):
    authentication_classes = ()
    permission_classes = ()

    error_codes = dict(
        e01="Missing required field: Employee ID",
        e02="Missing required field: Email",
        e03="Missing required field: password",
        e04="The Employee ID you provided is incorrect",
        e05="The Email you provided is incorrect",
        e06="Missing required field: First Name",
        e07="Missing required field: Last Name",
        e99="Unknown error"
    )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if hasattr(request, "data") and request.data:
            post_data = request.data
        elif request.POST:
            post_data = request.POST
        else:
            post_data = {}

        error_code = "e99"

        if 'emp_id' not in post_data:
            error_code = "e01"
            return Response(dict(success=False, error=self.error_codes[error_code]))
        if "email" not in post_data:
            error_code = "e02"
            return Response(dict(success=False, error=self.error_codes[error_code]))
        if "password" not in post_data:
            error_code = "e03"
            return Response(dict(success=False, error=self.error_codes[error_code]))
        if "first_name" not in post_data:
            error_code = "e06"
            return Response(dict(success=False, error=self.error_codes[error_code]))
        if "last_name" not in post_data:
            error_code = "e07"
            return Response(dict(success=False, error=self.error_codes[error_code]))

        emp_id = request.data.get('emp_id')
        if not emp_id:
            return Response(dict(success=False, error="Employee ID cannot be empty"))

        email = request.data.get('email')
        if not email:
            return Response(dict(success=False, error="Email cannot be empty"))

        password = request.data.get('password')
        if not password:
            return Response(dict(success=False, error="Password cannot be empty"))
        
        first_name = request.data.get('first_name')
        if not first_name:
            return Response(dict(success=False, error="First name cannot be empty"))
        
        last_name = request.data.get('last_name')
        if not last_name:
            return Response(dict(success=False, error="Last name cannot be empty"))

        try:
            user = User.objects.create(
                first_name=first_name, last_name=last_name, email=email,
                emp_id=emp_id
            )
            user.set_password(password)
            user.save()
        except Exception:
            return Response(dict(success=False, error="User already exists"))

        return Response(dict(success=True))


class UserLogoutApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        response = Response()

        for k, _ in request.COOKIES.items():
            response.delete_cookie(k)
        return response


class KBDocsApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user_id'] = request.user.id
        data['name'] = f"KB_{data['tools']}_{KBDocs.objects.count()+1}"
        KBDocs.objects.create(**data)
        return Response(dict(success=True))

    def put(self, request, *args, **kwargs):
        kbdoc_id = kwargs.get('pk')
        KBDocs.objects.filter(id=kbdoc_id).update(**request.data)
        return Response(dict(success=True))


class BaseTemplateView(TemplateView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    whitelisted_templates = []

    def dispatch(self, request, *args, **kwargs):
        template_name = self.get_template_names()[0]
        # Allow whitelisted urls through without a permission check
        if template_name not in self.whitelisted_templates:
            for permission_class in self.permission_classes:
                if not permission_class().has_permission(request, self):
                    error_message = json.dumps(dict(error_msg='Unauthorized request'))
                    print(
                        f"Unauthorized request to {template_name}.  Consider adding to whitelisted_templates"
                    )
                    # return HttpResponseUnauthorized(error_message)
                    return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        self.is_404 = False
    
    def get_context_data(self, **kwargs):

        super_context = super().get_context_data(**kwargs)
        base_content = base_context(self.request)

        context = {**super_context, **base_content}

        template_name = self.get_template_names()[0]
        context = get_template_context(self.request, template_name, context, **kwargs)
        if not context:
            self.is_404 = True
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.is_404:
            response_kwargs['status'] = 404
        return super().render_to_response( context, **response_kwargs)


#NOTE: We can add a single custom view to load all the templates based on url kwargs

class IndexView(BaseTemplateView):
    template_name = 'index.html'

    # List of views that don't require authentication
    whitelisted_templates = ['index.html']


class AddKBDocsView(BaseTemplateView):
    template_name = 'addkbdocs.html'


class ViewKBDocsView(BaseTemplateView):
    template_name = 'viewkbdocs.html'


class DynamicTemplateView(BaseTemplateView):
    """
    This will parse the template path out of the URL
    and assign the template name
    """

    # List of views that don't require authentication
    whitelisted_templates = ['signup.html']
    template_names = []

    def get_template_names(self):
        if self.template_names:
            return self.template_names

        # If get_context_data triggered a 404
        if self.is_404:
            self.is_404 = True
            return ['404.html']
        
        template_name = self.kwargs.get('template')

        if not template_name:
            return ['404.html']

        if not template_name.endswith('.html'):
            template_name = f"{template_name}.html"

        # Store the template so when this function reloads we don't have to redo all the logic
        self.template_names = [template_name]
        return self.template_names
