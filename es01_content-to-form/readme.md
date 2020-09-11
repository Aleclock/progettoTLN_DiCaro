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

# 1.1 Preprocessing

Per ogni termine definito (chiave del dizionario), viene applicato il pre-processing attraverso la funzione `preProcess()`, la quale applica le seguenti procedure:

* tokenizzazione;
* rimozione stopword;
* rimozione punteggiatura;
* lemmatizzazione;
* stemming.

Per ogni definizione, viene applicato il preprocessing e la funzione ritorna una lista di liste contentenenti i termini presenti nelle varie definizioni.

<br/><br/>

# 1.2 Calcolo similarità tra definizioni

La similarità tra le definizioni di uno stesso termine (contenute nella lista `dProcessed`) viene calcolata con la funzione `getSimilarity()`, la quale calcola la similarità tra tutte le possibili definizioni dello stesso termine. Il valore di similarità tra due definizioni `d1,d2` viene calcolato come

~~~~python
sim = d1.intersection(d2) / (min(len(d1),len(d2)))
~~~~

ovvero come la cardinalità dell'insieme intersezione tra gli insiemi normalizzata sulla cardinalità minima dei due insiemi.

Il valore di similarità totale viene calcolato come la media tra le similarità tra le coppie di definizioni. Nel calcolo della similarità non si tiene conto della similarità tra due definizioni uguali

<br/><br/>

# 2 Aggregazione sulle due dimensioni

Dopo aver calcolato la similarità generale per tutti e quattro i termini, il risultato è il seguente

&nbsp;| Abstract | Concrete
------------: | :------------: | :-------------:
**Generic** | 0.09 | 0.26
**Specific** | 0.14 | 0.16

<br/><br/>

# 3 Interpretazione dei risultati

Si può notare, come è normale che sia, che le definizioni riguardanti i termini astratti risultino meno simili tra loro rispetto a quelli concreti. Importante notare che, mentre le definizioni del concetto generico concreto risultano più simili rispetto a quelle del termine specifco concreto (10% più simili), nel caso dei termini astratti avviene il contrario.
