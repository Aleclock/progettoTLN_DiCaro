# **Content to form**

<br/><br/>

>L’esercitazione prevede l’implementazione della teoria di P. Hanks:

>1.	Scegliere un verbo transitivo (minimo valenza = 2);
>2.	Recuperare da un corpus n istanze in cui esso viene usato;
>3.	Effettuare parsing e disambiguazione
>4.	Usare i super sensi di WordNet sugli argomenti (subj e obj) del verbo scelto;
>5.	Aggregare i risultati, calcolare le frequenze, stampare i cluster semantici ottenuti.
>   *	Un **cluster semantico** è inteso come combinazione dei semantic types (ad esempio coppie di sem_types se valenza = 2)



<br/>

# 0. Scelta del verbo 

TODO

<br/><br/>

# 1. Ottenere le istanze contenenti il verbo scelto

Le istanze vengono recuperate dal Brown Corpus. La funzione `extractBrownSentences()` permette di estrarre tutte le frasi dal corpus (attraverso la funzione `brown.sents()`).

Successivamente si cicla su ogni termine di ogni frase estratta e si determina il part-of-speech della frase (`nltk.pos_tag(sent)`). Nel caso in cui il TAG del termine sia un verbo, allora viene lemmatizzato. Nel caso in cui il termine sia uguale al verbo scelto la frase viene selezionata e aggiunta alla lista di frasi da analizzare.

~~~~python
def extractBrownSentences(verb, verbs_pos):
    lemmatizer = WordNetLemmatizer()

    list_sent = brown.sents() #  Return all sentences in the corpus or in the specified file(s).
    sentences = []
    for sent in list_sent:
        tags = dict(nltk.pos_tag(sent))
        for word in sent:
            if tags[word] in verbs_pos:
                word = lemmatizer.lemmatize(word, 'v')
                if word == verb:
                    sentences.append(sent)
    return sentences
~~~~

Siccome questa operazione richiede parecchio tempo per essere eseguita, il risultato (le frasi estratte) vengono salvate nel file *sentences.txt* e lette ad ogni esecuzione.

<br/><br/>

## 2. Parsing e disambiguazione

La teoria di Hanks si basa sull'idea che il verbo sia la radice del significato, in quanto non esistono espressioni senza verbo. Ad ogni verbo viene associata una valenza, ovvero il numero di argomenti necessari per il verbo. In base al numero di argomenti che un verbo richiede, in certi casi è possibile differenziarne il
significato.

<br/>

Dopo aver ottenuto le frasi contenenti il verbo scelto, è necessario fare il parsing e la disambiguazione.

Per ogni frase si determina l'albero a dipendenze grazie alla funzione `dependencyParsing()`. Successivamente si utilizza `spaCy`[1] per determinare il soggetto e l'oggetto associato al verbo scelto (gli argomenti del verbo).

Dato l'albero a dipendenze della frase (`tree`), i tre elementi si determinano come segue:

* `verbAddress` è il termine nell'albero il quale corrisponde ai verbi scelti;
* `subjects` è una lista contenente tutti i termini della frase il cui reggente (`head`) è `verbAddress`, la cui relazione sintattica (`dep_`) è `nsubj` e il cui part-of-speech (`tag_`) è `NN`;
* `objects` è una lista contenente tutti i termini della frase il cui reggente (`head`) è `verbAddress`, la cui relazione sintattica (`dep_`) è `obj` e il cui part-of-speech (`tag_`) è `NN`;

~~~~python
def extractVerbSubjObj (verb, tree):
    verbAddress = next(t.text for t in tree if t.text in verb)
    subjects = list(t.text for t in tree if str(t.head) == verbAddress and "nsubj" in t.dep_ and "NN" in t.tag_)
    objects = list(t.text for t in tree if str(t.head) == verbAddress and "obj" in t.dep_ and "NN" in t.tag_)
    return subjects, objects
~~~~

In questo modo è possibile determinare i filler (soggetti nominali e oggetti) del verbo scelto [2].

Nel caso in cui il verbo abbia valenza 2 e quindi entrambi i filler sono presenti, si calcola attraverso l'algoritmo di Lesk il miglior WordNet synset associato ad ogni filler. L'algoritmo di Lesk prende in input un termine polisemico e la frase in cui occorre e restituisce il senso migliore.

Per ogni senso associato al termine da disambiguare (ottenuto tramite `wn.synsets(word)`), la funzione `lesk()` calcola l'overlap tra i contesti della frase e del synset. I due contesti sono ottenuti con un approccio bag-of-words e sono composti da:

