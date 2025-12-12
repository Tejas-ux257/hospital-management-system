from django import forms
from doctors.models import AvailabilitySlot


class BookingForm(forms.Form):
    slot_id = forms.IntegerField(widget=forms.HiddenInput())
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Additional Notes (Optional)'
    )
    
    def clean_slot_id(self):
        slot_id = self.cleaned_data['slot_id']
        try:
            slot = AvailabilitySlot.objects.get(id=slot_id)
            if not slot.is_available:
                raise forms.ValidationError("This slot is already booked.")
            if not slot.is_future():
                raise forms.ValidationError("Cannot book past time slots.")
        except AvailabilitySlot.DoesNotExist:
            raise forms.ValidationError("Invalid availability slot.")
        return slot_id

