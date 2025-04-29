import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import Event, LiveEvent, Room, TripRecommendation, UserTrip
from .forms import EventForm
from datetime import datetime
from django.utils import timezone
import random
from nltk import word_tokenize, pos_tag
import spacy
from .remainder import send_email_reminder, send_sms_reminder
from datetime import timedelta


import logging

logger = logging.getLogger(__name__)

def personalized_home(request):
    return render(request, 'personalized_guest_experience/personalized_home.html')

def ai_recommendations(request):
    # Fetch all rooms from the database
    all_rooms = list(Room.objects.all())

    # Check time of day and filter rooms
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:  # Morning
        recommended_rooms = [room for room in all_rooms if "Yoga" in room.name or "Garden" in room.name]
    elif 12 <= current_hour < 18:  # Afternoon
        recommended_rooms = [room for room in all_rooms if "Ocean" in room.name or "Garden" in room.name]
    else:  # Evening/Night
        recommended_rooms = [room for room in all_rooms if "Presidential" in room.name or "Sunset" in room.name]

    # Add randomness for fun
    random.shuffle(recommended_rooms)
    recommended_rooms = recommended_rooms[:3]  # Limit to 3 rooms max

    # Pagination
    paginator = Paginator(recommended_rooms, 3)  # Show 3 rooms per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'personalized_guest_experience/ai_recommendations.html', {'page_obj': page_obj})
def room_detail(request, room_slug):
    # Fetch the specific room based on the slug
    room = get_object_or_404(Room, slug=room_slug)
    
    return render(request, 'personalized_guest_experience/room_detail.html', {'room': room})

