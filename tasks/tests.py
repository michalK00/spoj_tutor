from django.test import TestCase
from django.urls import reverse, resolve
from .views import tasks, single_task, page_not_found
from .models import Task


# Create your tests here.


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_tasks_url_resolves_tasks_view(self):
        view = resolve('/tasks/')
        self.assertEquals(view.func, tasks)


class TaskTests(TestCase):
    def setUp(self):
        Task.objects.create(name="Two sum", source="leetcode",
                            url="https://leetcode.com/problems/palindrome-linked-list/", task_content="None")

    def test_single_task_view_success_status_code(self):
        url = reverse('single_task', kwargs={'task_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_single_task_view_not_found_status_code(self):
        url = reverse('single_task', kwargs={'task_id': 100})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_single_task_view_not_found_resolves_404_view(self):
        view = resolve('/tasks/99')
        self.assertEquals(view.func, page_not_found)

    def test_single_task_url_resolves_single_task_view(self):
        view = resolve('/tasks/1')
        self.assertEquals(view.func, single_task)

