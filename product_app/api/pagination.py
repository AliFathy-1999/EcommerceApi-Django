from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'limit'
    max_page_size = 10
    last_page_strings = 'last'
    
class ProductLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10;
    limit_query_param = "limit";
    offset_query_param = "page";
    max_limit=10;