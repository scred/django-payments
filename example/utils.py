from payments.connector import PaymentConnector

class PickledPaymentConnector(PaymentConnector):

    def __init__(self, code, data={}):
        data["code"] = code
        self.code = code
        self.data = data

    def get_value(self, key):
        return self.data[key]

    @classmethod
    def lookup(self, code):
        payment = self(code)
        payment.load()
        return payment

    def load(self):
        import pickle
        fh = open("%s.pickle" % self.code, "r")
        self.data = pickle.load(fh)
        fh.close()

    def save(self):
        import pickle
        fh = open("%s.pickle" % self.code, "w")
        pickle.dump(self.data, fh)
        fh.close()

PaymentConnector.set_connector(PickledPaymentConnector)
