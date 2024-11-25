from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, UpdateView, ListView, DetailView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from .forms import AlumniSignUpForm, AlumniProfileForm, LoginForm
from .models import Alumni
from events.models import Event, EventParticipation

def signup_view(request):
    if request.method == 'POST':
        form = AlumniSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_alumni = True
            user.save()
            
            Alumni.objects.create(
                user=user,
                graduation_year=form.cleaned_data['graduation_year'],
                degree=form.cleaned_data['degree']
            )
            
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('alumni:dashboard')
    else:
        form = AlumniSignUpForm()
    return render(request, 'alumni/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('alumni:dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'alumni/login.html', {'form': form})

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'alumni/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if hasattr(self.request.user, 'alumni'):
            # User participations
            user_participations = EventParticipation.objects.filter(
                alumni=self.request.user.alumni
            )
            
            # Basic statistics
            context['registered_events_count'] = user_participations.filter(
                event__date__gte=timezone.now()
            ).count()
            context['participated_events_count'] = user_participations.filter(
                event__date__lt=timezone.now()
            ).count()
            
            # Upcoming events
            context['upcoming_events'] = Event.objects.filter(
                date__gte=timezone.now()
            ).prefetch_related('event_participations').order_by('date')[:5]
            
            # User's recent events
            context['my_events'] = user_participations.select_related('event').order_by('-event__date')[:5]

            # Chart Data: Event Participation by Month
            six_months_ago = timezone.now() - timedelta(days=180)
            monthly_participation = EventParticipation.objects.filter(
                event__date__gte=six_months_ago
            ).annotate(
                month=TruncMonth('event__date')
            ).values('month').annotate(
                count=Count('id')
            ).order_by('month')

            # Format data for Chart.js
            context['chart_labels'] = [item['month'].strftime('%B %Y') for item in monthly_participation]
            context['chart_data'] = [item['count'] for item in monthly_participation]

            # Additional statistics for the chart
            context['total_events'] = Event.objects.count()
            context['total_participants'] = EventParticipation.objects.count()
            context['upcoming_events_count'] = Event.objects.filter(
                date__gte=timezone.now()
            ).count()
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'alumni'):
            messages.warning(request, 'Please complete your profile first.')
            return redirect('alumni:profile')
        return super().dispatch(request, *args, **kwargs)

class AlumniDirectoryView(LoginRequiredMixin, ListView):
    model = Alumni
    template_name = 'alumni/directory.html'
    context_object_name = 'alumni_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(degree__icontains=search_query)
            )
        return queryset.order_by('-graduation_year')

class AlumniDetailView(LoginRequiredMixin, DetailView):
    model = Alumni
    template_name = 'alumni/alumni_detail.html'
    context_object_name = 'alumni'

class ProfileView(LoginRequiredMixin, UpdateView):
    model = Alumni
    template_name = 'alumni/profile_form.html'
    fields = ['graduation_year', 'degree']
    success_url = '/dashboard/'

    def get_object(self, queryset=None):
        obj, created = Alumni.objects.get_or_create(
            user=self.request.user,
            defaults={
                'graduation_year': 2024,
                'degree': 'Not Specified'
            }
        )
        return obj

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Alumni
    form_class = AlumniProfileForm
    template_name = 'alumni/profile_edit.html'
    success_url = reverse_lazy('alumni:dashboard')

    def get_object(self, queryset=None):
        return self.request.user.alumni

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = AlumniProfileForm(request.POST, request.FILES, instance=request.user.alumni)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('alumni:profile')
    else:
        form = AlumniProfileForm(instance=request.user.alumni)
    return render(request, 'alumni/profile_edit.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('alumni:home')