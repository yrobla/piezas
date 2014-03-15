from oscar.apps.basket.managers import OpenBasketManager as CoreOpenBasketManager, \
    SavedBasketManager as CoreSavedBasketManager

class OpenBasketManager(CoreOpenBasketManager):
    """For searching/creating OPEN baskets only."""
    status_filter = "Open"

    def get_query_set(self):
        return super(OpenBasketManager, self).get_query_set().filter(
            status=self.status_filter)

    def get_or_create(self, **kwargs):
        return self.get_query_set().get_or_create(
            status=self.status_filter, **kwargs)

class SavedBasketManager(CoreSavedBasketManager):
    """For searching/creating SAVED baskets only."""
    status_filter = "Saved"

    def get_query_set(self):
        return super(SavedBasketManager, self).get_query_set().filter(
            status=self.status_filter)

    def create(self, **kwargs):
        return self.get_query_set().create(status=self.status_filter, **kwargs)

    def get_or_create(self, **kwargs):
        return self.get_query_set().get_or_create(
            status=self.status_filter, **kwargs)

