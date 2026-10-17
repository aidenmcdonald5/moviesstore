from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie, Review
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce


# Create your views here.
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})
def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')
def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')
@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    order = Order()
    order.user = request.user
    order.total = cart_total
    profile = getattr(request.user, 'profile', None)
    order.region = profile.region if profile else None
    order.save()
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})
@login_required
def user_engagement(request):
    if not request.user.is_staff:
        return redirect('home.index')
    size = request.GET.get('size', '').strip()
    users = (
        User.objects
        .annotate(purchase_count=Coalesce(Sum('order__item__quantity'), Value(0)))
        .order_by('-purchase_count', 'username')
    )
    if size:
        try:
            size_int = int(size)
            if size_int > 0:
                users = users[:size_int]
        except ValueError:
            pass

    top_commenter = (
        User.objects
        .annotate(comment_count=Coalesce(Count('review'), Value(0)))
        .order_by('-comment_count', 'username')
        .first()
    )   

    template_data = {}
    template_data['title'] = 'User Engagement'
    template_data['users'] = users
    template_data['size'] = size
    template_data['top_commenter'] = top_commenter
    return render(request, 'cart/user_engagement.html', {'template_data': template_data})