* `ctx_sentence`: composto da tutti i termini della frase soggetti a pre-processing (tokenizzazione, rimozione punteggiatura e stopwords, lemmatizzazione). 
* `ctx_synset`: composto da tutti i termini presenti nella definizione e negli esempi soggetti a pre-processing (tokenizzazione, rimozione punteggiatura e stopwords, lemmatizzazione). 

L'algoritmo ritorna il senso migliore, ovvero il synset che ha ottenuto l'overlap maggiore.

<br/>

Successivamente, nel caso in cui l'algoritmo di Lesk abbia ritornato un senso, si determinano i tipi semantici, ovvero delle generalizzazioni concettuali strutturate come una gerarchia. Questo procedimento viene fatto in quanto il significato di un verbo dipende dagli argomenti e dai tipi semantici ad esso associati.
Il tipo semantico di un synset si ottiene determinando il suo super senso (attraverso la funzione `synset.lexname()` [3]).

Infine gli argomenti del verbo con valenza 2 vengono aggiunti ad una lista (`instances`) in modo da semplificare il calcolo delle frequenze. `instances` è una lista contenente tutte le istanze (frasi) in cui il verbo ha valenza 2 (dove è presente sia il soggetto che l'oggetto del verbo).


<br/><br/>

## 3. Calcolo delle frequenze

L'ultimo step prevede l'aggregazione dei risultati attraverso il calcolo delle frequenze. Queste vengono calcolate con la funzione `getFrequency()`, la quale cicla su tutti gli elementi della lista istance `instances` e calcola la frequenza dei valori dei supersensi relativi ai filler desiderati ()

~~~~python
count = collections.Counter([s for i in instances for s in i.arg]).most_common()
~~~~

Successivamente viene calcolata in maniera analoga la frequenza dei cluster semantici, ovvero la combinazione dei semantic types.

<br/><br/>

## 4. Risultati

Nella seguente tabella sono presenti i risultati ottenuti:

~~~~plain
VERB: play
TOTAL SENTENCES: 308
SENTENCES ANALYZED (valency = 2): 51

____ SEMANTIC TYPES

SUBJ (46)

[('noun.person', 17), ('noun.attribute', 6), ('noun.cognition', 4), ('noun.relation', 4), ('noun.state', 4), ('noun.artifact', 2), ('verb.change', 1), ('verb.possession', 1), ('noun.phenomenon', 1), ('noun.group', 1), ('verb.stative', 1), ('noun.substance', 1), ('noun.act', 1), ('noun.event', 1), ('noun.animal', 1)]

OBJ: (51)

[('noun.act', 27), ('noun.person', 7), ('noun.artifact', 5), ('noun.cognition', 4), ('noun.attribute', 2), ('noun.location', 2), ('noun.animal', 1), ('noun.time', 1), ('noun.relation', 1), ('verb.motion', 1)]

____ SEMANTIC CLUSTER (48)

[(('noun.person', 'noun.act'), 8), (('noun.attribute', 'noun.act'), 4), (('noun.relation', 'noun.act'), 4), (('noun.person', 'noun.person'), 4), (('noun.state', 'noun.act'), 4), (('noun.person', 'noun.attribute'), 2), (('noun.cognition', 'noun.act'), 2), (('noun.person', 'noun.location'), 2), (('noun.artifact', 'noun.artifact'), 2), (('noun.person', 'noun.time'), 1), (('noun.cognition', 'noun.relation'), 1), (('noun.attribute', 'verb.motion'), 1), (('noun.attribute', 'noun.person'), 1), (('verb.change', 'noun.act'), 1), (('verb.possession', 'noun.cognition'), 1), (('noun.person', 'noun.cognition'), 1), (('noun.phenomenon', 'noun.cognition'), 1), (('noun.group', 'noun.act'), 1), (('verb.stative', 'noun.artifact'), 1), (('noun.cognition', 'noun.cognition'), 1), (('noun.substance', 'noun.act'), 1), (('noun.act', 'noun.act'), 1), (('noun.event', 'noun.act'), 1), (('noun.animal', 'noun.act'), 1), (('noun.person', 'noun.artifact'), 1)]
~~~~

~~~~plain
VERB: watch
TOTAL SENTENCES: 197
SENTENCES ANALYZED (valency = 2): 16

____ SEMANTIC TYPES

SUBJ (14)

frequency of subjs: [('noun.person', 9), ('noun.group', 1), ('noun.animal', 1), ('noun.quantity', 1), ('noun.plant', 1), ('noun.event', 1)]

OBJ: (16)

frequency of obj: [('noun.person', 3), ('noun.location', 2), ('noun.act', 2), ('noun.artifact', 2), ('noun.feeling', 1), ('noun.process', 1), ('verb.social', 1), ('noun.cognition', 1), ('verb.contact', 1), ('noun.food', 1), ('noun.state', 1)]

____ SEMANTIC CLUSTER (14)

[(('noun.person', 'noun.artifact'), 2), (('noun.person', 'noun.person'), 2), (('noun.group', 'noun.location'), 1), (('noun.person', 'noun.feeling'), 1), (('noun.person', 'noun.process'), 1), (('noun.person', 'noun.act'), 1), (('noun.person', 'noun.location'), 1), (('noun.person', 'verb.social'), 1), (('noun.animal', 'noun.act'), 1), (('noun.plant', 'verb.contact'), 1), (('noun.event', 'noun.food'), 1), (('noun.event', 'noun.state'), 1)]
~~~~

~~~~plain
VERB: get
TOTAL SENTENCES: 1407
SENTENCES ANALYZED (valency = 2): 77

____ SEMANTIC TYPES

SUBJ (62) frequency

[('noun.person', 31), ('noun.group', 5), ('noun.artifact', 5), ('noun.communication', 4), ('noun.animal', 3), ('noun.act', 3), ('noun.location', 3), ('noun.quantity', 2), ('noun.state', 2), ('verb.change', 1), ('noun.process', 1), ('verb.stative', 1), ('verb.emotion', 1)]

OBJ: (81) frequency

[('noun.act', 11), ('noun.artifact', 10), ('noun.communication', 8), ('noun.cognition', 7), ('noun.possession', 5), ('noun.attribute', 5), ('noun.person', 4), ('verb.social', 3), ('noun.time', 3), ('noun.group', 3), ('verb.motion', 3), ('verb.contact', 3), ('noun.location', 2), ('noun.animal', 2), ('noun.body', 2), ('noun.event', 1), ('noun.feeling', 1), ('verb.creation', 1), ('verb.change', 1), ('noun.food', 1), ('noun.Tops', 1), ('noun.state', 1), ('noun.quantity', 1), ('verb.possession', 1), ('verb.body', 1)]

____ SEMANTIC CLUSTER (66)

[(('noun.person', 'noun.cognition'), 5), (('noun.person', 'noun.communication'), 4), (('noun.animal', 'noun.act'), 3), (('noun.person', 'noun.act'), 3), (('noun.person', 'noun.possession'), 3), (('noun.person', 'noun.attribute'), 3), (('noun.person', 'noun.location'), 2), (('noun.animal', 'verb.social'), 2), (('noun.artifact', 'noun.communication'), 2), (('noun.person', 'noun.artifact'), 2), (('noun.person', 'noun.body'), 2), (('noun.state', 'noun.artifact'), 2), (('noun.act', 'noun.artifact'), 2), (('noun.person', 'verb.social'), 1), (('noun.group', 'noun.feeling'), 1), (('noun.act', 'noun.group'), 1), (('verb.change', 'noun.possession'), 1), (('noun.person', 'verb.creation'), 1), (('noun.artifact', 'noun.act'), 1), (('noun.person', 'noun.person'), 1), (('noun.process', 'noun.Tops'), 1), (('noun.communication', 'noun.time'), 1), (('noun.group', 'noun.time'), 1), (('noun.location', 'noun.cognition'), 1), (('noun.quantity', 'noun.attribute'), 1), (('noun.location', 'noun.possession'), 1), (('noun.quantity', 'noun.cognition'), 1), (('noun.person', 'noun.state'), 1), (('noun.person', 'noun.animal'), 1), (('noun.person', 'noun.group'), 1), (('noun.communication', 'noun.attribute'), 1), (('noun.location', 'noun.artifact'), 1), (('noun.group', 'noun.act'), 1), (('verb.stative', 'noun.act'), 1), (('noun.group', 'verb.contact'), 1), (('noun.group', 'noun.animal'), 1), (('noun.person', 'verb.possession'), 1), (('noun.artifact', 'verb.motion'), 1), (('noun.person', 'verb.contact'), 1), (('noun.artifact', 'noun.group'), 1), (('noun.communication', 'noun.act'), 1), (('verb.emotion', 'noun.person'), 1), (('noun.person', 'verb.motion'), 1), (('noun.communication', 'verb.body'), 1)]
~~~~

Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
greed | `Synset('greed.n.01')` | 7 | &nbsp; | politics | `Synset('section.n.03')` | 6
greed | `Synset('actor.n.02')` | 7 | &nbsp; | politics | `Synset('governed.n.01')` | 6

<br/><br/>

# 5 Sitografia

[1] <https://spacy.io/usage/linguistic-features> <br/>
[2] <https://spacy.io/api/annotation> <br/>
[3] <https://wordnet.princeton.edu/documentation/lexnames5wn>
