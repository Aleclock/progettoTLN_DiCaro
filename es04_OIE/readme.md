# **Text segmentation**

<br/><br/>

>L’esercitazione prevede l’implementazione di un sistema di OIE (lezione 5 Giugno)

<br/>

# 0. Estrazione delle frasi da un corpus

Le frasi vengono estratte dal Brown corpus attraverso la funzione `extractSencenses()`, nella quale vengono estratte un numero preciso di frasi attraverso la funzione NLTK `brown.sents()`. Siccome le istanze ritornate dalla funzione sono liste di parole, queste vengono unite in un'unica stringa.

<br/><br/>

# 1. Parsing ed estrazione del verbo

Per ogni frase viene estratto l'albero a dipendenze tramite la funzione `dependencyParsing()`. L'albero a dipendenze viene calcolato tramite spaCy

~~~~python
def dependencyParsing (sentence):
    nlp = spacy.load('en_core_web_sm')
    return nlp(sentence)
~~~~

Dopo aver calcolato l'albero a dipendenze, il verbo principale viene determinato con la funzione `extractMainVerb()`, la quale scorre tutti i token dell'albero e seleziona solo quello con il valore "ROOT" come relazione di dipendenza sintattica (`token.dep_`) e con il valore "VB" relativo al part-of-speech (`t.tag_`).

<br/><br/>

# 2. Calcolo del soggetto e dell'oggetto del verbo principale

Nel caso in cui esista il verbo principale, vengono estratti il soggetto e l'oggetto del verbo principale attraverso la funzione `extractVerbSubjObj`. La funzione scorre tutti i token dell'albero a dipendenze e

* il soggetto è la lista di token il cui reggente (`head`) è il verbo principale (`verb`) e la cui relazione sintattica (`dep_`) è `nsubj`;
* il soggetto è la lista di token il cui reggente (`head`) è il verbo principale (`verb`) e la cui relazione sintattica (`dep_`) è `obj`. [1][2]

Nel caso in cui non sia presente l'oggetto, ovvero se non è presente un token con la relazioen sintattica `dep_`, allora viene preso il token con la relazione `ccomp`.

~~~~python
def extractVerbSubjObj (tree, verb):
    subjs = list(t for t in tree if str(t.head) == verb.text and "nsubj" in t.dep_)
    objs = list(t for t in tree if str(t.head) == verb.text and "obj" in t.dep_)

    if not objs:
        objs = list(t for t in tree if str(t.head) == verb.text and "ccomp" in t.dep_)

    return subjs, objs
~~~~

<br/><br/>

# 3. Calcolo delle dipendenze degli argomenti

Nel caso in cui siano presenti sia il soggetto che l'oggetto del verbo, è possibile determinare la tripletta composta da:

~~~~python
[arg1, verbal_phrase, arg2]
~~~~

I dipendenti del verbo si calcolano con la funzione `geVerbDependency()`, la quale estrae dall'albero tutti i token che hanno come reggente il verbo e come relazione sintattica `aux` (ausiliario). La lista di token viene successivamente ordinata in base all'indice nell'albero a dipendenze.

<br/>

I dipendenti del soggetto e dell'oggetto si calcolano con la funzione `getDependency()`, la quale estrae dall'albero a dipendenze tutti i token che hanno come reggente l'argomento (soggetto o oggetto). Questa funzione permette di estrarre in maniera ricorsiva i dipendenti dei dipendenti. Anche in questo caso i token vengono ordinati in base all'indice nell'albero.

~~~~python
def getDependency(tree, argument, limit):
    full_arg = set ()
    if limit > 0:
        for arg in [t for t in tree if str(t.head) == argument.text]:
            full_arg |= set(getDependency(tree, arg, limit - 1))
    return full_arg | set([t for t in tree if str(t.head) == argument.text] + [argument])

def geVerbDependency(tree, verb):
    return sorted([verb] + [t for t in tree if str(t.head) == verb.text and "aux" in t.dep_], key = lambda v: v.i)
~~~~

Infine le liste di token relativi ai vari argomenti vengono convertiti in stringhe (funzione `joinArg()`) e uniti in una lista.

<br/><br/>

# 4. Risultati

