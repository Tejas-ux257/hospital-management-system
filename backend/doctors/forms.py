from django import forms
from .models import DoctorProfile, AvailabilitySlot
from django.utils import timezone


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'bio', 'years_of_experience']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class AvailabilitySlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if date and start_time and end_time:
            # Check if date is in the future
            if date < timezone.now().date():
                raise forms.ValidationError("Date must be in the future.")
            
            # Check if end_time is after start_time
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data