def event_schedule(request):
    now = timezone.now()

    # Automatically delete past events
    Event.objects.filter(time__lt=now).delete()

    events = Event.objects.all().order_by('-time')  # Fetch all events, newest first
    paginator = Paginator(events, 3)  # Paginate events (3 per page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    today = timezone.now().date()  # Today's date for comparison

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            # Ensure the user is logged in before saving the event
            if request.user.is_authenticated:
                event = form.save(commit=False)
                event.created_by = request.user  # Assign the logged-in user
                event.save()

                # Send email and SMS reminder (1 day before the event)
                reminder_time = event.time - timedelta(days=1)  # 1 day before the event
                phone_number = event.created_by.profile.phone_number if hasattr(event.created_by, 'profile') else None

                # Send reminder if user is logged in and has a phone number
                if request.user.is_authenticated:
                    send_email_reminder(event)  # Send the email reminder
                    if phone_number:
                        send_sms_reminder(phone_number, event.name, event.time)  # Send SMS reminder

                return redirect('personalized_guest_experience:event_schedule')  # Redirect back to event list
    else:
        form = EventForm()

    # Pass 'today' to template context
    return render(request, 'personalized_guest_experience/event_schedule.html', {
        'page_obj': page_obj,
        'form': form,
        'today': today,  # Passing today's date to the template
    })
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return JsonResponse({
                'success': True,
                'event': {
                    'id': event.id,
                    'name': event.name,
                    'location': event.location,
                    'time': event.time.strftime('%I:%M %p'),
                    'created_at': event.created_at.strftime('%B %d, %Y %H:%M'),
                    'image_url': event.image.url if event.image else '',
                    'created_by': event.created_by.username,
                }
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def live_event_suggestions(request):
    live_events = LiveEvent.objects.all().order_by('start_time')
    today = timezone.now().date()

    for event in live_events:
        event.is_today = (event.start_time.date() == today)

    paginator = Paginator(live_events, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'personalized_guest_experience/live_events.html', {'live_events': live_events, 'page_obj': page_obj})

nlp = spacy.load("en_core_web_sm")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input', '').strip()

            if not user_input:
                return JsonResponse({'error': 'No input received'}, status=400)

            # Use spaCy for Intent Detection
            doc = nlp(user_input.lower())
            intent = detect_intent(doc)

            # Default response
            bot_reply = "🤔 I'm here to help with anything you need. Could you tell me a bit more?"
            suggested_activity = None

            # Fetch dynamic recommendations
            if intent in ["beach", "restaurant", "event", "hotel"]:
                bot_reply, suggested_activity = fetch_dynamic_recommendations(intent)

            return JsonResponse({
                'bot_reply': bot_reply,
                'suggested_activity': suggested_activity  # important!
            })

        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def fetch_dynamic_recommendations(intent):
    """
    Fetch dynamic recommendations based on the intent.
    Returns both a text reply and a suggested activity object.
    """
    if intent == "beach":
        return (
            "🏖️ There are some great beaches nearby: Sandy Shores, Blue Lagoon, and Coral Bay!",
            {
                "name": "Sandy Shores",
                "location": "Nearby Coast",
                "time": "Morning"
            }
        )

    elif intent == "restaurant":
        return (
            "🍽️ Here are some great restaurants: Coastal Cafe, The Beach Grill, Sunset Bistro.",
            {
                "name": "Coastal Cafe",
                "location": "Downtown",
                "time": "Dinner"
            }
        )

    elif intent == "event":
        return (
            "🎭 There's a live music event tonight! Would you like me to add it to your trip?",
            {
                "name": "Live Music Concert",
                "location": "City Center Stage",
                "time": "Tonight at 8 PM"
            }
        )

    elif intent == "hotel":
        return (
            "🏨 I found these hotels for you: Ocean View Resort, Luxe Suites, and Seaside Inn.",
            {
                "name": "Ocean View Resort",
                "location": "Seaside",
                "time": "Check-in: 3 PM"
            }
        )

    else:
        return (
            "🤔 I wasn't able to find exactly what you're looking for, but I can help with other queries!",
            None
        )
def detect_intent(doc):
    """
    Advanced intent detection using spaCy and a few predefined keywords.
    """
    beach_keywords = ['beach', 'sand', 'coast', 'sea', 'shore']
    restaurant_keywords = ['restaurant', 'food', 'eat', 'dine', 'meal']
    event_keywords = ['event', 'concert', 'show', 'festival', 'party']
    hotel_keywords = ['hotel', 'stay', 'room', 'accommodation', 'resort']

    intent = "general"

    for token in doc:
        if token.text in beach_keywords:
            intent = "beach"
        elif token.text in restaurant_keywords:
            intent = "restaurant"
        elif token.text in event_keywords:
            intent = "event"
        elif token.text in hotel_keywords:
            intent = "hotel"

    if intent == "general" and doc.ents:
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                intent = "location"

    return intent

@csrf_exempt  # Exempt CSRF for testing
def trip_planner(request):
    if request.method == 'POST':
        logger.debug(f"Request Received: {request.body}")  # Log the raw body of the request
        try:
            data = json.loads(request.body)  # Parse JSON from the body
            user_input = data.get('user_input', '').strip()  # Fetch the user input
            logger.debug(f"User Input: {user_input}")  # Log the user input

            if user_input:
                recommendations = get_mock_recommendations(user_input)
                trip, created = UserTrip.objects.get_or_create(user=request.user, destination="Sample Destination")

                for rec in recommendations:
                    TripRecommendation.objects.create(
                        user_trip=trip,
                        activity_name=rec['name'],
                        activity_description=rec['description'],
                        activity_location=rec['location'],
                        activity_time=rec['time']
                    )

                logger.debug(f"Recommendations: {recommendations}")  # Log recommendations

                return JsonResponse({
                    'recommendations': recommendations,
                    'itinerary': trip.planned_activities
                })
            else:
                logger.debug('No user input received.')  # Log empty input error
                return JsonResponse({'error': 'No input received'}, status=400)

        except Exception as e:
            logger.error(f"Error processing the request: {e}")
            return JsonResponse({'error': 'Error processing request'}, status=500)

    return render(request, 'personalized_guest_experience/trip_planner.html')


# Mock function to simulate recommendation generation
def get_mock_recommendations(user_input):
    # For now, just return static mock data
    return [
        {
            'name': 'Visit the Eiffel Tower',
            'description': 'A must-see landmark in Paris, known for its breathtaking views.',
            'location': 'Paris, France',
            'time': '10:00 AM'
        },
        {
            'name': 'Take a Seine River Cruise',
            'description': 'Enjoy the beauty of Paris from the Seine River.',
            'location': 'Paris, France',
            'time': '2:00 PM'
        }
    ]

# View for handling the "Surprise Me" button
def surprise_me(request):
    _ = request
    all_activities = LiveEvent.objects.all()
    
    if not all_activities.exists():
        return JsonResponse({'error': 'No live events available.'}, status=404)
    
    random_activity = random.choice(all_activities)
    return JsonResponse({
        'activity_name': random_activity.name,
        'activity_location': random_activity.location,
        'activity_time': random_activity.start_time.strftime('%I:%M %p'),
    })
