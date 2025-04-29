from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib

class LedgerEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    entry_type = models.CharField(max_length=20, choices=[('feedback', 'Feedback'), ('complaint', 'Complaint')])
    timestamp = models.DateTimeField(default=timezone.now)
    previous_hash = models.CharField(max_length=64, blank=True)
    hash = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        if not self.previous_hash:
            last_entry = LedgerEntry.objects.order_by('-id').first()
            self.previous_hash = last_entry.hash if last_entry else '0'*64
        to_hash = f"{self.user.id}{self.message}{self.entry_type}{self.timestamp}{self.previous_hash}"
        self.hash = hashlib.sha256(to_hash.encode('utf-8')).hexdigest()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.entry_type} at {self.timestamp}"

    @staticmethod
    def validate_ledger():
        """
        Validate the integrity of the entire ledger.
        Returns True if intact, False if broken.
        """
        entries = LedgerEntry.objects.order_by('timestamp')
        previous_hash = '0'*64
        for entry in entries:
            # Recalculate expected hash
            to_hash = f"{entry.user.id}{entry.message}{entry.entry_type}{entry.timestamp}{entry.previous_hash}"
            expected_hash = hashlib.sha256(to_hash.encode('utf-8')).hexdigest()

            if entry.previous_hash != previous_hash or entry.hash != expected_hash:
                return False  # Ledger is broken

            previous_hash = entry.hash
        return True  # Ledger is valid
