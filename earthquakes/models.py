from django.db import models


class Earthquake(models.Model):
    usgs_id = models.CharField(max_length=50, unique=True)
    magnitude = models.FloatField()
    place = models.CharField(max_length=255)
    time = models.DateTimeField(db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    depth_km = models.FloatField(null=True, blank=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return f"M{self.magnitude} - {self.place}"
