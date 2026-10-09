from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .trending import trending_by_region


@login_required
def popularity_map(request):
    regions = trending_by_region()
    markers = [{"code": r["code"], "name": r["name"], "lat": r["lat"], "lng": r["lng"]} for r in regions]
    profile = getattr(request.user, "profile", None)
    template_data = {
        "title": "Local Popularity Map",
        "regions": regions,
        "markers": markers,
        "selected": (profile and profile.region) or regions[0]["code"],
    }
    return render(request, "popularity/map.html", {"template_data": template_data})