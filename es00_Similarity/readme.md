# **Definition similarity**

<br/><br/>

>Questa esercitazione prevede i seguenti passaggi:
>
>1. Caricamento dei dati sulle definizioni (file definizioni.xls o documento Google presente su Moodle);
>2. Preprocessing (su frequenza minima dei termini, stemming, etc. a vostra scelta);
>3. Calcolo similarità tra definizioni (cardinalità dell’intersezione dei termini normalizzata su lunghezza minima tra le due, o varianti a scelta);
>4. Aggregazione sulle due dimensioni (concretezza / specificità come da schema in basso);
>5. Interpretazione dei risultati e scrittura di un piccolo report (da inserire nel vostro portfolio per l’esame).

<br/>

# 0. Caricamento dei dati sulle definizioni 

Le definizioni presenti nel file sono state fornite da diverse persone e riguardano i seguenti termini:

* building (concreto generico);
* molecule (concreto specifico);
* freedom (astratto generico);
* compassion (astratto specifico).

Il file *definizioni.csv* in input viene convertito, grazie alla funzione `load_csv()`, in un dizionario composto dalle seguenti chiavi:

* `conc_generic`: definizioni generiche riguardanti l'elemento concreto;
* `conc_specific`: definzioni specifiche riguardanti l'elemento concreto;
* `abst_generic`: definizioni generiche riguardanti l'elemento astratto;
* `abst_specific`: definizioni specifiche riguardanti l'elemento astratto.

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

La similarità tra le definizioni di uno stesso termine (contenute nella lista `dProcessed`) viene calcolata con la funzione `getSimilarity()`, la quale calcola la similarità tra tutte le possibili definizioni dello stesso termine. Il valore di similarità viene calcolato come 

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
