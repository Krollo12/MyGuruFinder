import sys
import os
import gensim
import nltk
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def NearestNeighbourFinder(guru,train=False):
    data, titles_list = guru.nearest()
    tagger = titles_list.index(guru.wikipage)

    #Train model if train = True (Set in MyGuruFinder script)
    if train:
        # A single document, made up of `words` (a list of unicode string tokens)
        #and `tags` (a list of tokens)
        # Make all words lower-case and tokenize the words to split off punctuation
        # tags: A number representing the article
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

        # Build the Doc2Vec model with chosen parameters
        model = Doc2Vec(vector_size=40,
                        alpha=0.025,
                        min_alpha=0.00025,
                        window = 3,
                        min_count = 2,
                        dm =1)

        # Builds a vocabulary over the frequently occuring words.
        model.build_vocab(tagged_data)

        # Define the training session
        max_epochs = 40
        print("Starting training...")
        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # decrease the learning rate
            model.alpha -= 0.0002
            # fix the learning rate, no decay
            model.min_alpha = model.alpha
        print('Training done')
        model.save("d2v.model")
        print("Model Saved")

    # Load pretrained model
    model= Doc2Vec.load("d2v.model")

    # Find the most similar articles using the tag index
    similar_doc = model.docvecs.most_similar(tagger)

    # Make lists to return
    sim_list = [str(titles_list[int(similar_doc[0][0])]),str(titles_list[int(similar_doc[1][0])]),str(titles_list[int(similar_doc[2][0])])]
    score_list =  [similar_doc[0][1], similar_doc[1][1], similar_doc[2][1]]
    return sim_list, score_list
