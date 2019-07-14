import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Poem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    poem = models.TextField()
    average_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    total_ratings = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # String representation of self
    def __str__(self):
        return f"{self.pk} - {self.user} ||| Title: {self.title} ||| Average Rating: {self.average_rating} ||| Total Ratings: {self.total_ratings} ||| Date: {self.date}"


class ChangePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    # String representation of self
    def __str__(self):
        return f"{self.pk} - {self.user} ||| Change Password: Initiated"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    CHOICE = [(1.0, "1.0"), (2.0, "2.0"), (3.0, "3.0"), (4.0, "4.0"), (5.0, "5.0")]
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=CHOICE)
    # Unique column pair
    class Meta:
        unique_together = ("user", "poem")

    # String representation of self
    def __str__(self):
        return f"{self.pk} - {self.user} ||| Poem: {self.poem.pk} ||| Rating: {self.rating}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    headline = models.CharField(max_length=64)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # Unique column pair
    class Meta:
        unique_together = ("user", "poem")

    # String representation of self
    def __str__(self):
        return f"{self.pk} - {self.user} ||| Poem: {self.poem.pk} ||| Headline: {self.headline}"


class Notification(models.Model):
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)
    CHOICE = [("Rate", "Rate"), ("Review", "Review")]
    notification_type = models.CharField(max_length=64, choices=CHOICE)
    notification_data = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    # String representation of self
    def __str__(self):
        return f"{self.pk} - {self.receiver} ||| Sender: {self.sender} ||| {self.notification_data}  ||| {self.read} ||| Date: {self.date}"
