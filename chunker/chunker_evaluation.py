import nltk
from nltk.corpus.reader import ConllChunkCorpusReader


############################################################
#Trigram Chunker
############################################################


#Chunker
#http://www.nltk.org/book/ch07.html
#Evaluation version
class TrigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
        self.tagger = nltk.TrigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)

#Lets define the ConllChunkCorpusReader corpus. Each of the files should begin by "trainer_"
conllreader = ConllChunkCorpusReader('conlleac/', 'trainer_.*', ('VND', 'PDT', 'VSN'))

#We train a chunker for each corpus file.
#trainer_product trains with the goal of recognize NE elements inside visited pages titles
train_sents_product = conllreader.chunked_sents('trainer_product_train', chunk_types=['VND', 'PDT', 'VSN'])
chunkerTrigram_product = TrigramChunker(train_sents_product)

#We use the same ConllChunkCorpusReader corpus to train a tagger
train_tagger_product = conllreader.tagged_sents('trainer_product_train')
tagger_t0 = nltk.DefaultTagger('NNP')
tagger_t1 = nltk.UnigramTagger(train_tagger_product, backoff=tagger_t0)

#Evaluating the tagger
print(tagger_t1.evaluate(conllreader.tagged_sents('trainer_product_test')))
#Evaluating the chunker
test_sents_product = conllreader.chunked_sents('trainer_product_test', chunk_types=['VND', 'PDT', 'VSN'])
print(chunkerTrigram_product.evaluate(test_sents_product))

'''
TRAINER PRODUCT ['VND', 'PDT', 'VSN', 'FTR'] (f-measure of 72%)
ChunkParse score:
    IOB Accuracy:  72.0%
    Precision:     58.2%
    Recall:        48.8%
    F-Measure:     53.1%

TRAINER PRODUCT NO FTR ['VND', 'PDT', 'VSN']
ChunkParse score:
    IOB Accuracy:  95.4%
    Precision:     79.2%
    Recall:        79.9%
    F-Measure:     79.6%
'''

#trainer_product trains with the goal of recognize NE elements inside visited pages bodies
#train_sents_default = conllreader.chunked_sents('trainer_default', chunk_types=['VND', 'PDT', 'VSN', 'TSW', 'SIM', 'WHT', 'DIM', 'HRD', 'RAM', 'PCS', 'PCT', 'CAM', 'SCR', 'PXL', 'CTY', 'OTR'])
#chunkerTrigram_default = TrigramChunker(train_sents_default)
