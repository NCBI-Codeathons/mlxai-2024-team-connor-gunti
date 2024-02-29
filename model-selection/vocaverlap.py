from collections import defaultdict

def dofd():
    return defaultdict(int)

class VocabOverlap:
    def __init__(self, data):
        self.info = {}

        self.freqs = defaultdict(dofd)
        for name, text in data:
            for word in text.split():
                self.freqs[name][word] += 1
                
        self.wfreqs = {}
        for attr, tokens in self.freqs.items():
            self.wfreqs[attr] = sorted(tokens.items(), key=lambda x: x[1], reverse=True)
            
    def apply(self, fn_oov):
        '''
        fn_oov - function getting a token and returning True if it is OOV
        '''
        
        for n, v in self.wfreqs.items():
            oov_total = 0
            oov, voc = [], []
            for t, w in v:
                if fn_oov(t):
                    oov.append((t, w))
                    oov_total += w
                else:
                    voc.append((t, w))
                    
            self.info[n] = {
                            'tokens': sum([p[1] for p in v]),
                            'uniq': len(v),
                            'oov_tokens': oov_total,
                            'oov_uniq': len(oov),
                            'voc': voc,
                            'oov': oov }
        return self
