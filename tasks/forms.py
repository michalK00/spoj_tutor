from django import forms

from tasks.models import UserTask


class EditUserTask(forms.Form):
    def __init__(self, data, **kwargs):
        initial = kwargs.get('initial', {})
        data = {**initial, **data}
        super().__init__(data, **kwargs)

    user_solution = forms.CharField(max_length=UserTask._meta.get_field("user_solution").max_length,
                                    required=False,
                                    widget=forms.Textarea(
                                        attrs={
                                            'rows': '7;'
                                        })
                                    )
    user_note = forms.CharField(max_length=UserTask._meta.get_field("user_note").max_length,
                                required=False,
                                widget=forms.Textarea(
                                    attrs={
                                        'rows': '3;'
                                    })
                                )
