import django_filters
from .models import Message, Conversation  # Ensure Conversation is imported

class MessageFilter(django_filters.FilterSet):
    # Date range filters
    start_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="timestamp", lookup_expr='lte')
    
    # Custom filter for the 'conversation' field if it's a ForeignKey in Message model
    conversation = django_filters.ModelChoiceFilter(queryset=Conversation.objects.all())

    class Meta:
        model = Message
        fields = ['start_date', 'end_date']  # Removed 'conversation' from here
