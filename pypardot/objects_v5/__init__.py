from .accounts import Accounts
from .imports import Imports

def load_objects(client):
    client.accounts = Accounts(client)
    client.imports = Imports(client)