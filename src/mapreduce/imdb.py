import datetime
import os

from bs4 import BeautifulSoup

def html_mapper(key, value):
    with open(os.path.join('names', value), 'r') as infile:
        html = infile.read()
    yield value, html

def reducer(key, value):
    html = list(value)[0]
    yield key, html

class ActorDataMapper(object):
    def __call__(self, key, value):
        actor = self.parse(value)
        birthday = actor['birthday']
        name = actor['name']
        edad = actor['age']
        yield (name, birthday), actor

    def parse(self, html):
        import datetime
        import re
        parsed_html = {'name':None, 'age':None, 'birthday':None}
        soup = BeautifulSoup(html)
        name_tag = soup.find(itemprop="name")
        if name_tag:
            parsed_html['name'] = re.sub(r'\s', ' ', name_tag.text)
        birthday_tag = soup.find(itemprop="birthDate")
        if birthday_tag:
           birthday = birthday_tag.get('datetime')
           dt = datetime.datetime.strptime(birthday, '%Y-%m-%d')
           parsed_html['birthday'] = birthday
        return parsed_html


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(html_mapper, reducer)
    job.additer(ActorDataMapper, reducer)
    job.run()
