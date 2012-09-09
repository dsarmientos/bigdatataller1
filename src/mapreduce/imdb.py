import re

from bs4 import BeautifulSoup


class ActorMapper(object):
    def __call__(self, key, value):
        actor = self.parse(value)
        actor_id = key[-9:]
        actor.update({'record_type': 'actor', 'id': actor_id})
        yield actor_id, unicode(actor)

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
        birth_place_tag = soup.find('a', href=re.compile('\?birth_place=.+'))
        if birth_place_tag:
            birth_place = birth_place_tag.text.split(',')
            if birth_place:
                actor['country'] = birth_place[-1].strip()
        job_title_tags = soup.find_all('a', itemprop='jobTitle')
        job_titles = [tag.text.lower() for tag in job_title_tags]
        gender = '?'
        if 'actor' in job_titles:
            gender = 'M'
        elif 'actress' in job_titles:
            gender = 'F'
        # finally, guess director means male
        elif 'director' in job_titles:
            gender = 'M'
        actor['gender'] = gender

        return actor


def reducer(key, value):
    html = value.next()
    yield key, html


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(ActorMapper, reducer)
    job.run()
