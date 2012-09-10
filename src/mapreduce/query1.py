import ast
import datetime
import collections


class MovieFilter(object):
    def __call__(self, key, value):
        id_, val = value.split('\t')
        record = ast.literal_eval(val)
        fields = ('cast')
        has_fields = all([record.has_key(field) for field in fields])
        if has_fields and record.get('record_type', '') == 'movie':
            yield id_, record

class MovieCountGender(object):
    def __init__(self):
        # gender_index.txt is distributed to all nodes
        with open('gender_index.txt', 'r') as index_file:
            gender_index = index_file.read()
        self.gender_index = {}
        for line in gender_index:
            actor, gender = line.split('\t')
            self.gender_index[actor] = gender
    def __call__(self, key, value):
        for movie in value['cast']:
            actor_id = movie['actor_id']
            if actor_id in self.gender_index:
                yield actor_id, (self.gender_index[actor_id], 1)


def reducer(key, value):
    value = value.next()
    yield key, value

def gender_sum_reducer(key, value):
    counter = collections.defaultdict(lambda: 0)
    for val in values:
        gender, count = val
        counter[gender] += count
    yield key, counter.items()


if __name__ == "__main__":
    import dumbo
    job = dumbo.Job()
    job.additer(MovieFilter, reducer)
    job.additer(MovieCountGender, gender_sum_reducer)
    job.run()
