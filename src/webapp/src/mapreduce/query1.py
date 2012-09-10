import ast
import datetime
import collections
import re


class ActorFilter(object):
    def __init__(self):
        self.name_filter = self.params["name"].lower()
    def __call__(self, key, value):
        id_, val = value.split('\t')
        record = ast.literal_eval(val)
        fields = ('name',)
        has_fields = all([record.has_key(field) for field in fields])
        if has_fields and record.get('record_type', '') == 'actor':
            if re.search(r'.*%s.*' % (self.name_filter),
                        record['name'].lower()):
                yield id_, [('A', record)]

class MovieFilter(object):
    def __call__(self, key, value):
        id_, val = value.split('\t')
        record = ast.literal_eval(val)
        if record.get('record_type', '') == 'movie':
            yield id_, record

class MovieCountGender(object):
    def __init__(self):
        # gender_index.txt is distributed to all nodes
        with open('gender_index.txt', 'r') as index_file:
            gender_index = index_file.read()
        self.gender_index = {}
        for line in gender_index.split('\n'):
            if line:
                actor, gender = line.split('\t')
                self.gender_index[actor.strip("'")] = gender.strip("'")

    def __call__(self, key, value):
        for movie in value['cast']:
            actor_id = movie['actor_id']
            yield key, (self.gender_index.get(actor_id, '?'), 1)

class ResultsMapper(object):
    def __call__(self, key, value):
        yield key, value


def reducer(key, value):
    value = value.next()
    yield key, value


def join_reducer(key, value):
    values = list(value)
    if len(values) == 2:
        val1 = values[0]
        val2 = values[1]
        if val1[0][0] == 'A':
            info = val1[0][1]
            count = val2[0][1]
        else:
            info = val2[0][1]
            count = val1[0][1]
        info.update({'colleagues':count})
        yield key, str(info)


def gender_sum_reducer(key, value):
    counter = collections.defaultdict(lambda: 0)
    for val in value:
        gender, count = val
        counter[gender] += count
    yield key, [('C', counter.items())]


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    o0 = job.additer(MovieFilter, reducer, input=job.root)
    o1 = job.additer(MovieCountGender, gender_sum_reducer, input=o0)
    o2 = job.additer(ActorFilter, reducer, input=job.root)
    o3 = job.additer(ResultsMapper, join_reducer, input=[o1, o2])
    job.run()
