from oscar.core.loading import get_model
from oscar.apps.basket.middleware import BasketMiddleware as CoreBasketMiddleware
from django.utils.functional import SimpleLazyObject
from piezas import settings
import models
import managers

Basket = models.Basket

class BasketMiddleware(CoreBasketMiddleware):

    def process_request(self, request):
        request.cookies_to_delete = []
        request.strategy = None

        def lazy_load_basket():
            basket = self.get_basket(request)
            basket.strategy = request.strategy

            request.basket = basket
            return basket

        request.basket = SimpleLazyObject(lazy_load_basket)

    def get_basket(self, request):
        """
        Return an open basket for this request
        """
        manager = Basket.open
        cookie_basket = self.get_cookie_basket(
            settings.OSCAR_BASKET_COOKIE_OPEN, request, manager)

        if hasattr(request, 'user') and request.user.is_authenticated():
            # Signed-in user: if they have a cookie basket too, it means
            # that they have just signed in and we need to merge their cookie
            # basket into their user basket, then delete the cookie
            try:
                basket, _ = manager.get_or_create(owner=request.user)
            except Basket.MultipleObjectsReturned:
                # Not sure quite how we end up here with multiple baskets
                # We merge them and create a fresh one
                old_baskets = list(manager.filter(owner=request.user))
                basket = old_baskets[0]
                for other_basket in old_baskets[1:]:
                    self.merge_baskets(basket, other_basket)
            # Assign user onto basket to prevent further SQL queries when
            # basket.owner is accessed.
            basket.owner = request.user

            if cookie_basket:
                self.merge_baskets(basket, cookie_basket)
                request.cookies_to_delete.append(
                    settings.OSCAR_BASKET_COOKIE_OPEN)
        elif cookie_basket:
            # Anonymous user with a basket tied to the cookie
            basket = cookie_basket
        else:
            # Anonymous user with no basket - we don't save the basket until
            # we need to.
            basket = Basket()
        return basket
