from datetime import datetime, timezone

import requests
from django.core.management.base import BaseCommand

from earthquakes.models import Earthquake

BASE = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}.geojson"


class Command(BaseCommand):
    help = "Merr tërmetet e fundit nga USGS dhe i ruan në bazën e të dhënave."

    def add_arguments(self, parser):
        parser.add_argument(
            "--feed",
            default="2.5_month",
            help="p.sh. 2.5_week, 2.5_month, 4.5_month, all_day",
        )

    def handle(self, *args, **options):
        url = BASE.format(options["feed"])
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        features = response.json()["features"]

        created = 0
        for f in features:
            props = f["properties"]
            lon, lat, depth = f["geometry"]["coordinates"]
            if props.get("mag") is None:
                continue
            _, is_new = Earthquake.objects.update_or_create(
                usgs_id=f["id"],
                defaults={
                    "magnitude": props["mag"],
                    "place": props.get("place") or "Pa emër",
                    "time": datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
                    "latitude": lat,
                    "longitude": lon,
                    "depth_km": depth,
                    "url": props.get("url") or "",
                },
            )
            created += is_new

        self.stdout.write(self.style.SUCCESS(
            f"U procesuan {len(features)} tërmete, {created} të reja."
        ))
