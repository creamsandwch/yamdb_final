from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """Миксин для возврата группы объектов, создания объекта
    и удаления объекта.
    """
    pass
