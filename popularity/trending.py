from collections import defaultdict
from django.db.models import Count, Sum
from accounts.regions import REGIONS
from cart.models import Item
import movies

def trending_by_region(top_n=5):
    rows = (
        Item.objects
        .values('order__region', 'movie_id', 'movie__name')
        .annotate(units=Sum('quantity'), buyers=Count('order__user', distinct=True))
        .order_by('order__region', '-units', 'movie__name')
    )
    by_region = defaultdict(list)
    for row in rows:
        by_region[row['order__region']].append(row)
    return [
        {"code": code, "name": name, "lat": lat, "lng": lng, "top": by_region[code][:top_n]}
        for code, name, lat, lng in REGIONS
    ]