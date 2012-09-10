import os
import re

from bs4 import BeautifulSoup
import lxml.html as lh

def html_mapper(key, value):
    with open(os.path.join('names', value), 'r') as infile:
        html = infile.read()
    yield value, html

def reducer(key, value):
    html = value.next()
    yield key, html

class ActorMapper(object):
    def __call__(self, key, value):
        actor = self.parse(value)
        actor.update({'record_type': 'actor', 'id': key})
        yield key, actor

    def parse(self, html):
        actor = {}
        soup = BeautifulSoup(html)
        doc = lh.document_fromstring(html)
        name_tag = soup.find(itemprop="name")
        if name_tag:
            actor['name'] = self.get_name_from_tag(name_tag)
        birthday_tag = soup.find(itemprop="birthDate")
        if birthday_tag:
            actor['birthday'] = self.get_birthday_from_tag(birthday_tag)
        birth_place_tag = soup.find('a', href=re.compile('\?birth_place=.+'))
        if birth_place_tag:
            actor['country'] = self.get_country_from_birthplace_tag(
                birth_place_tag)
        job_title_tags = soup.find_all('a', itemprop='jobTitle')
        if job_title_tags:
            actor['gender'] = self.get_gender_from_job_title_tags(
                job_title_tags)
        kf_elem_list = doc.xpath(r'//a[@itemprop="performerIn"]')
        actor['known_for'] = self.get_known_for(kf_elem_list)

        appears_elem_list = doc.xpath(r'//a[@itemprop="performerIn"]')
        actor['known_for'] = self.get_known_for(kf_elem_list)

        return actor


    def get_name_from_tag(self, name_tag):
        return re.sub(r'\s', ' ', name_tag.text.strip())


    def get_birthday_from_tag(self, birthday_tag):
       birthday = birthday_tag.get('datetime')
       return birthday

    def get_country_from_birthplace_tag(self, birth_place_tag):
        birth_place = birth_place_tag.text.split(',')
        if birth_place:
            return birth_place[-1].strip()

    def get_gender_from_job_title_tags(self, job_title_tags):
        job_titles = [tag.text.lower() for tag in job_title_tags]
        gender = '?'
        if 'actor' in job_titles:
            gender = 'M'
        elif 'actress' in job_titles:
            gender = 'F'
        # finally, guess director means male
        elif 'director' in job_titles:
            gender = 'M'
        return gender

    def get_known_for(self, element_list):
        known_for = []
        for element in element_list:
            title_id = element.get('href')[-10:-1]
            year_i_pos = element.text.rfind('(')
            title = element.text[:year_i_pos].strip()
            year = element.text[year_i_pos+1:-1]
            known_for.append({'title_id': title_id, 'year': year,
                             'title':title})
        return known_for

class MovieMapper(object):
    def __call__(self, key, value):
        movie = self.parse(value)
        movie.update({'record_type': 'movie', 'id': key})
        for actor in movie['cast']:
            key = actor['actor_id']
            yield key, str(movie)

    def parse(self, html):
        movie = {}
        doc = lh.document_fromstring(html)
        title_tag = doc.xpath(r'//h1[@itemprop="name"]')
        if title_tag:
            movie['title'] = self.get_title_from_tag(title_tag[0])
        published_tag = doc.xpath(r'//*[@itemprop="datePublished"]')
        if published_tag:
            movie['year'] = self.get_year_from_published_tag(published_tag[0])
        genre_tags = doc.xpath(r'//*[@itemprop="genre"]')
        if genre_tags:
            movie['genre'] = genre_tags[0].text
        cast_tags = doc.xpath(r'//td[@class="name"]')
        movie['cast'] = self.get_cast_from_tags(cast_tags)

        return movie


    def get_title_from_tag(self, name_tag):
        return re.sub(r'\s', ' ', name_tag.text.strip())


    def get_year_from_published_tag(self, published_tag):
        year = published_tag.get('datetime')[:4]
        return year

    def get_cast_from_tags(self, cast_tags):
        cast = []
        for element in cast_tags:
            actor_link = element.find('a')
            actor_id = actor_link.get('href')[-10:-1]
            name = actor_link.text.strip()
            cast.append({'actor_id': actor_id, 'name': name})
        return cast


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(html_mapper, reducer)
    job.additer(MovieMapper, reducer)
    job.run()
