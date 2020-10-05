from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import (
    TextInput,
    EmailInput,
    ChoiceWidget
)

from mptt.forms import TreeNodeChoiceField

from knox.models import AuthToken

from papermerge.core.models import (
    User,
    Automate,
    Folder,
    Access
)


class ControlForm(forms.ModelForm):
    """
    Adds to following widgets css class 'form-control':
        * TextInput
        * EmailInput
        * ChoiceWidget
        * TreeNodeChoiceField
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(
                visible.field.widget,
                (TextInput, EmailInput, ChoiceWidget, TreeNodeChoiceField)
            ):
                visible.field.widget.attrs['class'] = 'form-control'


class AutomateForm(ControlForm):

    class Meta:
        model = Automate

        fields = (
            'name',
            'match',
            'matching_algorithm',
            'is_case_sensitive',
            'dst_folder',
            'extract_page'
        )
        field_classes = {
            'dst_folder': TreeNodeChoiceField,
        }

    def __init__(self, *args, **kwargs):
        # first get rid of custom arg
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)

        if instance:
            user = instance.user

        if user:
            # Provide user a choice of all folder he/she has
            # READ access to. User might have access to folder he is not
            # the owner of.
            # Exclude folder - inbox
            all_folders = Folder.objects.exclude(
                title=Folder.INBOX_NAME
            )
            folder_choice_ids = []

            for folder in all_folders:
                if user.has_perm(Access.PERM_READ, folder):
                    folder_choice_ids.append(folder.id)

            self.fields['dst_folder'].queryset = Folder.objects.filter(
                id__in=folder_choice_ids
            )

class UserFormWithoutPassword(ControlForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'user_permissions',
            'is_superuser',
            'is_staff',
            'is_active',
        )


class UserFormWithPassword(UserFormWithoutPassword):

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        strip=True,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        strip=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'groups',
            'is_superuser',
            'is_staff',
            'is_active',
        )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        try:
            validate_password(password2, self.instance)
        except forms.ValidationError as error:
            self.add_error('password2', error)
        return password2


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = (
            'name',
        )


class AuthTokenForm(forms.ModelForm):
    """
    Let user choose number of hours until token expires
    """
    hours = forms.IntegerField(
        required=True,
        initial=4464,  # ~ 6 months
        help_text=_(
            "Number of hours this token will be valid (4464 hours ~ 6 months)"
        ),
    )

    class Meta:
        model = AuthToken
        fields = ('hours',)
