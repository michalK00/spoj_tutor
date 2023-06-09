from django.test import TestCase
from django.urls import reverse, resolve
from .views import tasks, single_task
from .models import Task


# Create your tests here.
# TODO: fix tests after new model migration (mainly setUp), split tests between files (like in accounts app)

class TasksTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(name="Two sum", source="leetcode",
                                        url="https://leetcode.com/problems/palindrome-linked-list/",
                                        task_content="None")
        url = reverse('tasks')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_tasks_url_resolves_tasks_view(self):
        view = resolve('/tasks/')
        self.assertEquals(view.func, tasks)

    def test_tasks_view_contains_link_to_single_task_page(self):
        single_task_url = reverse('single_task', kwargs={'task_id': self.task.pk})
        self.assertContains(self.response, 'href="{0}"'.format(single_task_url))


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

    # doesn't work
    # def test_single_task_view_not_found_resolves_404_view(self):
    #     view = resolve('/tasks/99')
    #     self.assertEquals(view.func, page_not_found)

    def test_single_task_url_resolves_single_task_view(self):
        view = resolve('/tasks/1/')
        self.assertEquals(view.func, single_task)
