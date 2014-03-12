from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication

class CustomerApplication(CoreCustomerApplication):
    pass

application = CustomerApplication()
