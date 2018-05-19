import codecs
import os
from utils import (mkdir, api)
import time
from prettytable import PrettyTable
from utils import init_config

DATA_DIR = 'D:\\Data\\society'
NAME_FORMAT = "{data_dir}/{name}-{doc_id}.md"


class Dispatch:
    def __init__(self):
        self._refresh_time()
        self.nonparametric_command = {
            'REFRESH': self.refresh_cache,
            'UPDATE': self.update,
            'INIT': self.init_config
        }

        self.parametric_command = {
            'FIND': self.find,
            'CREATE': self.create,
        }

        self.start()

    def init_config(self):
        program_name = input("Please input your program_name:")
        user = input("Please input your username in yuque.com :")
        repo_id = input("Please input your repo_id in yuque.com :")
        token = input("Please input your token in yuque.com :")

        init_config({
            'headers': {
                "User-Agent": program_name,
                "X-Auth-Token": token
            },
            'user': user,
            'repo_id': repo_id
        })

    def start(self):
        while 1:
            command = input('society > ').split()

            order = command[0].upper()

            if order in self.nonparametric_command:
                self.nonparametric_command[order]()
            elif order in self.parametric_command:
                keyword = command[1]
                self.parametric_command[order](keyword)
            elif order == 'EXIT':
                break
            else:
                print('The orders supported now are (CREATE,FIND,REFRESH,UPDATE,EXIT) !')

    def _refresh_time(self):
        self.last_update_time = time.time()

    def refresh_cache(self):
        doc_list = api.get_doc_list()
        id_and_title = [(doc['id'], doc['title'])
                        for doc in doc_list['data']]

        for doc_id, title in id_and_title:
            doc = api.get_doc(doc_id)
            with codecs.open(NAME_FORMAT.format(data_dir=DATA_DIR,
                                                name=title,
                                                doc_id=doc_id), 'w', 'utf-8') as f:
                f.write(doc['data']['body'])
        self._refresh_time()

    def update(self):
        for filename in self.filenames:
            filepath = '{}/{}'.format(DATA_DIR, filename)
            modify_time = os.stat(filepath).st_mtime

            if modify_time > self.last_update_time:
                with codecs.open(filepath, 'r', 'utf-8') as f:
                    filename = filename.split('.')[0]  # remove suffix
                    title, doc_id = filename.split('-')
                    api.update_doc(doc_id,
                                   title=title,
                                   body=f.read())
        self._refresh_time()

    def create(self, title):
        api.create_doc(title)
        self.refresh_cache()

    def _open(self, filepath):
        os.startfile(filepath)

    def find(self, keyword):
        result = []
        index = 0

        for filename in self.filenames:
            filepath = '{}/{}'.format(DATA_DIR, filename)
            with codecs.open(filepath, 'r', 'utf-8') as f:
                if keyword in ' '.join([filename, f.read()]):
                    result.append((filename, filepath))
        if len(result) == 0:
            choose = input('No people you want! Create it? (y/n)')
            if choose == 'y':
                self.create(keyword)
            return
        elif len(result) > 1:
            table = PrettyTable(['Index', 'Filename'])
            [table.add_row([index, fileinfo[0]]) for index, fileinfo in enumerate(result)]
            print(table)

            index = int(input('Which index of file you want to modify:'))

        self._open(result[index][1])

    @property
    def filenames(self):
        return os.listdir(DATA_DIR)


if __name__ == '__main__':
    mkdir(DATA_DIR)
    Dispatch()
