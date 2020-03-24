from libvoikko import Voikko
voikko = Voikko("fi")

# from https://stackoverflow.com/a/1988826/95357


class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        # Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[args]


@Memoize
def analyze_word(form):
    return voikko.analyze(form)
