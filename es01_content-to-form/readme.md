# **Content to form**

<br/><br/>

>L’esercitazione prevede i seguenti passaggi:
>
>1. Caricamento dei dati content-to-form (presente su Moodle);
>2. Preprocessing (si veda esercitazione precedente, a vostra scelta);
>3. Utilizzo di WordNet come sense inventory, per inferire il concetto descritto dalle diverse definizioni;
>4. Definire ed implementare un algoritmo (efficace ma anche efficiente) di esplorazione dei sensi di WordNet, usando concetti di similarità (tra gloss e definizioni, esempi d’uso, rappresentazioni vettoriali, etc.);
>
>* Suggerimento A: sfruttare principi del genus-differentia;
>* Suggerimento B: sfruttare tassonomia WordNet nell’esplorazione;
>* Suggerimento C: pensare a meccanismi di backtracking.


<br/>

# 0. Caricamento dei dati sulle definizioni 

Il file *definizioni.csv* contiene 12 definizioni per ogni termine, per un totale di 8 termini. Il file in input viene convertito, grazie alla funzione `load_csv()`, in una lista di liste contenenti le varie definizioni per un termine.

<br/><br/>

# 1. Determinazione concetto definito

## 1.1 Preprocessing e 

Per ogni lista di definizioni del concetto viene calcolata una lista contenente i termini più comuni presenti nelle varie definizioni. Le definizioni sono soggette a pre-processing grazie alla funzione `preProcess()` (tokenizzazione, rimozione stopword e punteggiatura, lemmatizzazione).

La funzione `getCommonTerms()` permette di ottenere, a partire da una lista ottenuta unendo le varie definizioni/liste, una lista ordinata in base alla frequenza degli elementi. Questo viene fatto nel seguente modo

~~~~python
most_common_words= [(word,word_count) for word, word_count in Counter(d).most_common()]
~~~~

<br/><br/>

## 1.2 Determinazione dei Synset in base ai lemmi

Dopo aver determinato in termini più comuni presenti nelle definizioni del concetto, con la funzione `getSynsetsFromLemma()` si calcolano i WordNet Synset associati ai termini più comuni. Questo viene fatto perchè si ipotizza che i termini più frequenti sono quelli più rilevanti nella definizione del concetto.

La funzione determina i Synset a partire dai 10 termini più rilevanti e, per ogni termine, determina i synsets associati con la funzione WordNet `wn.synsets(lemma)`. Per ogni senso ottenuto viene fatta una ricerca in profondità in modo tale da aggiungere alla lista di sensi gli iponimi e gli iperonimi (`synset.hyponyms()` e `synset.hypernyms()`). La ricerca degli iponimi e degli iperonimi viene fatta anche sui nuovi sensi trovati. Il processo ricorsivo viene fermato in base a due variabili:

* `hyponyms_limit`: imposta un limite nella ricerca in profondità degli iponimi;
* `hypernyms_limit`: imposta un limite nella ricerca in profondità degli iperonimi.

L'algoritmo sviluppato imposta a 3 la profondità nella ricerca sia degli iponimi sia degli iperonimi.

La funzione `getSynsetsFromLemma()` ritorna una lista contenente synset ottenuti a partire dai termini più frequenti presenti nelle definizioni del concetto.

**ATTENZIONE**: Ho notato che la lista di synset che ottengo nella ricerca in base al lemma cambia di volta in volta, motivo per cui i risultati spesso cambiano. 

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