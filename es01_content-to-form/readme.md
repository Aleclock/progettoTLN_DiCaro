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

In base ai risultati, solo in un caso c'è perfetta corrispondenza (greed , `Synset('greed.n.01')`), mentre in 4 casi viene individuato il contesto corretto (`'right.n.01'`, `'governed.n.01'`, `'carbohydrate.n.01'`, `'band.n.11'`). Nel caso dei termini “patience”, “radiator” e “vehicle” il synset trovato non è corretto.

Nelle seguenti tabelle è presente l’elenco ordinato dei 10 migliori synset per ogni termine. Come si può notare, molto spesso ci sono diversi synset con lo stesso valore massimo. Inoltre la variazione del punteggio è molto basso tra i primi dieci synset. Nel caso di termini come “radiator” e “vehicle”, il synset associato è rispettivamente `Synset('hot.a.01')` e `Synset('container.n.01')`( con punteggio 7 e 8), ma tra i primi dieci risultati ci sono anche synset più adatti come `Synset('heating_system.n.01')` (punteggio 5) e `Synset('wheeled_vehicle.n.01')` (punteggio 7).
Mentre nella maggior parte delle definizioni è stato analizzato il synset perfettamente corrispondente al termine, nel caso dei termini “patience” e “screw” i synset associati direttamente a questi termini non sono stati analizzati.




Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
justice | `Synset('right.n.01')` | 6 | &nbsp; | patience | `Synset('day.n.07')` | 5
justice | `Synset('human_right.n.01')` | 4 | &nbsp; | patience | `Synset('digest.v.03')` | 5
justice | `Synset('jurisprudence.n.01')` | 4 | &nbsp; | patience | `Synset('long_run.n.01')` | 4
justice | `Synset('rule.n.01')` | 4 | &nbsp; | patience | `Synset('stretch.n.06')` | 4
justice | `Synset('law.n.02')` | 4 | &nbsp; | patience | `Synset('lunar_day.n.01')` | 4
justice | `Synset('entitlement.n.01')` | 4 | &nbsp; | patience | `Synset('able.s.03')` | 4
justice | `Synset('principle.n.04')` | 4 | &nbsp; | patience | `Synset('blue_moon.n.01')` | 4
justice | `Synset('use.n.07')` | 4 | &nbsp; | patience | `Synset('spontaneity.n.01')` | 4
justice | `Synset('military_law.n.01')` | 4 | &nbsp; | patience | `Synset('compassion.n.02')` | 4
justice | `Synset('justice.n.01')` | 3 | &nbsp; | patience | `Synset('mental_quickness.n.01')` | 4

<br/>

Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
greed | `Synset('greed.n.01')` | 7 | &nbsp; | politics | `Synset('governed.n.01')` | 6
greed | `Synset'acquisitiveness.n.01')` | 5 | &nbsp; | politics | `Synset('section.n.03')` | 6
greed | `Synset('air.n.03')` | 5 | &nbsp; | politics | `Synset('regulate.v.02')` | 5
greed | `Synset('tone.n.10')` | 5 | &nbsp; | politics | `Synset('relationship.n.03')` | 5
greed | `Synset('recommendation.n.03')` | 5 | &nbsp; | politics | `Synset('politics.n.05')` | 5
greed | `Synset('covet.v.01')` | 5 | &nbsp; | politics | `Synset('government.n.01')` | 5
greed | `Synset('color.n.08')` | 5 | &nbsp; | politics | `Synset('authoritarian_state.n.01')` | 5
greed | `Synset('hunger.n.02')` | 4 | &nbsp; | politics | `Synset('population.n.04')` | 5
greed | `Synset('magnificence.n.02')` | 4 | &nbsp; | politics | `Synset('state.n.04')` | 5
greed | `Synset('possessiveness.n.01')` | 4 | &nbsp; | politics | `Synset('utopia.n.02')` | 5

<br/>

Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
food | `Synset('carbohydrate.n.01')` | 5 | &nbsp; | radiator | `Synset('hot.a.01')` | 7
food | `Synset('biology.n.02')` | 5 | &nbsp; | radiator | `Synset('central_heating.n.01')` | 6
food | `Synset('animation.n.01')` | 5 | &nbsp; | radiator | `Synset('utility.n.06')` | 6
food | `Synset('reservoir.n.04')` | 5 | &nbsp; | radiator | `Synset('furnace_room.n.01')` | 6
food | `Synset('parasite.n.01')` | 5 | &nbsp; | radiator | `Synset('heating_system.n.01')` | 5
food | `Synset('life.n.11')` | 5 | &nbsp; | radiator | `Synset('section.n.04')` | 5
food | `Synset('parent.n.02')` | 5 | &nbsp; | radiator | `Synset('mineral_water.n.01')` | 5
food | `Synset('embryo.n.02')` | 5 | &nbsp; | radiator | `Synset('position.n.07')` | 4
food | `Synset('process.n.05')` | 5 | &nbsp; | radiator | `Synset('dining-hall.n.01')` | 4
food | `Synset('life.n.03')` | 4 | &nbsp; | radiator | `Synset('component.n.03')` | 4

<br/>

Term | Synset | Value | &nbsp; | Term | Synset | Value
------------ | ------------ | ------------- | ------------- | ------------ | ------------ | -------------
vehicle | `Synset('container.n.01')` | 8 | &nbsp; | screw | `Synset('band.n.11')` | 7
vehicle | `Synset('wheeled_vehicle.n.01')` | 8 | &nbsp; | screw | `Synset('slice.n.05')` | 6
vehicle | `Synset('way.n.06')` | 7 | &nbsp; | screw | `Synset('solder.n.01')` | 6
vehicle | `Synset('component.n.03')` | 6 | &nbsp; | screw | `Synset('counter.n.08')` | 6
vehicle | `Synset('translocate.v.02')` | 6 | &nbsp; | screw | `Synset('beam.n.02')` | 6
vehicle | `Synset('motion.n.06')` | 6 | &nbsp; | screw | `Synset('section.n.04')` | 6
vehicle | `Synset('airlift.n.01')` | 6 | &nbsp; | screw | `Synset('connect.v.01')` | 6
vehicle | `Synset('handcart.n.01')` | 6 | &nbsp; | screw | `Synset('bimetal.n.01')` | 5
vehicle | `Synset('section.n.04')` | 6 | &nbsp; | screw | `Synset('join.v.02')` | 5
vehicle | `Synset('teleportation.n.01')` | 5 | &nbsp; | screw | `Synset('ridge.n.06')` | 5

<br/><br/>

Nella seguente tabella sono riportati i valori di similarità corrispondenti ai synset che avrebbero dovuto ottenere il punteggio maggiore.

Term | Synset | Value
------------ | ------------ | -------------
justice | `Synset('justice.n.01')` | 3
patience | Not evaluated | &nbsp;
greed | `Synset('greed.n.01'` | 7
politics | `Synset('politics.n.02')` <br/> `Synset('politics.n.05')` | 4 <br/> 5
food | `Synset('food.n.01')` | 4
radiator | `Synset('radiator.n.01')` | 2
vehicle | `Synset('vehicle.n.01')` | 4
screw | Not evaluated | &nbsp;