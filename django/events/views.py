from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from .models import Event, EventParticipation
from django.db import IntegrityError
from django.utils import timezone

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.all().order_by('date')
        print(f"Total events in database: {queryset.count()}")  # Debug print
        
        # Print each event's details for debugging
        for event in queryset:
            print(f"Event: {event.title}, Date: {event.date}, Is Virtual: {event.is_virtual}")
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.request.user, 'alumni'):
            # Get events where the user is participating - Fixed the query
            context['participating_events'] = Event.objects.filter(
                event_participations__alumni=self.request.user.alumni
            )
        else:
            context['participating_events'] = Event.objects.none()
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    login_url = 'account_login'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and hasattr(self.request.user, 'alumni'):
            context['is_participating'] = EventParticipation.objects.filter(
                event=self.object,
                alumni=self.request.user.alumni
            ).exists()
            if context['is_participating']:
                context['participation'] = EventParticipation.objects.get(
                    event=self.object,
                    alumni=self.request.user.alumni
                )
        return context

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        if not hasattr(request.user, 'alumni'):
            messages.error(request, 'Only alumni can register for events.')
            return redirect('events:detail', pk=event.pk)

        if event.is_full():
            messages.error(request, 'Sorry, this event is already full.')
            return redirect('events:detail', pk=event.pk)
            
        try:
            EventParticipation.objects.create(
                event=event,
                alumni=request.user.alumni,
                attendance_mode=request.POST.get('attendance_mode', 'in_person')
            )
            messages.success(request, f'You have successfully registered for {event.title}!')
        except IntegrityError:
            messages.warning(request, 'You are already registered for this event.')
        
        return redirect('events:detail', pk=event.pk)



class EventCreateView(UserPassesTestMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'description', 'date', 'location', 'is_virtual']
    success_url = reverse_lazy('events:list')

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

class EventDeleteView(UserPassesTestMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('events:list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Event deleted successfully!')
        return super().delete(request, *args, **kwargs)

# New views for event participation
class EventParticipationView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        attendance_type = request.POST.get('attendance_type')
        
        if attendance_type not in ['virtual', 'in_person']:
            messages.error(request, 'Invalid attendance type')
            return redirect('events:detail', pk=pk)
            
        # Create or update participation
        participation, created = EventParticipation.objects.get_or_create(
            event=event,
            alumni=request.user.alumni,
            defaults={'attendance_type': attendance_type}
        )

class EventParticipationCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        EventParticipation.objects.filter(
            event=event,
            user=request.user.alumni
        ).delete()
        messages.success(request, 'Event participation cancelled successfully!')
        return redirect('events:detail', pk=pk)