# class to write auditing events, give this to PaymentProcessor in init.
# or rather you give a sub-class of this where you override stuff

class PaymentAuditEvent():

    @staticmethod
    def store_audit_event(event_type, payment_method, payment_code, data):
        """
        Override this in a sub-class of PaymentAuditEvent. The
        overriding method should save the audit event to persistent
        storage in whatever way is convenient.
        
        event_type = basestring
        payment_method = basestring
        payment_code = basestring
        data = dict where keys and values are basestrings
        """
        raise NotImplementedError()

class AuditDjango(PaymentAuditEvent):

    @staticmethod
    def store_audit_event(event_type, payment_method, payment_code, data):

        # ... do stuff ...
        
        pass
