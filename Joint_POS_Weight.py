import sys

sys.path.insert(0, "conllu-perceptron-tagger")
sys.stderr = open("debugg.log", "w")
sys.stdout = open("CtrainF.conllu", "w")
# sys.stdout = open("feat.log", "w")

import random
from collections import defaultdict
import pickle

from PerceptronW import AveragedPerceptron
from copy import copy
from MaximumSpanning import maxspan
from tagger import PerceptronTagger

def _pc(n, d):
    return (float(n) / d) * 100

class PerceptronWeighter():
    '''Greedy Averaged Perceptron weighter, inspired by Matthew Honnibal.

    See more implementation details here:
        http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

    :param load: Load the pickled model upon instantiation.
    '''

    START = ['-START-', 'ROOT']
    END = ['-END-', '-END2-']

    def __init__(self, fname, load=False):
        # self.tagger = PerceptronTagger(tagfile, load=False)
        self.model = AveragedPerceptron()
        self.tagdict = {}
        self.classes = set()
        self.model_file = fname
        # self.tag_file = tagfile
        if load:
            self.load(self.model_file)
        print("Classes ==============\n",self.classes, file=sys.stderr)
        # if tagload:
        #     self.tagger.load(self.tag_file)

    def parse(self, corpus, tokenise=False):
        '''Tags a string `corpus`.'''
        # Assume untokenised corpus has \n between sentences and ' ' between words
        #s_split = SentenceTokenizer().tokenise if tokenise else lambda t: t.split('\n')
        #w_split = WordTokenizer().tokenise if tokenise else lambda s: s.split()

        reading = True
        for sentence in corpus:
            # print(c, n, '|||', sentence);
            # print(n, end='', file=sys.stderr)
            print("sentence =============", file=sys.stderr)
            print(sentence, file=sys.stderr)
            
            # removing unnecessary lines
            trimed_sentence = []
            V = [0]
            for token in sentence:
                if "." in token[0]:
                    continue
                V.append(int(token[0]))
                trimed_sentence.append(token)
            
            E = []
            F = {}
            context = self.START + [self._normalise(w[1]) for w in trimed_sentence] + self.END
            print("context ============\n", context, file=sys.stderr)
            tags = [w[3] for w in sentence]
            guessed_tags = {}
            POS_feats = {}
            for i in range(0, len(V)):
                for j in range(i + 1, len(V)):
                    print((i,j), file=sys.stderr)
                    dep = j
                    head = i
                    token = trimed_sentence[j-1]
                    depWord = token[1]
                    ########## depPOS = token[3]
                    
                    # head info
                    if i == 0:
                        headWord = "ROOT"
                        headPOS = "ROOT"
                    else:
                        h_token = trimed_sentence[i-1]
                        headWord = h_token[1]
                        headPOS = guessed_tags[head]

                    # prev retrieval
                    if j == 1:
                        prev = "ROOT"
                        prev2 = "START"
                    elif j == 2:
                        prev = guessed_tags[j-1]
                        prev2 = "ROOT"
                    else:
                        prev = guessed_tags[j-1]
                        prev2 = guessed_tags[j-2]

                    ########### depPOS
                    depPOS = self.tagdict.get(depWord)
                    # print("depPOS and word ==============\n", depPOS, depWord, file=sys.stderr)
                    if not depPOS:
                        depPOS = guessed_tags.setdefault(j, "current")
                        # print("TAGdict =========Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                        if depPOS == "current":
                            fPOS = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                            print("fPOS =================================\n", fPOS, file=sys.stderr)
                            depPOS = self.model.POS_predict(fPOS)
                            # print("Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                            guessed_tags[dep] = depPOS
                            POS_feats[dep] = fPOS
                    else:
                        guessed_tags[dep] = depPOS
                    # print("guessed_tags =============\n", guessed_tags, file=sys.stderr)
                    # break
                    # get features
                    feats = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                    # print(feats)
                    guess = self.model.predict(feats, depPOS)

                    e_tmp =[head, dep, guess]
                    E.append(e_tmp)
                    F[(head,dep)] = feats
                if i >= 2:
                    for j in range(1,i):
                        print((i,j), file=sys.stderr)
                        dep = j
                        head = i
                        token = trimed_sentence[j-1]
                        depWord = token[1]
                        ########## depPOS = token[3]
                        
                        # head info
                        if i == 0:
                            headWord = "ROOT"
                            headPOS = "ROOT"
                        else:
                            h_token = trimed_sentence[i-1]
                            headWord = h_token[1]
                            headPOS = guessed_tags[head]

                        # prev retrieval
                        if j == 1:
                            prev = "ROOT"
                            prev2 = "START"
                        elif j == 2:
                            prev = guessed_tags[j-1]
                            prev2 = "ROOT"
                        else:
                            prev = guessed_tags[j-1]
                            prev2 = guessed_tags[j-2]

                        ########### depPOS
                        depPOS = self.tagdict.get(depWord)
                        # print("depPOS and word ==============\n", depPOS, depWord, file=sys.stderr)
                        if not depPOS:
                            depPOS = guessed_tags.setdefault(j, "current")
                            # print("TAGdict =========Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                            if depPOS == "current":
                                fPOS = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                                # print("fPOS =================================\n", fPOS, file=sys.stderr)
                                depPOS = self.model.POS_predict(fPOS)
                                # print("Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                                guessed_tags[dep] = depPOS
                                POS_feats[dep] = fPOS
                        else:
                            guessed_tags[dep] = depPOS
                        # print("guessed_tags =============\n", guessed_tags, file=sys.stderr)
                        # break
                        # get features
                        feats = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                        # print(feats)
                        guess = self.model.predict(feats, depPOS)

                        e_tmp =[head, dep, guess]
                        E.append(e_tmp)
                        F[(head,dep)] = feats
                        
            # print("Gold V =================", file=sys.stderr)
            # print(G_V, file=sys.stderr)
            # print("Gold E =================", file=sys.stderr)
            # print(G_E, file=sys.stderr)
            # print("V ======================", file=sys.stderr)
            # print(V, file=sys.stderr)
            # print("E ======================", file=sys.stderr)
            # print(E, file=sys.stderr)
            # print("F =====================", file=sys.stderr)
            # print(F, file=sys.stderr)
            # print("==============================================================", file=sys.stderr)
            print("Maxspan", file=sys.stderr)
            M = maxspan(V,E)
            print(M, file=sys.stderr)
            
            if M:
                print("#\n#", file=sys.stdout)
            for token in sentence:
                if "." in token[0]:
                    p_str = ""
                    i = 0
                    while i < len(token):
                        if i == 6:
                            tmp = str(token[i])
                        else:
                            tmp = token[i]
                        p_str += tmp + "\t"
                        i += 1
                    p_str = p_str[0:-1]
                    print(p_str, file=sys.stdout)
                elif token ==[]:
                    print("\n", file=sys.stdout)
                else:
                    dep = int(token[0])
                    for m in M:
                        if m[1] == dep:
                            # token[]
                            p_str = ""
                            i = 0
                            while i < len(token):
                                if i == 3:
                                    tmp = guessed_tags[dep]
                                elif i == 6:
                                    tmp = str(m[0])
                                    # print(tmp, file=sys.stderr)
                                else:
                                    tmp = token[i]
                                p_str += tmp + "\t"
                                i += 1
                            p_str = p_str[0:-1]
                            print(p_str, file=sys.stdout)
            if M:
                print("", file=sys.stdout)

        return 

    def predict(self,sentence):
        '''
        predict weights for a graph
        '''

    def train(self, sentences, tag_loc=None, save_loc=None, nr_iter=5):
        '''Train a model from sentences, and save it at ``save_loc``. ``nr_iter``
        controls the number of Perceptron training iterations.

        :param sentences: A list of 10-value tuples
        :param save_loc: If not ``None``, saves a pickled model in this location.
        :param nr_iter: Number of training iterations.
        '''
        # self._make_tagdict(sentences)
        self._make_tagdict(sentences)
        self.model.classes = self.classes
        # print("classes =============\n", self.classes)
        # print("tagdict======================\n",self.tagdict)
        # self.model.classes = self.classes
        for iter_ in range(nr_iter):
            c = 0
            n = 0
            # for words,tags in sentences:
            for sentence in sentences:
                # print(c, n, '|||', sentence);
                print(n, end='', file=sys.stderr)
                print("sentence =============", file=sys.stderr)
                print(sentence, file=sys.stderr)

                ###### Gold tree #######
                G_V = [0]
                G_E = []
                trimed_sentence = []
                for token in sentence:
                    if "." in token[0]:
                        continue
                    trimed_sentence.append(token)
                    dependent = int(token[0])
                    # print(dependent)
                    head = int(token[6])

                    G_V.append(dependent)
                    e_tmp =(head, dependent)
                    G_E.append(e_tmp)
                
                ###### Guessing weights ##############
                V = copy(G_V)
                E = []
                F = {}
                context = self.START + [self._normalise(w[1]) for w in trimed_sentence] + self.END
                print("context ============\n", context, file=sys.stderr)
                tags = [w[3] for w in sentence]
                guessed_tags = {}
                POS_feats = {}
                for i in range(0, len(V)):
                    for j in range(i + 1, len(V)):
                        print((i,j), file=sys.stderr)
                        dep = j
                        head = i
                        token = trimed_sentence[j-1]
                        depWord = token[1]
                        ########## depPOS = token[3]
                        
                        # head info
                        if i == 0:
                            headWord = "ROOT"
                            headPOS = "ROOT"
                        else:
                            h_token = trimed_sentence[i-1]
                            headWord = h_token[1]
                            headPOS = guessed_tags[head]

                        # prev retrieval
                        if j == 1:
                            prev = "ROOT"
                            prev2 = "START"
                        elif j == 2:
                            prev = guessed_tags[j-1]
                            prev2 = "ROOT"
                        else:
                            prev = guessed_tags[j-1]
                            prev2 = guessed_tags[j-2]

                        ########### depPOS
                        depPOS = self.tagdict.get(depWord)
                        # print("depPOS and word ==============\n", depPOS, depWord, file=sys.stderr)
                        if not depPOS:
                            depPOS = guessed_tags.setdefault(j, "current")
                            # print("TAGdict =========Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                            if depPOS == "current":
                                fPOS = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                                # print("fPOS =================================\n", fPOS, file=sys.stderr)
                                depPOS = self.model.POS_predict(fPOS)
                                # print("Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                                guessed_tags[dep] = depPOS
                                POS_feats[dep] = fPOS
                        else:
                            guessed_tags[dep] = depPOS
                        # print("guessed_tags =============\n", guessed_tags, file=sys.stderr)
                        # break
                        # get features
                        feats = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                        # print(feats)
                        guess = self.model.predict(feats, depPOS)

                        e_tmp =[head, dep, guess]
                        E.append(e_tmp)
                        F[(head,dep)] = feats
                    if i >= 2:
                        for j in range(1,i):
                            print((i,j), file=sys.stderr)
                            dep = j
                            head = i
                            token = trimed_sentence[j-1]
                            depWord = token[1]
                            ########## depPOS = token[3]
                            
                            # head info
                            if i == 0:
                                headWord = "ROOT"
                                headPOS = "ROOT"
                            else:
                                h_token = trimed_sentence[i-1]
                                headWord = h_token[1]
                                headPOS = guessed_tags[head]

                            # prev retrieval
                            if j == 1:
                                prev = "ROOT"
                                prev2 = "START"
                            elif j == 2:
                                prev = guessed_tags[j-1]
                                prev2 = "ROOT"
                            else:
                                prev = guessed_tags[j-1]
                                prev2 = guessed_tags[j-2]

                            ########### depPOS
                            depPOS = self.tagdict.get(depWord)
                            # print("depPOS and word ==============\n", depPOS, depWord, file=sys.stderr)
                            if not depPOS:
                                depPOS = guessed_tags.setdefault(j, "current")
                                # print("TAGdict =========Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                                if depPOS == "current":
                                    fPOS = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                                    # print("fPOS =================================\n", fPOS, file=sys.stderr)
                                    depPOS = self.model.POS_predict(fPOS)
                                    # print("Guessed depPOS and word =============\n", depPOS, depWord, file=sys.stderr)
                                    guessed_tags[dep] = depPOS
                                    POS_feats[dep] = fPOS
                            else:
                                guessed_tags[dep] = depPOS
                            # print("guessed_tags =============\n", guessed_tags, file=sys.stderr)
                            # break
                            # get features
                            feats = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                            # print(feats)
                            guess = self.model.predict(feats, depPOS)

                            e_tmp =[head, dep, guess]
                            E.append(e_tmp)
                            F[(head,dep)] = feats
                            # break
                            # dep = j
                            # head = i
                            # token = trimed_sentence[j-1]
                            # depWord = token[1]
                            # depPOS = token[3]

                            # # head info
                            # h_token = trimed_sentence[i-1]
                            # headWord = h_token[1]
                            # headPOS = h_token[3]

                            # # prev retrieval
                            # if j == 1:
                            #     prev = "ROOT"
                            #     prev2 = "START"
                            # elif j == 2:
                            #     prev = trimed_sentence[j-2][3]
                            #     prev2 = "ROOT"
                            # else:
                            #     prev = trimed_sentence[j-2][3]
                            #     prev2 = trimed_sentence[j-3][3]
                            
                            # # break

                            # # get features
                            # feats = self._get_features(self._normalise(depWord), prev, prev2, headPOS, self._normalise(headWord), depPOS, context, dep, head)
                            # # print(feats)
                            # guess = self.model.predict(feats)

                            # e_tmp =[head, dep, guess]
                            # E.append(e_tmp)
                            # F[(head,dep)] = feats
                print("Gold V =================", file=sys.stderr)
                print(G_V, file=sys.stderr)
                print("Gold E =================", file=sys.stderr)
                print(G_E, file=sys.stderr)
                print("V ======================", file=sys.stderr)
                print(V, file=sys.stderr)
                print("E ======================", file=sys.stderr)
                print(E, file=sys.stderr)
                print("F =====================", file=sys.stderr)
                print(F, file=sys.stderr)
                print("==============================================================", file=sys.stderr)
                print("Maxspan", file=sys.stderr)
                M = maxspan(V,E)
                print(M, file=sys.stderr)

                '''scores'''
                # Caluculate the score for M
                M_score = 0
                for m in M:
                    if m in G_E:
                        c += 1
                    n += 1
                    # M_score += self.model.predict(F[m])
                
                # Calculate the score for G_E
                # G_score = 0
                # for g in G_E:
                #     G_score += self.model.predict(F[g])

                # print("M score ====================\n", M_score, file=sys.stderr)
                # print("G score ====================\n", G_score, file=sys.stderr)
                

                # g_feat = []
                # for g in G_E:
                #     g_feat += F[g]
                # print("G feat ====================\n", g_feat)
                # feat = []
                # for m in M:
                #     feat += F[m]
                # print("feat ======================\n", feat)

                # dictionary of features, keys = dependent
                GM_dep_feat = {}
                for g in G_E:
                    for m in M:
                        if g[1] == m[1]:
                            GM_dep_feat[g[1]] = [F[g].keys(),F[m].keys()]
                # print("GM_feat =====================\n", GM_dep_feat)

                # GM_head_feat = {}
                # for g in G_E:
                #     for m in M:
                #         if g[0] == m[0]:
                #             GM

                # count = 0
                # for m in M:
                #     if m in G_E:
                #         count += 1
                # print("count ===================\n", count)

                '''update for POS'''
                for k in POS_feats.keys():
                    self.model.POS_update(tags[k-1],guessed_tags[k], POS_feats[k])
                # print(self.model.weights)

                ###### update for weighting
                for k in GM_dep_feat.keys():
                    gold = GM_dep_feat[k][0]
                    guessed = GM_dep_feat[k][1]
                    # print(guessed_tags[k])
                    self.model.update(gold, guessed, tags[k-1], guessed_tags[k])
                # for m in M:
                #     if m in G_E:
                #         self.model.update(F[m], 1.0)
                #         c += 1
                #     else:
                #         self.model.update(F[m], -1.0)
                #     n += 1
                # for m in G_E:
                #     if not (m in M):
                #         self.model.update(F[m],1.0)
            # break
                
            random.shuffle(sentences)
            print()
            print("Iter {0}: {1}/{2}={3}".format(iter_, c, n, _pc(c, n)))
        # print("\nweights ============", file=sys.stderr)
        # print(self.model.weights, file=sys.stderr)
        self.model.average_weights()
        # Pickle as a binary file
        if save_loc is not None:
            pickle.dump((self.model.weights, self.tagdict, self.classes),
                         open(save_loc, 'wb'), -1)

        print("\nweights ============", file=sys.stderr)
        print(self.model.weights, file=sys.stderr)
        return None

    def load(self, loc):
        '''Load a pickled model.'''
        try:
            w_td_c = pickle.load(open(loc, 'rb'))
        except IOError:
            print("Missing " +loc+" file.")
            sys.exit(-1)
        self.model.weights, self.tagdict, self.classes = w_td_c
        self.model.classes = self.classes
        return None

    def _normalise(self, word):
        '''Normalisation used in pre-processing.

        - All words are lower cased
        - Digits in the range 0000-2100 are represented as !YEAR;
        - Other digits are represented as !DIGITS

        :rtype: str
        '''
        if '-' in word and word[0] != '-':
            return '!HYPHEN'
        elif word.isdigit() and len(word) == 4:
            return '!YEAR'
        elif word[0].isdigit():
            return '!DIGITS'
        else:
            return word.lower()
    
    # def _get_features(self, i, word, context, prev, prev2, headPOS, headW, dependentPOS):
    def _get_features(self, depWord, prev, prev2, headPOS, headWord, depPOS, context, dep, head):
        '''Map tokens into a feature representation, implemented as a
        {hashable: float} dict. If the features change, a new model must be
        trained.
        '''
        # print("Context ===============")
        # print(context)
        # print("Word =================")
        # print(depWord)
        def add(name, *args):
            # print((name,) + tuple(args), file=sys.stdout)
            features[' '.join((name,) + tuple(args))] += 1

        dep += len(self.START) - 1
        features = defaultdict(int)
        # It's useful to have a constant feature, which acts sort of like a prior
        add('bias')
        add('i suffix', depWord[-3:])
        add('i pref1', depWord[0])
        add('i-1 tag', prev)
        add('i-2 tag', prev2)
        add('i tag+i-2 tag', prev, prev2)
        # print("dep =======")
        # print(dep)
        # print("context ==========")
        # print(context)
        add('i word', context[dep])
        add('i-1 tag+i word', prev, context[dep])
        add('i-1 word', context[dep-1])
        add('i-1 suffix', context[dep-1][-3:])
        add('i-2 word', context[dep-2])
        add('i+1 word', context[dep+1])
        add('i+1 suffix', context[dep+1][-3:])
        add('i+2 word', context[dep+2])
        ##########  features for edge weighting
        add('head POS', headPOS)
        add("head word", headWord)
        add("head POS word", headPOS, headWord)
        add('dependent POS', depPOS)
        add('dependent word', depWord)
        add('dep POS word', depPOS, depWord)
        add("head dep POS", headPOS, depPOS)
        add("head dep Word", headWord, depWord)
        add("|head - dep|", str(abs(head - dep)))
        add("dep - head", str(dep-head))
        ######### additional
        add('p-word, p-pos, c-word, c-pos', headWord, headPOS, depWord, depPOS)
        add('p-pos, c-word, c-pos', headPOS, depWord,depPOS)
        add('p-word, c-word, c-pos', headWord, depWord, depPOS)
        add('p-word, p-pos, c-pos', headWord, headPOS, depPOS)
        add('p-word, p-pos, c-word', headWord, headPOS, depWord)

        #print(word, '|||', features)
        return features
    
    def _make_tagdict(self, sentences):
        '''Make a tag dictionary for single-tag words.'''
        counts = defaultdict(lambda: defaultdict(int))
        # for words, tags in sentences:
        for sentence in sentences:
            for token in sentence:
                word = token[1]
                tag = token[3]
                counts[word][tag] += 1
                self.classes.add(tag)
        freq_thresh = 20
        ambiguity_thresh = 0.97
        for word, tag_freqs in counts.items():
            tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
            n = sum(tag_freqs.values())
            # Don't add rare words to the tag dictionary
            # Only add quite unambiguous words
            if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
                self.tagdict[word] = tag


