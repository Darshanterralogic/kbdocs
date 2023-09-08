from django.contrib.auth import login
from django.db.models import Count

from rest_framework_simplejwt.tokens import RefreshToken


def user_authenticate(emp_id, email):
    from core.models import User
    user = User.objects.filter(
        emp_id=emp_id.strip(),
        email=email.strip()
    ).first()
    return user or None


def user_login(request, user):
    """
    Accepts request and user to login()
    Returns a JWT Token
    """
    login(request, user)
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def get_next_unique_model_value(string_to_truncate, model, field, max_length=100, truncate_count=0, iteration=0):
    """
    This method will check a given DB model for a
    unique value for a given field.
    If the value is not unique, an incremented value
    will be applied until a unique field value is found.
    """
    truncated_string = string_to_truncate[:max_length - truncate_count]

    # Only need to check the base string on the first try
    if iteration == 0:
        # If this string is unique, we are done
        query_filter = {field: truncated_string}
        record_count = model.objects.filter(**query_filter).count()
        if record_count == 0:
            return truncated_string

    # If the truncated string is less than max_length characters
    # We got here due to adding a digit not being unique
    if len(truncated_string) < max_length and iteration > 0:
        truncated_string = truncated_string[:max_length - len(str(iteration))] + str(iteration)

    else:
        # The string is not unique, trim a character for each significant digit in count
        query_filter = {f"{field}__istartswith": truncated_string}
        record_count = model.objects.filter(**query_filter).count()
        truncate_count = len(str(record_count))

        # Is the truncated name plus the count digit unique
        truncated_string = truncated_string[:max_length - truncate_count] + str(record_count)

    # If this string is unique, we are done
    query_filter = {f"{field}__istartswith": truncated_string}
    record_count = model.objects.filter(**query_filter).count()
    if record_count == 0:
        return truncated_string

    # If there are more records than we have digits for
    if len(str(record_count)) > truncate_count:
        truncate_count += 1
    iteration += 1
    return get_next_unique_model_value(string_to_truncate, model, field, max_length, truncate_count, iteration)


def base_context(request):
    is_authed = hasattr(request, "user") and hasattr(request.user, "email") and hasattr(request.user, "emp_id")
    
    context = dict(
        LOGGED_IN   = False,
        AUTHED = "true" if is_authed else "false",
    )

    if request.user.is_authenticated:
        context['LOGGED_IN'] = True
        context['request'] = request

    context['LOGGED_IN'] = str(context['LOGGED_IN']).lower()
    return context


def get_template_context(request, template_name, context, **kwargs):
    template_context = {}

    if template_name == "index.html":
        from core.models import KBDocs
        template_context['header_title'] = "Dashboard"
        print ('index')
        template_context['kbdocs'] = KBDocs.objects.values('tools').order_by('tools').annotate(count=Count('tools'))
        template_context['all_kbdocs'] = KBDocs.objects.all()
    elif template_name == "viewkbdocs.html":
        from core.models import KBDocs
        template_context['header_title'] = "View KB Docs"
        template_context['kbdocs'] = KBDocs.objects.filter(user=request.user)
    elif template_name == "viewdetailkbdoc.html":
        from core.models import KBDocs
        kbdoc_id = kwargs.get('kbdocid')
        template_context['header_title'] = "View Detail KB Docs"
        template_context['kbdoc'] = KBDocs.objects.filter(id=kbdoc_id).first()
    elif template_name == "editdetailkbdoc.html":
        from core.models import KBDocs
        kbdoc_id = kwargs.get('kbdocid')
        template_context['header_title'] = "Edit Detail KB Docs"
        template_context['kbdoc'] = KBDocs.objects.filter(id=kbdoc_id).first()

    return {**context, **template_context}
