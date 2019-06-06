from django.core.paginator import Paginator


def rec_page(request, obj):
    """
    分页
    :param request:
    :param obj:
    :return:
    """
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 12)
    paginator = Paginator(obj, limit)
    page_obj = paginator.get_page(page)
    return page_obj
