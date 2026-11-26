from datetime import timedelta

from django.db.models import Avg, Count, Max
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone

from .models import Earthquake


def _number(value, default, cast):
    try:
        return cast(value)
    except (TypeError, ValueError):
        return default


def index(request):
    min_mag = _number(request.GET.get("min_mag"), 2.5, float)
    days = min(max(_number(request.GET.get("days"), 7, int), 1), 30)
    q = request.GET.get("q", "").strip()

    since = timezone.now() - timedelta(days=days)
    qs = Earthquake.objects.filter(time__gte=since, magnitude__gte=min_mag)
    if q:
        qs = qs.filter(place__icontains=q)

    stats = qs.aggregate(total=Count("id"), strongest=Max("magnitude"), average=Avg("magnitude"))

    per_day = (
        qs.annotate(day=TruncDate("time"))
        .values("day")
        .annotate(n=Count("id"))
        .order_by("day")
    )
    chart = {
        "labels": [row["day"].isoformat() for row in per_day],
        "values": [row["n"] for row in per_day],
    }

    points = list(qs.values("place", "magnitude", "latitude", "longitude", "depth_km", "url")[:500])

    return render(request, "earthquakes/index.html", {
        "earthquakes": qs[:50],
        "stats": stats,
        "chart": chart,
        "points": points,
        "min_mag": min_mag,
        "days": days,
        "q": q,
    })
