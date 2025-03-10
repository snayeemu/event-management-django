from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from events import models, forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Prefetch, Count, Q
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm

def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

# Create your views here.
def event_list(request):
    # events = models.Event.objects.all()
    events = models.Event.objects.select_related("category").annotate(
        Count("participants")
    )
    data = "abc"
    if request.method == "POST": 
        data = request.POST
        if data["name"] != "" and data["category"] != "all":
            # category = models.Category.get(name=)
            events = events.filter(
                name__icontains=data["name"], category__name=data["category"]
            )
        elif data["name"] != "":
            events = events.filter(name__icontains=data["name"])
        elif data["category"] != "all":
            events = events.filter(category__name=data["category"])
    search_form = forms.SearchForm(request.GET)
    context = {"events": events, "search_form": search_form, "data": data}
    return render(request, "event/events-list.html", context)

def event_cards(request):
    # events = models.Event.objects.all()
    events = models.Event.objects.select_related("category").annotate(
        Count("participants")
    )
    data = "abc"
    if request.method == "POST": 
        data = request.POST
        if data["name"] != "" and data["category"] != "all":
            # category = models.Category.get(name=)
            events = events.filter(
                name__icontains=data["name"], category__name=data["category"]
            )
        elif data["name"] != "":
            events = events.filter(name__icontains=data["name"])
        elif data["category"] != "all":
            events = events.filter(category__name=data["category"])
    context = {"events": events}
    return render(request, "event/event-cards.html", context)


def event_details(request, pk):
    event = models.Event.objects.prefetch_related("participant_set").get(id=pk)
    return render(request, "events/event_detail.html", {"event": event})

@login_required
@permission_required("event.add_event", login_url="no-permission")
def event_create(request):
    event_form = forms.EventForm()

    if request.method == "POST":
        event_form = forms.EventForm(request.POST, request.FILES)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, f"Event created Successfully")
            return redirect("event-create")

    context = {
        "event_form": event_form,
    }
    return render(request, "event/events-forms.html", context)

@login_required
@permission_required("event.change_event", login_url="no-permission")
def event_update(request, pk):
    event = get_object_or_404(models.Event, id=pk)
    event_form = forms.EventForm(instance=event)

    if request.method == "POST":
        event_form = forms.EventForm(request.POST, instance=event)

        if event_form.is_valid():
            event_form.save()
            messages.success(request, f"Event updated Successfully")
            return redirect("event-create")

    context = {"event_form": event_form}
    return render(request, "event/events-forms.html", context)

@login_required
@permission_required("event.delete_event", login_url="no-permission")
def event_delete(request, pk):
    event = get_object_or_404(models.Event, id=pk)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted Successfully")
        return redirect("event-list")
    return redirect("event-list")


def event_details(request, pk):
    event = get_object_or_404(models.Event, id=pk)
    return render(request, "event/event-details.html", {"event": event})

@login_required
@permission_required("event.view_participant", login_url="no-permission")
def participant_list(request):
    participants = User.objects.prefetch_related("event_set").all()
    return render(
        request, "participant/participant-list.html", {"participants": participants}
    )



@login_required
@permission_required("event.change_participant", login_url="no-permission")
def participant_update(request, pk):
    participant = get_object_or_404(User, id=pk)
    participant_form = UserCreationForm(instance=participant)

    if request.method == "POST":
        participant_form = UserCreationForm(request.POST, instance=participant)

        if participant_form.is_valid():
            user = participant_form.save(commit=False)
            user.set_password(request.POST.get("password"))
            user.save()
            messages.success(request, f"Participant Updated Successfully")
            return redirect("participant-create")

    context = {"participant_form": participant_form}
    return render(request, "participant/participant-form.html", context)


def participant_delete(request, pk):
    participant = get_object_or_404(models.Participant, id=pk)

    if request.method == "POST":
        participant.delete()
        messages.success(request, "Participant Deleted Successfully")
        return redirect("participant-list")
    return redirect("participant-list")


def category_list(request):
    categories = models.Category.objects.prefetch_related(Prefetch("event_set")).all()
    return render(request, "category/category-list.html", {"categories": categories})


def category_create(request):
    category_form = forms.CategoryForm()

    if request.method == "POST":
        category_form = forms.CategoryForm(request.POST)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, f"category created Successfully")
            return redirect("category-create")

    return render(
        request,
        "category/category-form.html",
        {"category_form": category_form},
    )


def category_update(request, pk):
    category = get_object_or_404(models.Category, id=pk)
    category_form = forms.CategoryForm(instance=category)

    if request.method == "POST":
        category_form = forms.CategoryForm(request.POST, instance=category)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, f"category Updated Successfully")
            return redirect("category-create")

    context = {"category_form": category_form}
    return render(request, "category/category-form.html", context)


def category_delete(request, pk):
    category = get_object_or_404(models.Category, id=pk)

    if request.method == "POST":
        category.delete()
        messages.success(request, "category Deleted Successfully")
        return redirect("category-list")
    return redirect("category-list")

@login_required
@user_passes_test(is_organizer, login_url="no-permission")
def organizer_dashboard(request):
    # Aggregate query to calculate the total number of participants
    categories = models.Category.objects.prefetch_related(Prefetch("event_set")).all()
    q = request.GET.get("q", "all")
    total_participants = User.objects.filter(event__isnull=False).distinct().count()
    base = models.Event.objects.select_related("category")
    todays_event = base.filter(date=datetime.now().date())
    if q == "all":
        events = base.annotate(Count("participants"))
    elif q == "upcoming":
        events = base.filter(date__gt=datetime.now()).annotate(Count("participants"))
    elif q == "past":
        events = base.filter(date__lt=datetime.now()).annotate(Count("participants"))

    counts = base.aggregate(
        total=Count("id"),
        upcoming_events=Count("id", Q(date__gt=datetime.now())),
        past_events=Count("id", Q(date__lt=datetime.now())),
    )
    context = {
        "total_participants": total_participants,
        "events": events,
        "counts": counts,
        "todays_event": todays_event, 
        "categories": categories,
    }
    return render(request, "dashboard/organizer-dashboard.html", context)

@login_required
def rsvp(request, id):
    event = models.Event.objects.get(id=id)
    event_set = request.user.event_set.filter(id=id)
    if event_set.exists():
        messages.warning(request, f"Event {event.name} already added!")
        return redirect("event-list")
    else:
        event.participants.add(request.user)
        messages.success(request, f"Event {event.name} added successfully!")
        try:
            subject = f"RSVP Confirmation for {event.name}" 
            message = f"Hello {request.user.username},\n\nYou have successfully RSVP'd to: {event.name}\nDate: {event.date}\nTime: {event.time}\nLocation: {event.location}\n\nThank you for joining!"
            recipient_list = [request.user.email] 
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(str(e)) 
    return redirect("event-list") 