from django.db import models
from django.contrib.auth.models import User

# Room Model
class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='rooms/')

    def __str__(self):
        return self.name

# Event Model
class Event(models.Model):
    name = models.CharField(max_length=255)
    time = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Live Event Model
class LiveEvent(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tags = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# Model for storing user trip details
class UserTrip(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming each user can have a trip
    destination = models.CharField(max_length=200)  # Where the trip is planned
    planned_activities = models.TextField(blank=True, null=True)  # Text to hold planned activities in a string format
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip to {self.destination} by {self.user.username}"

# Model for storing chatbot recommendations
class TripRecommendation(models.Model):
    user_trip = models.ForeignKey(UserTrip, on_delete=models.CASCADE, related_name="recommendations")
    activity_name = models.CharField(max_length=200)
    activity_description = models.TextField()
    activity_location = models.CharField(max_length=200)
    activity_time = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recommendation for {self.user_trip.destination}: {self.activity_name}"


# Surprise Me Feature - Random Activity Model (Surprise recommendations)
class SurpriseActivity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']


# Surprise Me Action (tracks surprise activities chosen)
class SurpriseActivityChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surprise_choices')
    activity = models.ForeignKey(SurpriseActivity, on_delete=models.CASCADE)
    chosen_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Surprise activity {self.activity.name} chosen by {self.user.username}"