I test sono stati fatti su 30 frasi, ottenendo i seguenti risultati

Sentence | Triple
------------ | ------------
The Fulton County Grand Jury said Friday an investigation of Atlanta's recent primary election produced `` no evidence '' that any irregularities took place . | [The Fulton County Grand Jury] <br/> [said] <br/> [an investigation of election]
The jury further said in term-end presentments that the City Executive Committee , which had over-all charge of the election , `` deserves the praise and thanks of the City of Atlanta '' for the manner in which the election was conducted . | [The jury] <br/> [said] <br/> [that the City Executive Committee , had , ` ` deserves the praise and thanks of '' for manner]
`` Only a relative handful of such reports was received '' , the jury said , `` considering the widespread interest in the election , the number of voters and the size of this city '' . | [the jury] <br/> [said] <br/> [` ` Only a relative handful of was received '']
The jury said it did find that many of Georgia's registration and election laws `` are outmoded or inadequate and often ambiguous '' . | [The jury] <br/> [said] <br/> [it did find that many ` ` are outmoded or inadequate]
It recommended that Fulton legislators act `` to have these laws studied and revised to the end of modernizing and improving them '' . | [It] <br/> [recommended] <br/> [that Fulton legislators act ` ` to have studied '']
The grand jury commented on a number of other topics , among them the Atlanta and Fulton County purchasing departments which it said `` are well operated and follow generally accepted practices which inure to the best interest of both governments '' . | [The grand jury] <br/> [commented] <br/> [among them the Atlanta and County purchasing departments which it said are]
However , the jury said it believes `` these two offices should be combined to achieve greater efficiency and reduce the cost of administration '' . | [the jury] <br/> [said] <br/> [it believes ` ` offices should be combined achieve]
It urged that the city `` take steps to remedy '' this problem . | [It] <br/> [urged] <br/> [that the city ` ` take steps to remedy '' problem]
It urged that the next Legislature `` provide enabling funds and re-set the effective date so that an orderly implementation of the law may be effected '' . | [It] <br/> [urged] <br/> [that the next Legislature ` ` provide enabling funds and - set the effective date so that implementation may be effected]
The grand jury took a swipe at the State Welfare Department's handling of federal funds granted for child welfare services in foster homes . | [The grand jury] <br/> [took] <br/> [a swipe]
The jurors said they realize `` a proportionate distribution of these funds might disable this program in our less populous counties '' . | [The jurors] <br/> [said] <br/> [they realize ` distribution might disable program in '']
Nevertheless , `` we feel that in the future Fulton County should receive some portion of these available funds '' , the jurors said . | [the jurors] <br/> [said] <br/> [Nevertheless , ` ` we feel that in County should receive portion '']
The jury also commented on the Fulton ordinary's court which has been under fire for its practices in the appointment of appraisers , guardians and administrators and the awarding of fees and compensation . | [The jury] <br/> [commented] <br/> [which has been under fire for practices]
The jury said it found the court `` has incorporated into its operating procedures the recommendations '' of two previous grand juries , the Atlanta Bar Association and an interim citizens committee . | [The jury] <br/> [said] <br/> [it found court ` ` has incorporated into recommendations]
`` These actions should serve to protect in fact and in effect the court's wards from undue costs and its appointed and elected servants from unmeritorious criticisms '' , the jury said . | [the jury] <br/> [said] <br/> [` ` These actions should serve to protect in fact and in effect wards '']
Regarding Atlanta's new multi-million-dollar airport , the jury recommended `` that when the new management takes charge Jan. 1 the airport be operated in a manner that will eliminate political influences '' . | [the jury] <br/> [recommended] <br/> [Atlanta new dollar ` that when management takes charge Jan. the airport be operated in manner '']
The jury praised the administration and operation of the Atlanta Police Department , the Fulton Tax Commissioner's Office , the Bellwood and Alpharetta prison farms , Grady Hospital and the Fulton Health Department . | [The jury] <br/> [praised] <br/> [the Fulton Tax Commissioner 's Office , the Bellwood prison farms , Hospital]

<br/><br/>

# 5. Sitografia

[1] <https://spacy.io/api/token#attributes> <br/>
[2] <https://spacy.io/api/annotation> <br/>



