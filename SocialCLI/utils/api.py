from functools import partial
import requests
from . import load_config

config = load_config()
API_SOURCE = "https://yuque.com/api/v2"

HEADERS = config['headers']

USER = config['user']
REPO_ID = config['repo_id']

DOC_LIST_API = '{api_source}/repos/{repo_id}/docs'
DOC_API = '{api_source}/repos/{repo_id}/docs/{doc_id}?raw=1'
UPDATE_DOC_API = '{api_source}/repos/{repo_id}/docs/{doc_id}'
CREATE_DOC_API = '{api_source}/repos/{repo_id}/docs'

get = partial(requests.get, headers=HEADERS)
put = partial(requests.put, headers=HEADERS)
post = partial(requests.post, headers=HEADERS)


class society:
    def get_doc_list(self):
        api = self._get_api(DOC_LIST_API)
        req = get(api)
        return req.json()

    def get_doc(self, doc_id):
        api = self._get_api(DOC_API, doc_id=doc_id)
        req = get(api)
        return req.json()

    def update_doc(self, doc_id, title, body):
        api = self._get_api(UPDATE_DOC_API, doc_id=doc_id)
        put(api, data={
            'title': title,
            'body': body
        })

    def create_doc(self, title):
        api = self._get_api(CREATE_DOC_API)
        post(api, {'title': title, 'body': ''})

    def _get_api(self, api_template, **kwargs):
        return api_template.format(
            api_source=API_SOURCE,
            repo_id=REPO_ID,
            **kwargs
        )

    def _exists_doc(self, title):
        doc_list = self.get_doc_list()
        return title in [doc['title'] for doc in doc_list['data']]


api = society()
