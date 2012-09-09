import os
import re

from bs4 import BeautifulSoup

def html_mapper(key, value):
    with open(os.path.join('names', value), 'r') as infile:
        html = infile.read()
    yield value, html

def reducer(key, value):
    html = list(value)[0]
    yield key, html

class ActorMapper(object):
    def __call__(self, key, value):
        actor = self.parse(value)
        actor.update({'record_type': 'actor', 'id': key})
        yield key, actor

    def parse(self, html):
        actor = {}
        soup = BeautifulSoup(html)
        name_tag = soup.find(itemprop="name")
        if name_tag:
            actor['name'] = re.sub(r'\s', ' ', name_tag.text.strip())
        birthday_tag = soup.find(itemprop="birthDate")
        if birthday_tag:
           birthday = birthday_tag.get('datetime')
           actor['birthday'] = birthday
        return actor


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(html_mapper, reducer)
    job.additer(ActorMapper, reducer)
    job.run()
