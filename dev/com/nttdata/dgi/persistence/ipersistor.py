class IPersistor:

    def persist(self, *args, **kwargs):
        return self

    def select(self, *args, **kwargs):
        return self

    def drop(self, *args, **kwargs):
        return self

    def ask(self, *args, **kwargs) -> bool:
        return False

    def search(self, *args, **kwargs) -> dict:
        return False
