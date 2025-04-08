def get_id():
    for i in range(1,150):
        yield i


next_id = get_id().__next__()