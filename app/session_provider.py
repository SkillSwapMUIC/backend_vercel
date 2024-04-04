from flask import session


class SessionProvider:
    def __getitem__(self, key):
        return session.get(key)

    def __setitem__(self, key, value):
        session[key] = value


provider = SessionProvider()
