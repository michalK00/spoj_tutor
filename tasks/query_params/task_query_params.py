from ..models import Task, UserTask

QUERY_PARAMS_ORDER = ("search", "status", "source")


class TaskQuery:
    def __init__(self, request):
        self.request = request
        self.params = self._get_params()
        self.params_count = len(self.params)
        self.url = self._build_url()
        self.task_list = self._handle_params()

    def _get_params(self):
        params = []
        for item in self.request.GET.items():
            params.append(item[0])
        return params

    def _build_url(self):
        url = ""
        for param in QUERY_PARAMS_ORDER:
            if param in self.request.GET:
                url += f"&{param}={self.request.GET.get(param)}"
        return url

    def _handle_params(self):
        task_list = Task.objects.all()
        for param in self.params:
            match param:
                case "search":
                    task_list = task_list.filter(title__icontains=self.request.GET.get('search'))
                case "status":
                    if self.request.GET.get('status') == "to-add":
                        user_tasks = UserTask.objects.filter(user_id=self.request.user.id)
                        task_ids = user_tasks.values_list('task_id', flat=True)
                        task_list = task_list.exclude(id__in=task_ids)
                    elif self.request.GET.get('status') == "solved":
                        user_tasks = UserTask.objects.filter(user_id=self.request.user.id).exclude(finished_date=None)
                        task_ids = user_tasks.values_list('task_id', flat=True)
                        task_list = task_list.filter(id__in=task_ids)
                    elif self.request.GET.get('status') == "in-my-problems":
                        user_tasks = UserTask.objects.filter(user_id=self.request.user.id).filter(finished_date=None)
                        task_ids = user_tasks.values_list('task_id', flat=True)
                        task_list = task_list.filter(id__in=task_ids)
                case "source":
                    task_list = task_list.filter(spoj=self.request.GET.get('source'))
        return task_list


class UserTaskQuery:
    def __init__(self, request):
        self.request = request
        self.params = self._get_params()
        self.params_count = len(self.params)
        self.url = self._build_url()
        self.task_list = self._handle_params()

    def _get_params(self):
        params = []
        for item in self.request.GET.items():
            params.append(item[0])
        return params

    def _build_url(self):
        url = ""
        for param in QUERY_PARAMS_ORDER:
            if param in self.request.GET:
                url += f"&{param}={self.request.GET.get(param)}"
        return url

    def _handle_params(self):
        user_tasks = UserTask.objects.all()
        for param in self.params:
            match param:
                case "search":
                    user_tasks = user_tasks.filter(task_id__title__icontains=self.request.GET.get('search'))
                case "status":
                    if self.request.GET.get('status') == "solved":
                        user_tasks = UserTask.objects.filter(user_id=self.request.user.id).exclude(finished_date=None)
                    elif self.request.GET.get('status') == "in-my-problems":
                        user_tasks = UserTask.objects.filter(user_id=self.request.user.id).filter(finished_date=None)
                case "source":
                    user_tasks = user_tasks.filter(task_id__spoj__name=self.request.GET.get('source'))
        return user_tasks
