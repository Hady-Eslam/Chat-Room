from rest_framework.pagination import PageNumberPagination


class BasePaginator(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class RoomsPaginator(BasePaginator):
    pass
    
class MembersPaginator(BasePaginator):
    pass

class MessagesPaginator(BasePaginator):
    pass