###############################################################################

def parser(corpus_file, model_file):
    ''' tag some text. 
    :param corpus_file is a file handle
    :param model_file is a saved model file
    '''
    corpus_file = open(corpus_file, "r")

    sentences = []
    for sent in corpus_file.read().split('\n\n'):
        sentence = []
        for token in sent.split('\n'):
            if token.strip() == '':
                continue
            if token[0] == '#':
                continue
            sentence.append(tuple(token.strip().split('\t')))
        sentences.append(sentence)

    t = PerceptronWeighter(model_file, load=True)
    t.parse(sentences)

def trainer(corpus_file, model_file):
    ''' train a model 
    :param corpus_file is a file handle
    :param model_file is a saved model file
    '''
    corpus_file = open(corpus_file, "r")

    t = PerceptronWeighter(model_file, load=False)
    sentences = []
    for sent in corpus_file.read().split('\n\n'):
        sentence = []
        for token in sent.split('\n'):
            if token.strip() == '':
                continue
            if token[0] == '#':
                continue
            sentence.append(tuple(token.strip().split('\t')))
        sentences.append(sentence)
    
    # print(sentences[0])
    t.train(sentences, save_loc=model_file, nr_iter=7)

if len(sys.argv) == 3 and sys.argv[1] == '-t':
    trainer(sys.stdin, sys.argv[2])    
elif len(sys.argv) == 2:
    tagger(sys.stdin, sys.argv[1])
# else:
#     print('tagger.py [-t] model.dat');
#     sys.exit(-1)