import ast
import datetime

def reducer(key, value):
    value = value.next()
    yield key, value

class ActorFilterMapper(object):
    def __call__(self, key, value):
        id_, val = value.split('\t')
        record = ast.literal_eval(val)
        fields = ('country', 'birthday', 'known_for')
        has_fields = all([record.has_key(field) for field in fields])
        if has_fields and record['known_for'] and record.get('record_type', '') == 'actor':
            yield id_, record


class ActorQueryMapper(object):
    def __init__(self):
        self.now = datetime.datetime.now()
    def __call__(self, key, value):
        country = value.get('country', '')
        age = None
        last_five_years = False
        try:
            birthday = datetime.datetime.strptime(value.get('birthday', ''),
                                                  '%Y-%m-%d')
        except ValueError:
            pass
        else:
            time_delta = self.now - birthday
            age = int(time_delta.days / 365.25)
        know_for_years = [int(movie['year']) for movie in value['known_for']]
        year_diff = [self.now.year - year <= 5 for year in know_for_years]
        if year_diff and all(year_diff):
            last_five_years = True

        if country.find('USA') == -1 and last_five_years and age > 25:
            yield key, str(value)


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(ActorFilterMapper, reducer)
    job.additer(ActorQueryMapper, reducer)
    job.run()
