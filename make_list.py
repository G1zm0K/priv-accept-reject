def make_wordlist(input):
    accept_words_list = []
    for w in open(input, "r").read().splitlines():
        if not w == "":
            accept_words_list.append(w)
    return accept_words_list