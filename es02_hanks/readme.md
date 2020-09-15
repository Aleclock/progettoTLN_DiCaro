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

## 2 Parsing e disambiguazione

Dopo aver ottenuto le frasi contenenti il verbo scelto, è necessario fare il parsing e la disambiguazione.

Per ogni frase si ottiene il suo part-of-speech grazie alla funzione `nltk.pos_tag(sentence, tagset='universal')`. Successivamente si utilizza `spaCy`[1] per determinare il verbo, il soggetto e l'oggetto della frase.

Dato l'albero contenente il part-of-speech della frase (`tree`), i tre elementi si determinano come segue:

* `verbAddress` è il termine nell'albero il quale corrisponde ai verbi scelti;
* `subjects` è una lista contenente tutti i termini della frase il cui reggente (`head`) è `verbAddress`, la cui relazione sintattica (`dep_`) è `nsubj` e il cui part-of-speech (`tag_`) è `NN`;
* `objects` è una lista contenente tutti i termini della frase il cui reggente (`head`) è `verbAddress`, la cui relazione sintattica (`dep_`) è `obj` e il cui part-of-speech (`tag_`) è `NN`;

~~~~python
def extractVerbSubjObj (verb, tree):
    # for each token (t) in tree, if t.text is equal to verb get its index (next() get first element)
    verbAddress = next(t.text for t in tree if t.text in verb) 
    subjects = list(t.text for t in tree if str(t.head) == verbAddress and "nsubj" in t.dep_ and "NN" in t.tag_)
    objects = list(t.text for t in tree if str(t.head) == verbAddress and "obj" in t.dep_ and "NN" in t.tag_)
    return subjects, objects, obls
~~~~

In questo modo è possibile determinare il verbo, i soggetti nominali e gli oggetti della frase [2].

<br/><br/>

## 1.3 Determinazione miglior senso (concetto)

Per determinare il synset migliore rispetto alle definizioni si utilizza un approccio bag-of-words. La similarità è calcolata come:

~~~~plain
cardinalità dell'insieme intersezione tra i due contesti + 1
~~~~

dove i due contesti sono formati da:

* termini risultanti dal pre-processamento delle definizione del termine;
* termini risultati dal pre-processamento della definizione e degli esempi contenuti nel synset (`s.definition()` e `s.examples()`)

Il synset che ottiene l'overlap maggiore risulta essere quello che più corrisponde alle definizioni.

<br/><br/>

## 2 Risultati

Di seguito i risultati ottenuti

Correct term | Calculated term | Definition
------------ | ------------ | -------------
justice | `Synset('right.n.01')` | an abstract idea of that which is due to a person or governmental body by law or tradition or nature; ; - Eleanor Roosevelt
patience | `Synset('digest.v.03')` | put up with something or somebody unpleasant
greed | `Synset('greed.n.01')` | excessive desire to acquire or possess more (especially more material wealth) than one needs or deserves
politics | `Synset('governed.n.01')` | the body of people who are citizens of a particular government; --Declaration of Independence
food | `Synset('carbohydrate.n.01')` | an essential structural component of living cells and source of energy for animals; includes simple sugars with small molecules as well as macromolecular substances; are classified according to the number of monosaccharide groups they contain
radiator | `Synset('hot.a.01')` | used of physical heat; having a high or higher than desirable temperature or giving off heat or feeling or causing a sensation of heat or burning
vehicle | `Synset('container.n.01')` | any object that can be used to hold things (especially a large metal boxlike object of standardized dimensions that can be loaded from one form of transport to another)
screw | `Synset('band.n.11')` | a thin flat strip or loop of flexible material that goes around or over something else, typically to hold it together or as a decoration


<br/><br/>

# 3 Interpretazione dei risultati

In base ai risultati, solo in un caso c'è perfetta corrispondenza (greed , `Synset('greed.n.01')`), mentre negli altri casi il synset si avvicina al contesto del termine oppure il synset è completamente sbagliato.

Nelle seguenti tabelle sono riportati i migliori 10 synset per un dato concetto. Come si può notare, in alcuni casi ci sono dei valori a pari merito. In altri casi il senso che sarebbe ottimale per il concetto risulta essere nelle prime 10 posizioni ma per poco non risulta essere il migliore

Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
justice | `Synset('right.n.01')` | 6 | &nbsp; | patience | `Synset('day.n.07')` | 5
justice | `Synset('use.n.07')` | 4 | &nbsp; | patience | `Synset('digest.v.03')` | 5
justice | `Synset('respect.n.01')` | 4 | &nbsp; | patience | `Synset('resourcefulness.n.01')` | 4
justice | `Synset('force.n.04')` | 4 | &nbsp; | patience | `Synset('clock.v.01')` | 4
justice | `Synset('jurisprudence.n.01')` | 4 | &nbsp; | patience | `Synset('convertibility.n.01')` | 4
justice | `Synset('legal_right.n.01')` | 4 | &nbsp; | patience | `Synset('accept.v.07')` | 4
justice | `Synset('entitlement.n.01')` | 4 | &nbsp; | patience | `Synset('end.n.02')` | 4
justice | `Synset('interest.n.05')` | 4 | &nbsp; | patience | `Synset('duration.n.01')` | 4
justice | `Synset('restraint.n.04')` | 4 | &nbsp; | patience | `Synset('stretch.n.06')` | 4
justice | `Synset('law.n.01')` | 4 | &nbsp; | patience | `Synset('time_frame.n.01')` | 4

<br/>

Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
greed | `Synset('greed.n.01')` | 7 | &nbsp; | politics | `Synset('section.n.03')` | 6
greed | `Synset('actor.n.02')` | 7 | &nbsp; | politics | `Synset('governed.n.01')` | 6
greed | `Synset('longer.n.01')` | 6 | &nbsp; | politics | `Synset('wing.n.08')` | 5
greed | `Synset('covet.v.01')` | 5 | &nbsp; | politics | `Synset('politics.n.05')` | 5
greed | `Synset('acquisitiveness.n.01')` | 5 | &nbsp; | politics | `Synset('area.n.01')` | 5
greed | `Synset('wanter.n.01')` | 5 | &nbsp; | politics | `Synset('state.n.04')` | 5
greed | `Synset('maniac.n.02')` | 5 | &nbsp; | politics | `Synset('code.n.01')` | 5
greed | `Synset('kin.n.01')` | 4 | &nbsp; | politics | `Synset('population.n.04')` | 5
greed | `Synset('itch.v.04')` | 4 | &nbsp; | politics | `Synset('relationship.n.03')` | 5
greed | `Synset('user.n.01')` | 4 | &nbsp; | politics | `Synset('government.n.03')` | 5

<br/><br/>

# 5 Sitografia

[1] <https://spacy.io/usage/linguistic-features> <br/>
[2] <https://spacy.io/api/annotation>
