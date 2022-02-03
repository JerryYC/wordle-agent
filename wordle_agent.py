def _match(v1, v2):
    pat = ["","","","",""]
    count = {}
    for c in v2:
        count[c] = count.get(c,0) + 1
        
    for idx, c in enumerate(v1):
        if v1[idx] == v2[idx]:
            pat[idx] = "A"
            count[c] -= 1
    
    for idx, c in enumerate(v1):
        if pat[idx]=="":
            if v1[idx] in v2 and count[c]>0:
                count[c] -= 1
                pat[idx] = "B"
            else:
                pat[idx] = "_"
    return "".join(pat)

def classify_word(word, vocab, pattern_idx):
    result = []
    for i in range(3**5):
        result.append([])

    for v in vocab:
        pat = _match(word, v)
        result[pattern_idx[pat]].append(v)


    return result, max([len(r)**2 for r in result])


class wordle_agent:
    def __init__(self, dicitonary_path = "./vocab"):
        f = open(dicitonary_path, "r")
        self.vocab = f.read().split("\n")
        f.close()
        self.prior = self.vocab[::]
        self.pattern_idx = {}
        pref = [""]
        new_pref = []
        for _ in range(5):
            for s in pref:
                for c in ['A','B','_']:
                    new_pref += [s + c]
            pref = new_pref[::]
            new_pref = []
        for i, pattern in enumerate(pref):
            self.pattern_idx[pattern] = i
    def possible_words(self):
        return self.prior
            
    def update_prior(self, guess, result):
        guess = guess.lower()
        tmp = self.prior[::]
        self.prior = []
        for v in tmp:
            if result == _match(guess, v):
                self.prior += [v]
        print(f'{len(self.prior)} possible words left')
    
    def act(self):
        best_score = len(self.prior)**2
        best_guess = ""
        best_result = []
        for v in self.vocab:
            r, score = classify_word(v, self.prior, self.pattern_idx)
            if score < best_score or (score == best_score and v in self.prior):
                best_guess = v
                best_score = score
                best_result = r[::]
        print(f'Best guess is {best_guess}')