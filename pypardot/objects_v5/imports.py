import os
import json

class Imports(object):
    """
    A class to query and use Pardot Import API.
    Import API reference: https://developer.salesforce.com/docs/marketing/pardot/guide/import-v5.html
    """

    def __init__(self, client):
        self.client = client

    def create(self, file_name=None, **kwargs):
        """Creates a new asynchronous import.
        A single part with the name "importFile" should contain the CSV file for the batch. The file should contain a header row.
        Params(as importInput if file_name is not null):
        {
          "operation": "Upsert",
          "object": "Prospect",
          "state": "Ready"
        }
        """

        input = {
            "status": "Ready",
            "operation": "Upsert",
            "object": "Prospect",
            'restoreDeleted': True,
            'createOnNoMatch': True
        }

        if not file_name:
            headers = {"Content-Type": "application/json"}
            response = self._post(path=None, json=kwargs, headers=headers)
            return response

        with open(file_name, "rb") as f:
            files = {"file": f}
            input = {"input": json.dumps(input)}
            response = self._post(path=None,
                                  data=input,
                                  files=files)
        return response

    def add_batch(self, id, file_name, **kwargs):
        """Allows adding batches of data to an existing import when in the "Open" state.
        A single part with the name "importFile" should contain the CSV file for the batch. The file should contain a header row.
        """
        with open(file_name, "rb") as f:
            """files = {"importFile": f}"""
            files = {"file": f}

            print(files)

            response = self._post(path='/{id}/batches'.format(id=id),
                                  params=kwargs,
                                  files=files)

        return response

    def update(self, id=None, **kwargs):
        """Used to submit the import by changing the state to "Ready". After this step, no more batches of data can be added, and processing of the import begins.
        """
        headers = {"Content-Type": "application/json"}
        response = self._patch(path='/{id}'.format(id=id),
                               json=kwargs, headers=headers)
        return response

    def read(self, id=None, **kwargs):
        """Returns the current state of the import. If processing is complete, the output provides a path to the results of the operation along with any statistics about the operation.
        """

        if not hasattr(kwargs, 'fields'):
            kwargs['fields']='id,isExpired,status,createdCount,updatedCount,errorsRef,errorCount'

        response = self._get(path='/{id}'.format(id=id), params=kwargs)
        return response

    def query(self, **kwargs):
        """Used by administrators to retrieve a list of imports and their status. A user must have the “Admin > Imports > View” ability to execute this endpoint.
        """
        if not hasattr(kwargs, 'fields'):
            kwargs['fields']='id,createdAt,updatedAt,status'

        response = self._get(path=None, params=kwargs)
        return response

    def download_errors(self, **kwargs):
        """Download errors associated with the specified import (after it is complete).
        """
        response = self._get(path='/{id}/errors'.format(id=id), params=kwargs)
        return response
    
    def cancel(self, id, **kwargs):
        """Used to cancel the import. If the import is already completed or failed, it can't be canceled.
        """
        headers = {"Content-Type": "application/json"}
        response = self._post(path='/{id}/do/cancel'.format(id=id), params=kwargs, headers=headers)
        return response

    def _get(self, object_name='imports', path=None, params=None):
        """GET requests for the Account object."""
        if params is None:
            params = {}
        response = self.client.get(object_name=object_name, path=path, params=params)
        return response

    def _post(self, object_name='imports', path=None, params=None, headers=None, json=None, files=None, data=None):
        """POST requests for the Account object."""
        response = self.client.post(object_name=object_name, path=path,
                                    params=params, headers=headers,
                                    json=json, files=files, data=data)
        return response

    def _patch(self, object_name='imports', path=None, params=None,
              headers=None, json=None, files=None):
        """POST requests for the Account object."""
        response = self.client.patch(object_name=object_name, path=path,
                                     params=params, headers=headers,
                                     json=json, files=files)
        return response
