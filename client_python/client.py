import requests
from requests.adapters import HTTPAdapter, Retry
from time import sleep
from http import HTTPStatus

class Tokens:

    def __init__(self, access=None, refresh=None):
        self._access = access
        self._refresh = refresh

    @property
    def access(self):
        return {'jwt-access-token': self._access}

    @property
    def refresh(self):
        return {'jwt-refresh-token': self._refresh}

    @access.setter
    def access(self, value):
        self._access = value

    @refresh.setter
    def refresh(self, value):
        self._refresh = value


class SessionApi(requests.Session):

    tokens = Tokens()
    token_refresh_url = 'http://localhost:3001/token/refresh'


    def request(self, method, url, **kwargs):
        resp = super().request(method, url, **kwargs)

        if resp.status_code == HTTPStatus.UNAUTHORIZED:
            status_code, _ = self.refresh_token()
            if status_code == HTTPStatus.OK:
                kwargs['cookies'] = self.tokens.access
                resp = super().request(method, url, **kwargs)

        return resp

    def refresh_token(self):
        resp = requests.request('POST', self.token_refresh_url, cookies=self.tokens.refresh)
        if resp.ok:
            self.tokens.access = resp.cookies['jwt-access-token']

        return resp.status_code, resp.json()


class Client:

    def __init__(self, session):
        self.session = session

    def login(self):
        resp = self.session.request('POST',
                                    'http://localhost:3001/login',
                                     data = {'email': 'user1@user.com',
                                    'password': '123456!!'})

        if resp.ok:
            self.session.tokens.access = resp.cookies['jwt-access-token']
            self.session.tokens.refresh = resp.cookies['jwt-refresh-token']

        return resp.status_code, resp.json()

    def users(self):

        resp = self.session.request('GET','http://localhost:3001/users/', cookies=self.session.tokens.access)

        return resp.status_code, resp.json()


if __name__ == '__main__':

    session = SessionApi()

    client = Client(session)

    print(client.login())

    print(client.users())

    sleep(10)
    print(client.users())

    # print(client.refresh_token())

    # print(client.users())
