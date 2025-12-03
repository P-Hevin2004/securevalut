from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from .models import SharedFile, Group

MAX_UPLOAD_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

class FileUploadForm(forms.ModelForm):
    allowed_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
        help_text='Select users who can access this file'
    )
    allowed_groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
        help_text='Select groups who can access this file'
    )
    
    class Meta:
        model = SharedFile
        fields = ['title', 'description', 'file', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter file title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter file description (optional)'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Exclude current user from allowed_users list
            self.fields['allowed_users'].queryset = User.objects.exclude(id=user.id)
            # Only show groups the user is a member of or created
            self.fields['allowed_groups'].queryset = Group.objects.filter(
                Q(created_by=user) | Q(members=user)
            ).distinct()
        
        # Set initial values if editing
        if self.instance and self.instance.pk:
            self.fields['allowed_users'].initial = self.instance.allowed_users.all()
            self.fields['allowed_groups'].initial = self.instance.allowed_groups.all()
    
    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file and uploaded_file.size > MAX_UPLOAD_SIZE_BYTES:
            max_mb = MAX_UPLOAD_SIZE_BYTES // (1024 * 1024)
            raise forms.ValidationError(
                f'File size must be under {max_mb} MB.'
            )
        return uploaded_file
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Save many-to-many relationships
            self.save_m2m()
        return instance

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
