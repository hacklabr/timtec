from .models import Answer
from .serializers import AnswerSerializer
from rest_framework import viewsets


class AnswerViewSet(viewsets.ModelViewSet):
    model = Answer
    serializer_class = AnswerSerializer
    filter_fields = ('activity', 'user',)

    def pre_save(self, obj):
        obj.user = self.request.user

    def get_queryset(self):
        return Answer.objects.filter(user=self.request.user)
