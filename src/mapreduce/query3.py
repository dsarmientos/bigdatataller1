import ast
import datetime

def reducer(key, value):
    value = value.next()
    yield key, value

class ActorFilterMapper(object):
    def __call__(self, key, value):
        id_, val = value.split('\t')
        record = ast.literal_eval(val)
        fields = ('birthday')
        has_fields = all([record.has_key(field) for field in fields])
        if has_fields and record.get('record_type', '') == 'actor':
            yield id_, record


class ActorQueryMapper(object):
    def __init__(self):
        date = self.params["date"]
        self.date = datetime.datetime.strptime(date,'%Y-%m-%d')
    def __call__(self, key, value):
        birthday = datetime.datetime.strptime(value['birthday'],'%Y-%m-%d')
        if self.date.month == birthday.month and self.date.day == birthday.day:
            yield key, str(value)


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(ActorFilterMapper, reducer)
    job.additer(ActorQueryMapper, reducer)
    job.run()
