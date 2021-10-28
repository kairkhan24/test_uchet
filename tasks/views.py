import redis
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

from .models import Task
from .serializers import TaskListSerializer, TaskRetrieveSerializer, TaskCreateSerializer

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        if self.action == 'create':
            return TaskCreateSerializer
        return TaskRetrieveSerializer


class TaskExecuteView(APIView):

    @staticmethod
    def get(request, pk):
        try:
            task = Task.objects.get(id=pk)
        except Task.DoesNotExist:
            return Response({'info': f'Task with id {pk} does not exist.'}, status=404)
        task.is_done = not task.is_done
        task.save()
        emails = r.get('emails')
        if emails:
            emails.append(request.user.email)
            r.set('emails', emails)
        else:
            emails = []
            emails.append(request.user.email)
            r.set('emails', emails)
        serializer = TaskRetrieveSerializer(task, many=False)
        return Response(serializer.data, status=200)
