class Accounts(object):
    """
    A class to query and use Pardot  accounts.
    Account field reference: https://developer.salesforce.com/docs/marketing/pardot/guide/account-v5.html    
    """

    def __init__(self, client):
        self.client = client

    def read(self, **kwargs):
        """
        Returns the data for the account of the currently logged in user.
        """
        response = self._get(path=None, params=kwargs)
        return response

    def _get(self, object_name='account', path=None, params=None):
        """GET requests for the Account object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='account', path=None, params=None):
        """POST requests for the Account object."""
        if params is None:
            params = {}
        response = self.client.post(object_name=object_name, path=path, params=params)
        return response
