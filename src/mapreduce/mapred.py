import datetime

class BirthDayMapper(object):
    def __call__(self, key, value):
        # value = html site for actor
        #parsed_html = self.parse(value)
        #birthday = parsed_html['birthday']
        #actor = parsed_html['name']
        #edad = parsed_html['age']
        yield value, 1

    def parse(self, html):
        from bs4 import BeautifulSoup
        import datetime
        import re
        parsed_html = {'name':None, 'age':11, 'birthday':None}
        soup = BeautifulSoup(html)
        name_tag = soup.find(itemprop="name")
        if name_tag:
            parsed_html['name'] = re.sub(r'\s', ' ', name_tag.text)
        birthday_tag = soup.find(itemprop="birthDate")
        if birthday_tag and False:
            #birthday = birthday_tag.get('datetime')

            dt = datetime.datetime.strptime(birthday, '%Y-%m-%d')
            parsed_html['birthday'] = dt.date()
        return parsed_html


class FilterMapper(object):
    def __init__(self, date=None):
        import datetime
        self.date = datetime.date.today()

    def __call__(self, key, value):
        actor, birthday = key
        date = self.date
        if birthday and birthday.day == date.day and birthday.month == date.month:
            yield actor, {'birthday': birthday, 'age': value}

def reducer(key, values):
    yield key, sum(values)

if __name__ == "__main__":
    import datetime
    import dumbo
    job = dumbo.Job()
    job.additer(BirthDayMapper, reducer)
    job.run()
