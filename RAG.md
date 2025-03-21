comparación de embedders: https://huggingface.co/spaces/mteb/leaderboard
Para mitigar alucinaciones se puede: 
- in trainig-time: ajustarlo para que baje la probabilidad de halucinacińo
- in generation-time: se puede o analizar la probabilidad de generación o validar con otros LLMs
- con external tools: RAG
### Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity

Existen varias técnicas para resolver tareas con RAG, algunas directas otras avanzadas con varios loops, dicen que aplicarlo a una tarea sencilla es pérdida de tiempo -> un modelo clasificador que dice si la tarea es sencilla y entonces elegir el tipo de RAG (adaptative RAG)

todo leer: 
- Open-domain QA
- Multi-hop QA
- Adaptive Retrieval??

sin RAG los LLM halucinan, con simple RAG ayuda pero los querys más complejas no pueden. Luego multi-step RAG lleva un proceso iterativo para ir sacando cada vez más y más documentos y en cada iteración un LLM define la siguiente query.

# Retrieving and Reading : A Comprehensive Survey on Open-domain Question Answering
(bastante antiguo)

pregunta-respuesta directa -> cuando buscas en google y te sale directo.
Puedes ser RAG desde Textual QA (sin estructura, Wikipedia, science books...) o desde structured.

##### Traditional QA (más o menos obsoleto por Retrieving and reading): 
- question analysis: reformulate question para generar search queries (Antes de LLMs hacían muchas movidas) + question classification para obtener expected answer types (aquí también se hacían muchas opciones)
- Document retrieval -> Answer Extraction. Se pueden usar IR (infromation retrieval techniques): Boolean model, vector space model (embeddings), Probabilistic model, Language model (genera probs)
	Mencionan un post-procesado desupés de muchos documentos retrieveados
- Answer extraction: sacar final answer de los docs
![[Pasted image 20250224115508.png]]

tradicionalmente CNN, LSTM, MRC (machine reading comprehension -> transformers entran aquí)
Mencionan que se usa RAG en web también -> océano de información pero puede haber mucha información ruidosa.

Bidaf generaba varios embeddings para documento, con diferentes niveles de granularidad. ESto ya lo implementan con el concepto de atención los LLMs modernos, pero quizás se pueda integrar esta idea con diferentes LLMs. Diferentes LLMs están entrenados para capturar diferentes conceptos semánticos.

##### Entrenar el sistema de RAG:
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- REALM parece que tiene muy buena pinta.

##### Modern QA, Retrieving and Reading

![[Pasted image 20250224124940.png]]

Tipos de retrievers: 
- Sparse retrievers: usan bigramas y así, no interesantes
- Dense retriever: RAG con embeddings generados por transformers: 
	- Representation-based Retrievers: dos codificadores para pregunta y para respuestas, luego similitud semántica con función como coseno -> el de openai y el de huggingface 
	- Interaction-based Retriever: Se entrena un modelo como BERT para definir la relevancia de una query para dado un documento -> meten como input el query y el documento y usan el CLS de BERT para determinar si es relevante o no. Luego en inferencia se pasa toda la base de datos por el modelo para la query. Entonces el modelo captura para cada token la relación con atención para cada token de cada documento. Es más preciso que el dense normal pero tiene pinta de computacionalmente prohibitivo con una base de datos de tamaño suficiente.
	- Representation-interaction Retriever: combina las dos estrategias. Vectorizas los documentos y los query en embeddings pero a nivel de token (un embedding por token). Entonces luego al hacer el RAG va mirando una media de la similitud entre token y token con los querys y los documentos. Mencionan ColBERT-QA que utiliza ColBERT en un dataset de QA. Tiene muy buena pinta, no se hasta que punto degrada la eficiencia, #todo, también se podría mirar un enfoque híbrido de hacer rag normal sobre muchos y luego el colbert sobre pocos, mirar si ya existe -> también existe colbertV2
	

![[Pasted image 20250224154227.png]]
![[Pasted image 20250311150135.png]]
![[Pasted image 20250224154247.png]]
- Iterative retriever: lo mismo pero con varios pasos en los que se van modificando y añadiendo docs nuevos. Separa en document retriever (los mencionados antes), Query Reformulation (varias técnias, LLMs cabras -> Golden retriever, tiene pinta que los SOTA van mejor que esto), y retrieval stopping mechanism (varias técnicas, mirar SOTA más adelante)
Post procesado de documentos -> con varias estrategias elegir sólo los importantes, mirar SOTA.

Readers
Desde los documentos relevantes sacar la respuesta a la pregunta
- antes usaban Extractive Readers -> la respuesta a la pregunta tenía que estar en los documentos
- ahora el sota usa Generative readers (LLMs)

Answer Post processing
otra vez LLMs, mirar el sota mejor.

### APPROXIMATE NEAREST NEIGHBOR NEGATIVE CON-TRASTIVE LEARNING FOR DENSE TEXT RETRIEVAL

Presentan una técnica para entrenar modelos que generan embeddings. Parece que está obsoleto, puede ser interesante ajustar el modelo embedder para el dominio específico del RAG del proyecto #todo

usuario de reddit menciona querer ajustar me5
LlamaIndex tiene tutorial de como ajustar un modelo embedder para un rag mejor, genera preguntas sintéticas con LLM para entrenar el embedder: 
https://docs.llamaindex.ai/en/latest/examples/finetuning/embeddings/finetune_embedding/

otro paper de survey RAG menciona también que ajustar el embedder mejora un poco el rendimiento del RAG.

### Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering

Ajustan un modelo T5 o BART para pasarle un query con varios documentos retrieved y que este genere la respuesta deseada (el componente Reader basicamente). Supongo que el SOTA de gpt4 es mejor pero este es mucho más liviano y podría ejecutarse en local.

### Test-Time Self-Adaptive Small Language Models for Question Answerin

Entrenan un agente con datos sin etiquetar, tienen una bd con documentos y preguntas sin respuesta. Usan un agente con RAG para generar respuestas sintéticas, luego entrenan el mismo modelo con esas respuestas sintéticas -> aprende a usar el sistema.

### Internet-augmented language models through few-shot prompting for open-domain question answering

Usaron la api de google search para pasarle a un LLM varios documentos relacionados. Usaron tiempos de inferencia largos, computando simultaneamente varias respuestas paralelas para comparar respuestas.

### n-Context Retrieval-Augmented Language Models
Dicen que le añaden al LLM los docs del RAG sin fine tunearlo, a diferencia de otro RALM que lo entrenan para tener en cuenta los docs. Entiendo que se puede definir el token del Docs para pasarle docs relevantes.

### Improving Zero-shot Reader by Reducing Distractions from Irrelevant Documents in Open-Domain Question Answering

Muy interesante:
Mencionan que si los documentos del RAG son irrelevantes, distraen al modelo y se degenera su rendimiento. 
Proponen para cada documento retrieved, que el modelo junto a un prompt con generación greedy genere la solución a la pregunta. TAmbién le dan la opción de "Respuesta imposible". 
Entonces teniendo todas las respuestas, sacan la puntuación de cada respuesta como la probabilidad del modelo de generar esa respuesta dada la pregunta con el prompt y el documento, eligen esa respuesta.

### Retrieval-Augmented Generation for Large Language Models: A Survey

Mencionan varias técnicas de RAG "avanzado": 

##### Optimizar el index de datos
- Mejorar la granulariedad de los datos: se limpian los datos para mejorar la calidad y búsqueda; eliminar redundancias y carácteres especiales, actualizar obsoletos, verificar corrección...
- Optimizar sistemas de indexado: se pueden hacer sistemas por grafos (crear relaciones entre los índices de la forma que sea) + ajustar bien el tamaño del chunk (muy grande demasiado pequeño, pequeño falta contexto)
- Añadir metadata a los chunks: por ejemplo en la bd stackoverflow añadir las etiquetas a los chunks, filtrar por etiquetas antes mejor pero igual añaden info útil a los embeddings
- optimización del alignment: generar preguntas para los documentos y añadirlos a los propios documentos para que el embedding tenga info tamibén de las preguntas a las que podría responder
- Mixed retrieval: basicamente buscar con pgvector por consultas sql y luego por vectores
##### Optimizar embeddings
- Ajustar los modelos de embedding para que funcionen mejor en el dominio de la aplicación #todo, dicen que BGE está preparado para eso, generar sintéticamente con gpt querys para los documentos y entrenarlo con eso.

##### Proceso de post retrieval 
para no pasarle todos los documentos retrieved directametne al LLM
- ReRank: por como funciona el mecanismo de atención los LLM prestan más atención a los últimos y los primeros documentos -> poner los más improtantes al principio y al final. Hay varias técnicas para decidir cual es el más importante, según la similitud, según la diversidad (que no aparezcan seguidos al principio lso que sean muy parecidos)
- Compresión de documentos: usando varias técnicas comprimir los documentos para evitar ruido #todo -> varias técnicas

##### Optimización del pipeline RAG
- búsqueda híbrida como con Pgvector
- Recursive retrieval: separar el RAG en dos fases, primero recuperar documentos pequeños para obtener las ideas clave, y luego generar queries más específicas para documentos más extensos y detallados. Interesante, #todo
- Stepback prompt: decirla al LLM que puede descartar ideas (ir para atrás) -> con los LLM razonadores creo que esto no es necesario, pero se podría añadir algo en el prompt para fomentar que lo haga
- subqueries: que una consulta se divida en varias subconsultas, basado en el resultado de una primera consulta, se pueden generar consultas específicas sobre un tema -> esto las estrategias SOTA entinedo que lo tienen en cuenta.
- HyDE: en lugar de hacer la consulta con la pregunta, pedirle al LLM que genere una respuesta y buscar en base a esta respuesta. Puede no funcionar bien si el dominio requiere que el LLM sepa algo específico -> podría ser interesante intentarlo #todo

##### RAG modular
- Incorporar otros sistemas de búsqueda en fuentes que no tengan RAG con LLMs que busquen.
- Memory module: usar la memoria como rag también para buscar documentos relacionados en las propias respuestas del LLM, en SOTA debería haber algo de esto avanzado #todo
- Módulo de generación extra: en lugar de pasar los documentos directamente, usar otro LLM para sacar la info relevante -> sota también tendrá algo de esto #todo
- módulo adaptativo a la tarea: tener prompt templates para cada tarea para buscar en el sistema RAG. UPRISE: Universal Prompt Retrieval for Improving Zero-Shot Evaluation, tienen una BD de prompts. primero se usa el modelo ajustado para calcular la similitud del query con el documento (procesando cada par query-documento) y luego con un LLM "frozen" se le pasa los templates más adecuados y se genera el prompt final para hacer una búsqueda RAG en una base de datos grande. Muy interesante pero pinta muy complejo. #interesante
- Módulo alineador: se ajusta un LLM "alineador" usando aprendizaje por refuerzo (se mencionan varios papers con varias técnicas) para dado un query alinearlo mejor a la base de datos con los documentos para que el RAG posterior sea más efectivo.
- Módulo validador: una vez obtenidos los documentos, descartas los que se consideren no válidos.

##### Patrones modificando módulos

- ##### Query Rewriting for Retrieval-Augmented Large Language Models
	 #interesante, no parece tan difícil
	RL para entrenar un rewriter del query para buscar en el RAG.
	Usan un T5 de 770M, primero se hace una fase de "warm up" con un SFT y luego se afina con un RL.
	Para el SFT tienen un dataset de preguntas y respuesta. Ponen a un LLM a generar querys, con esas querys se pasan por el pipeline completo (retriever + reader) y se sacan las querys que generan respuestas correctas. Entonces entrenan con max log-likelihood contra esos querys.	
	Luego aplican RL con PPO: s -> secuencia hasta ahora, a -> vocabulario, p (policy) -> rewriter modelo, r -> calidad de la respuesta final del pipeline generada en relación al ground truth (usando el F1), se le añade una regularización con la divergencia KL.
- ##### GENERATE RATHER THAN RETRIEVE: LARGE LANGUAGE MODELS ARE STRONG CONTEXT GENERATORS
		#interesante, no parece muy difícil, se podría combinar con los documentos del RAG tradicional.
	En lugar de hacer retrieve en el RAG, generan los documentos con un LLM. Prueban a generar muchos, pero al final acaban generando parecidos. Prueban con varios prompts anotados por humanos y mejora un poco. Proponen una estrategia interesante: dada una query, recuperan documentos relevantes desde wikipedia + generados por gpt, los vecctorizan e indexan con query + doc. Luego los separan por k-means clusters. Entonces, a la hora de generar documentos en inferencia, le pasan n documentos aleatorios de cada cluster para cada documento en forma de few shot. De esta forma cada documento generado tiene el enfoque del cluster, es una forma de generar documentos más diferentes.
- ##### RECITATION-AUGMENTED LANGUAGE MODELS
		#interesante, lo de los hints no me convence, pero se podría complementar lo de las recitaciones con el paper anterior.
	Se basan en la premisa de que los humanos antes de responder una pregunta en nuestra mente recitamos información factual que conocemos.
	Primero le piden al modelo que recite pasajes de evidencia dada una pregunta (usan un few shots para que sepa la estructura), en preguntas complejas se hace un mult-hop en el que se recitan varios documentos seguidos y se les pone etiquetas tipo recite1 recite2. Es como una alternativa al CoT. Se generan varias recitaciones paralelas (top-sampling) y se elije la mejor.
	Para evitar recitaciones erróneas se usa una temperatura bastante baja y la estrategia "passage hint-based diversified recitation" Que consiste en generar hints (los path de la clasificación de documentos en wikipedia) dada una query, para basar las recitaciones en esos documentos. Para eso se ajusta el modelo para que aprenda la estructura de los encabezados de wikipedia.
##### Patrones añadiendo módulos
- ##### DEMONSTRATE–SEARCH–PREDICT: Composing retrieval and language models for knowledge-intensive NLP
	Proponen DSP, que actua como protocolo de comunicación entre LM y RM(retrieval model): D(crear queries pal training set) S(buscar queries nuevas en el hop) P(predecir final answer). Código en Github, usarlo estaría de locos.
	La implementación se menciona que utiliza objetos llamados "Example" a las que se les puede aplicar transformaciones de 3 tipos: 
	- multihop_demonstrate: sirve para buscar ejemplos few-shot para los ejemplos del dataset de entrenamiento. Se supone que esto pretende reemplazar el backpropagation en un ajuste fino, al pasarlo por few-shots se puede ajustar de forma sencilla el dominio llamando al anotate y cambiando los ejemplos de entrenamiento . Dicen que a la hora del few-shot pueden seleccionar ejemplos aleatorios o k nearest neightbours.
	
	- multihop_search: Dado el retrieve, debe definir el siguiente paso, ya sea responder o hacer un hop nuevo: 
		En este paper mencionan que ellos promptean a un LLM para que haga lo de condensar y lo de retrievear, pero estas estrategias son más difíciles de implementar pero más eficientes si se implementan bien (dicen que las usan en una segunda versión más compleja): 
		###### Answering Open-Domain Questions of Varying Reasoning Steps from Text
		#interesante, lo de los hops está muy bien, a lo mejor con los modelos razonadores ya viene integrado, se podría mirar si combinar algo así con lo del clasificador para saber si parar o no.
		
		La idea es generar los hops en el Reader para resolver la pregunta con varios retrieves razonando.
		Se ajusta un modelo encoder como BERT pasándole la traza del reader hasta ahora con tókenes especiales. Este decide si "SPAN", la respuesta se puede extraer del texto, SI / NO para preguntas binarias o NOANSWER si no se puede deducir de la traza. En lugar de usar solo la clase predecida se normaliza con "answerability" con las probabilidades para que no afecte tanto la longitud de la traza. En el caso de que no sea suficiente, un reranker le da una puntuación a cada documento determinando su utilidad para resolver la tarea (utiliza un BERT al que le mete la traza completa y el documento añadido a evaluar), le añade a la traza solo el más útil y le pasa la traza completa al retriever para que genere nuevos documentos. Para entrenar tanto el encoder como el reranker generan trazas de entrenamiento. Para ello tienen la base de datos QA con documentos relevantes. Entonces hacen un SFT de los documentos obtenidos con los documentos obtenidos en las trazas, le pasan tanto trazas útiles como inútiles para que el modelo aprenda a distinguir (son útiles si el documento generado por esa traza está en el gold standard de documentos útiles para ese dato).  Para entrenar con relevantes e irrelevantes se entrena como un discriminador que intenta maximizar la difereencia entre ambas clases, utiliza el loss NCE.
		
		##### Relevance-guided Supervision for OpenQA with ColBERT
		Proponen para entrenar un retriever sin datos ground truth de qué documentos son útiles y cuales no, hacer varias rondas de generar datos con retriever y ajustarlo con los mismos datos. De esta forma se van generando cada vez mejores datos con cada vez un mejor modelo. #todo, si ajusto un retriever con alguna de las técincas de otros papers esto estaría muy bien aplicarlo
		
		##### Baleen: Robust Multi-Hop Reasoning at Scale via Condensed Retrieval
		#todo, probar lo de condensar es muy interesante, si hago colbert pues también el otro. Mencionan en DSP que lo de elegir el orden de los documentos disponibles no haría falta porque en la fase demonstrate se generan esas interacciones complejas de forma automática.
		Proponen aplicar dos niveles de condensación: 
		- En lugar de pasarle todos los documentos al reader, resumirlos en "facts" que son frases
		- En lugar de añadir a la traza todos los facts, se agrupan de forma que eliminen facts supérfluos
		También proponen el módulo retriever "FLIPR" (usan bert-base). Es parecido al ColBERT, pero en lugar de sumar la similitud de todos los tokens, solo considera los más parecidos (argumentan el por qué, focused late interaction). Además, en lugar de usar solo la consulta para buscar en el rag utilizan también los "facts" de la traza.
		También proponen un entrenamiento en varias etapas como el anterior paper. La idea es que los documentos del gold standard están desordenados respecto a los hops, entonces primero entrenan un retriever para que genere las trazas para el primer documento retrieveado. Luego entrenan otro retriever para dadas las trazas anteriores, y el gold standard pero restándole los documentos ya retrieveados. Así sucesivamente (se entrena para generar las querys que generen con RAG documentos útiles)
		El condenser lo entrenan también (usando Electra-large): Le pasan las oraciones de la traza + cada oración de el rag actual, para que discrimine si es útil o no -> el electra genera el embedding de la oración que es como el CLS de BERT, se pasa por un FC para decidir si es o no relevante, se usa crossentropy.
		El segundo stage del condenser se entrena también aparte. Función de pérdida: 
		 - Softmax sobre todos a la vez (cross-entropy), dandole más valor a las etiquetadas como relevantes
		 - Clasificación binaria sobre cada una (binary-cross-entropy), dado el valor que se le asigna a cada una se indica un umbral para la que se consideran relevantes.
		La función de pérdida considera ambos a la vez.

	También a la hora de retrievear los documentos generan varias queries y fusionan los documentos. Para ello primero sacan con estrategia parecida a Combsum los más relevantes (cogen modelo ajustan para que diga importancia del documento para la query y suman si el doc sale en más de una query), luego se genera un resumen de los docs (con LLM) y se selecciona el más probable que ayude al query. #interesante, otro paper creo que hacía algo parecido, mirar como se puede combinar esto con otras estrategias.
		
		
	- multihop_predict: se ejecutan varios samples paralelos (con sus propios multihops), para elegir hay muchas estrategias, se puede hacer CoT y elegir la más popular (hacer un string.lower() y elegir la que más sale), solo en caso de que el answer sea algo muy específico.
	 Se puede coger las diferentes answers y aplicar las siguientes técnicas con un frozen LLM:
	 ##### STANDING ON THE SHOULDERS OF GIANT FROZEN LANGUAGE MODELS
	- Prompt learning: el prompt tunning tradicional solo se puede adaptar para una tarea. Proponen Input-dependent prompt tunning (ID-PT). Se pasa un prompt aprendido por un T5 congelado, el cual se supone que captura representaciones lingüisticas, esto genera salida variable, con unas capas adicionales se crea un prompt de tamaño fijo ajustado a la tarea de x.
		 
![[Pasted image 20250227102452.png]] 

- Frozen LLM como reader: Dicen que ajustar un reader suele ser muy costoso (mucho input length) -> suelen ser pequeños. Entonces proponen primero ajustar un reranker para obtener los documentos más útiles solo, y luego aplicar prompt learning sobre un LLM grande para que actue como Reader y genere la respuesta. #todo -> lo del reranker ya se mencionaba en otras estrategias (aquí mencionan también un paper que explica bine como hacerlo), pero se puede probar también a ajustar el input prompt. También entiendo que esto es una forma de combinar el RAG pre vectorizado con una técnica de reducir los documentos, es como combinarlo con lo del colbert, no se si se podría añadir eso también. También se puede aplicar una para cada multi-hop query, y luego con los resultados de cada multi-hop query aplicar uno de estos, como una segunda capa.
![[Pasted image 20250227103538.png]]

- LM Recursion. Proponen ajustar un prompt para un LM grande para que genere la respuesta para una pregunta, samplear varios de este LM y luego ajustar otro prompt para otro LM para que dados estos samples elija o genere la respuesta correcta. 
- Neural Recursion: dicen que al conectar la salida de uno a la entrada del otro se pierde mucho tiempo de inferencia. Entonces conectan la salida en embeddings de uno con la entrada a la primera capa de atención de la otra, lo llaman Connector -> ambos LM deberían ser el mismo modelo congelado para compatibildiad de embeddings. #interesante, mirar si esto puede caber en algún lado.

##### RANKGEN: Improving Text Generation with Large Ranking Models
Entrenan un modelo para mejorar la generación de texto, dado un texto original este evalúa la continuación de otro texto. Utilizan técnicas de entrenamiento avanzadas para distinguir negativos que no lo parecen. 
Esto se puede usar para meterle el query del rag como input y evaluar los documentos, no sé cuál sería su rendimiento frente a ajustar desde 0 un BERT, quizás habría que ajustarlo también este para que actúe como reranker, podría dar mejores resultados.

Se menciona que también es posible pasarle los documentos si son pocos a un LLM -> tiene pinta que lo mejor es desde muchos documentos hacer rerank y pasarlos a un LLM, valorar esto #todo
Dicen que en DSP se pasan los documentos para los hops de forma secuencial, y se van agregando en lugar de fusionando, luego ejecutar esto de forma paralela con varias trazas y fusionarlo esta vez sí en en un LLM que decida cual respuesta elegir.

Propuesta DSP del paper: 
- Demonstration -> Crear los ejemplos "demonstrations", usan el sistema en zero-shot para ir creando trazas válidas, cuando el resultado es correcto anotan la traza para luego pasar los ejemplos en forma de few-shots.
- Search -> LLM? genera query a buscar usando los ejemplos del demonstrate como few-shots. Buscan k=7 en el RAG (usando colbertV2). SearchV2 usan simulación de IRRR y Baleen. Lo que hace es primero generar summary del contexto, después genera query y retrievea los documetnos, después otra vez al search o al predict si devuelve N/A (ya se puede sacar el resultado). Lo de fusionar dicen que es para en cada search se pueden poner por ejemplo 10 queries paralelas y luego fusionar todos los documentos generados. Para esto le dicen de pasar una función de fusión, ellos usan una variante de CombSUM, igual lo del Baleen se podría meter aquí.
- Predict -> La idea es pasarle a un LLM las demostraciones, el contexto y la pregunta para que responda. Dicen de ejecutar múltiples responders paralelos y luego elegir la mejor opción. Para esto comentan de elegir la opción más frecuente (cuando la respuesta es muy específica) o utilizar un módulo ranker que defina cuál es el mejor.

#todo: se podrían definir 3 niveles para un agente con RAG :
- el RAG sin multi-hop, osea limpiando los datos y con un Colbert (y sin este)
- el RAG usando un DSP 
- el RAG usando un DSP y añadiendo alguna fumada como los del Baleen / IRRR / prompt tunning


- ##### Enhancing Retrieval-Augmented Large Language Models with Iterative Retrieval-Generation Synergy
Se supone que supera a DSP.
Destilan retriever desde ranker. Sacan documentos desde query original, después con un modelo LLM sacan Y1 desde el q y los docs. En la siguiente iteración pasan yt-1 + query al retriever para que saque más docs y otra vez así en bucle. La idea es que como el retriever está destilado desde el ranker diga la semántica que falta. Osea las primeras respuestas deberían estar mal y según va generando respuestas al final debería estar bien. 
##### Measuring and Narrowing the Compositionality Gap in Language Models -> (Self-ask)
técnica parecida a chain of thought donde se pregunta y se responde a sí mismo -> supongo que el reasoner esto lo hace automáticamente

##### Answering Questions by Meta-Reasoning over Multiple Chains of Thought 
Utilizan esta técnica de razonamiento junto a los documentos.

Dicen que self consistency trata de hacer varios CoT paralelos y coger el answer más repetido. El problema es que a veces aunque el resultado sea incorrecto los pasos intermedios tienen info útil.
Basicamente cogen varios CoT paralelos que iteran entre razonar y retrievear información y luego concatenan todos los pasos en uno solo, luego un modelo razonador tiene que decidir desde todos los pasos cuál escoger.

- ##### SELF-RAG: LEARNING TO RETRIEVE, GENERATE, AND CRITIQUE THROUGH SELF-REFLECTION
Entrenan un modelo (Llama 7b/13b) end-to-end para que dada una query responda en segmentos separados por varios tokens especiales: 
- Retrieve: después de cada segmento si es necesario o no rag. Si pone que sí entonces el modelo para de generar se hace el rag y se le mete de nuevo con los docs.
- IsRel: si el documento provee info relevante para resolver x
- IsSup: la repuesta y es verificada por d
- IsUse: el segmento es útil para x
Primero utilizan gpt-4 para obtener datos de entrenamiento. Con diferentes prompts anotan cada uno de los tokenes especiales para varias preguntas / segmentos de texto.
Con estos datos entrenan un modelo crítico. Este aprende a predecir los tokenes reflectivos especiales.
Después, se utiliza este modelo Crítico para generar datos para el modelo generador (el bueno). Entonces se va pasando la pregunta y respuesta por el crítico para que este vaya generando los diferentes tokens y los van concatenando a la respuesta:  
![[Pasted image 20250228172550.png]]

Comentan que también pueden triggerear el retrieve si la probabilidad del token retrieve = yes normalizado respecto a todo el output supera un límite.
Dicen que al usar RAG se extraen k documentos, y que por cada documento se genera en paralelo una traza. Utilizan el beam search usando la siguiente técnica de evaluación: 
probabilidad de y dada la traza (usando el modelo generativo) + probabilidad normalizada del token más deseable de cada token reflectivo especial
De alguna forma tienen la capacidad de cambiarle el "weight" a cada token especial para que el modelo le de más importancia a cada tarea.
#interesante, pinta muy difícil de implementar todo, a lo mejor se podría utilizar el modelo que han creado ellos. Lo del beam search es muy buena idea, mirar si se puede usar en los demás #todo

## Retriever

 - Chunk optimization: tener en cuenta el embedder utilizado a la hora de elegir el tamaño(sentence transformer ~sentence, text-embedding-ada-002 ~256-512). TAmbién el tamaño esperado de la aplicación. 
-overlapping sliding window: es dividir por chunks de tamaño pero superpuestos algunos tokens para no perder info semántica (bloque b tiene parte del bloqeu a y c repetido). 
-Small2Big: consiste en indexar documentos pequeños con información precisa, y a la hora de pasarle al modelo el documento pasarle el documento grande con más contexto. (osea indexas varios desde un documento grande)
-Abstract embedding: indexar el resumen y luego pasarle el documento entero.
-Metadata filtering technique: por ejemplo por etiquetas en stackoverflow
-Graph indexing: crear relaciones entre todumentos
- Ajustar modelo embedder: muy útil para ajustar al dominio y a la tarea -> LlamaIndex parece tener una forma sencilla de hacer esto. Comentan que PROMPTAGATOR utilizan LLMs para crear few-shots query generators, 
estos se supone que ajustan un embedder usando algunas técnias, #todo leer esto: https://arxiv.org/abs/2310.07554
- alinear query con documento: ITER-RETGEN va generando un pseudo-documento generando las querys y pegando los documentos.
##### Precise Zero-Shot Dense Retrieval without Relevance Labels
Proponen en lugar de buscar la query en el RAG, pedirle a un LLM que genere la respuesta a esa query (halucinando que flipas), y luego buscar ese documento en RAG para encontrar docs reales. #todo, esto se podría combinar con los demás como complementario

##### Query Rewriting for Retrieval-Augmented Large Language Models -> ajustar rewriter para buscar en RAG

#### TAKE A STEP BACK: EVOKING REASONING VIA ABSTRACTION IN LARGE LANGUAGE MODELS
Le dicen al modelo que de un paso para atrás y que genere una pregunta abstracta, esta pregunta se usa para hacer la query en el RAG #interesante, se podría considerar como otro añadido, cuidao al usarlo con modelos razonadores
"You are an expert at world knowledge. Your task is to step back and
paraphrase a question to a more generic step-back question, which is
easier to answer. Here are a few examples:"
- Ajustar embeddings con un adapter: LlamaIndex tiene un método "listo para producción" para hacerlo de forma sencilla. Entiendo que es más sencillo pero menos efectivo que ajustar todo el embedder. Hay un paper para entrenar el adapter en caso de que los docs estén estructurados y el query no (SANTA).
##### Structure-Aware Language Model Pretraining Improves Dense Retrieval on Structured Data
Proponen estrategia para alinear semánticamente datos estructurados y no estructurados. Tienen dataste de datos estructurados y en lenguaje natural que son parecidos y no parecidos. Los codifican con un T5 a embeddings y usan un aprendizaje contrastivo para intentar alejar los no parecidos y acercar los parecidos.
Esto no parece muy útil para el TFG a no ser que haya un caso con datos estructurados que no tiene pinta.

- Alinear el output del retriever con lo que el LLM necesita: 
##### Augmentation-Adapted Retriever Improves Generalization of Language Models as Generic Plug-In
#interesante, está el código. Pinta difícil pero factible.
Cuando no se puede ajustar el modelo junto al retriever (LLM caja negra), o se quiere variar el LLM
Entonces utilizan estrategia FiD (Fusion in Decoder, aplicar atención individualmente en el encoder y luego aplicar atención cruzada a todos los documentos en el decoder) para entrenar un embedder y posteriormente acoplar cualquier LLM. 
Tienen datos anotados de qué documentos son relevantes para unas query. Cogen un encoder-decoder como T5 para aplicarle atención a los documentos retrieved en el módulo encoder de forma individual. Luego, en la fase de la atención cruzada aplican la atención a todos los documentos a la vez. Cogen esta atención cruzada para determinar cuál documento es el más importante, juntan ground truth con las predicciones del modelo FiD -> FiD score = el score de un documento será el promedio de atención de varias capas para los tokens de ese documento sobre el primer token generado por el decoder, pq se supone que este atiende a todo el contexto del decoder al ser el primero.
Entonces utilizan estos datos para entrenar el retriever, que es el embedder.  Hacen crossentropy contrastivo, para que los documentos y los query que son relevantes generen embedding cercanos, y los que no pues no.
##### REPLUG: Retrieval-Augmented Black-Box Language Models
Tras extraer los documentos añaden cada documento en un flujo separado al input y se lo meten independientemente al LLM. El siguiente token de todos se añade de forma autorregresiva como el token más probable teniendo todos los flujos en cuenta.  #interesante no sé si se pierde contexto de esa forma pero bueno.
Se calcula la probabilidad del retriever (embedder) que le da a cada documento como una normalización de la función de similitud entre el documetno y el input (puede ser por ejepmlo la similitud coseno). Luego se calcula la probabilidad que le da el LLM al documento, concatenando cada documento individualmente al input, y sacando la perplejidad del modelo al pasarle el y del ground truth. Entonces, para entrenar el embedder se calcula KL entre ambas distribuciones. Como según se actualiza el embedder cambian los embeddings, tienen que re vectorizar la bd de nuevo cada T pasos de entrenamiento. No se como sacan la perplejidad del modelo de caja negra, igual tienen que hacer una aproximación poniendo temperatura 0 y haciendo un Bleu.
Comentan que utilizan Faiss para indexar. Faiss propone que utilizar una búsqueda semántica tradicional es muy costoso (al final se comparan todos los vectores por fuerza bruta), proponen varios algoritmos alternativos que sacrifican precisión pero son más rápidoos.
##### UPRISE: Universal Prompt Retrieval for Improving Zero-Shot Evaluation
Proponen ajustar un retriever para cualquier modelo para que extraiga prompts para tareas no vistas, primero lo entrenan sobre LLM pequeño y luego lo usan con LLM más grandes incluso de caja negra. El RAG se hace sobre los prompts para luego pasársela al LLM con el input en forma de zero-shot. #interesante, aplican RAG sobre los prompts en lugar de sobre los documentos, no se hasta que punto será efectivo eso xd.
Anotan dataset de prompts útiles para ejemplos de preguntas y respuestas, para cada input x sacan prompts útiles p, se los pasan a un modelo congelado el cual genera una predicción y. Lo comparan contra el ground truth y sacan métrica F1, Rouge... Entrenan con pérdida NCE.
##### Few-shot Learning with Retrieval Augmented Language Models
#todo, si ajusto embedder mirarme estas estrategias
Explican varios métodos de pérdida para ajustar el retriever:
-Attention distillation:Usando un encoder-decoder, pasan el input con los documentos por el encoder. Luego, utilizan la atención promedio del decodificador a cada documetno para determinar la relevancia de cada documento. Utilizan una fórmula para calcular la divergencia kL de la probabilidad retriever (dot product entre documento e input) con la del modelo: 
![[Pasted image 20250301113006.png]]
![[Pasted image 20250301112330.png]]
-End-to-end training of Multi-Document Reader and Retriever:  Se utiliza la probabilidad que el modelo asigna al output dado un solo documento y el input, el p retr es también el doct product de la estrategia anterior:
![[Pasted image 20250301112857.png]]
-Perplexity Distillation (PDist): como simplifiación del anterior, la idea es ver x documento cuanto mejora la perplejidad respecto a los demás documentos: 
![[Pasted image 20250301114031.png]]
Entonces, se hace la divergencia KL entre pk y la probabilidad del retriever p(retr).
-Leave-one-out Perplexity Distillatio: La idea es ver cuánto empeora la perplejidad del modelo al eliminar cada documento -> ploop(dk):
![[Pasted image 20250301114329.png]]
Se usa la log-probabilidad negativa para que -logplm(...) sea la relevancia de cada documento y se aplica posteriormente otra vez KL divergencia respecto al score del retriever.
Comentan que obviamente esta estrategia es más costosa porque tienen que ir computando cada combinación de eliminación de documentos.

Comentan como en anteriores que se deben actualizar los embeddings del index periódicamente actualizandolo respecto al retriever ajustado.
Otra opción es hacer un retrieve de muchos documentos primero y luego re-embedear con el retriever actualizado y hacer un re-rank con el modelo siendo ajustado. También se puede entrenar solo para encodear el query, y los del document dejarlos con el preentrenados, para evitar sobrecostes.
La estrategia de loss no parece variar mucho los resultados, la tercera estrategia parece la mejor en overall.

- Alinear el output del retriever con lo que el LLM necesita pero sin entrenar el retriever tampoco, con un adapter que adapte el output del retriever: 
Varias técnicas: PRCA, TokenFiltering, RECOMP, PKG
#todo -> mencionan que esto es muy robusto porque pueden añadir un adapter para diferentes retrievers / generadores, es como un extra más.

##### PRCA: Fitting Black-Box Large Language Models for Retrieval Question Answering via Pluggable Reward-Driven Contextual Adapte
Interesante pero pinta complicado con el RL.
Proponen crear un adaptar que dado un query y varios documentos genere el contexto para el generador (como un resumen). Lo entrenan en dos fases, primero un sft con el ground truth. Luego un RL con un LLM de caja negra, para ello definen el reward como el Rouge-L score entre el resultado del LLM y el resultado del ground truth.
![[Pasted image 20250302180326.png]]
Usan divergencia KL para regularizar el reward, para no desviar demasiado del entrenamiento anterior.
Usan PPOa quieren aplicarlo a nivel de token pero como LLM de caja negra pues no tienen las probabilidades -> esperan al token EOS, entonces sacan las probablidades del modelo que están entrenando sobre la respuesta dada y entonces ponderan el reward para cada token y aplican el proceso PPO para todos los tokens.
##### RECOMP: IMPROVING RETRIEVAL-AUGMENTED LMS WITH COMPRESSION AND SELECTIVE AUGMENTATION
#todo, lo de generar resúmenees es muy interesante, considerarlo.
Proponen añadir al output del retriever 2 compresores: 
-Extractive compressor: hace rag con sentences del documento. Encodea ambos sentences y query y recoge los n sentences más relevantes, entiendo que lo entrenan para que de los más relevantes.
Lo entrenan con contrastive Log likelihood, siendo el positivo el top sentence. Tienen un dataset para esto.
-Abstractive compressor: Cogen el query y los docs (filtrados los sentences), y con un LLM pequeño generan summaries. Este LLM lo destilan de gpt 3.5, quieren que el compresor sea pequeño. Hacen un filtrado de resumenes para el training set. Si el resumen tras añadirlo al query genera una perplejidad en el modelo para la respuesta superior al query sin ningún documento añadido entonces no añaden el documento al dataset.
##### Optimizing Retrieval-augmented Reader Models via Token Elimination
Dicen que en la estrategia FiD la fase del encoding es más costoso computacionalmente pero la del cross-attention es más costoso en tiempo. Para reducir el costo de la fase del decoding proponen eliminar los tokens menos relevantes, usando la atención del decoder.
Para saber cuál capa del decoder es más útil para esto, cogen para un ejemplo 100 docs, y ponen el primero el considerado mejor (gold). Entonces cogen para cada capa los top p tokens con más atención, y deciden la mejor capa como la que más tokens tiene del gold.
Luego en inferencia, calculan hasta la capa 3 la atención, para filtrar los top k tokens en la misma fase de inferencia eliminan (filtran) las activaciones de los tokens irrelevantes y sigue para alante.
##### Augmented Large Language Models with Parametric Knowledge Guiding
#interesante, no pinta muy difícil pero pinta que cuesta bastante tiempo -> se podría añadir generando un documento con uno de estos modelos ajustados, habría que ajustarlo sobre datos que LLMs grandes no sepan, cosas de la empresa.
En lugar de hacer el rag sobre los documentos, ajustan un modelo caja blanca pequeña sobre los documentos y lo utilizan para generar documentos útiles para dada la consulta.
Primer transforman el dataset a pregunta / respuesta y entonces ajustan el modelo.
En un dataset con imágenes codifican con CLIP-ViT y le aplican cross attention a cada capa del LLama.

## Generator

- Compresión de información: un postprocesado de los documentos retrieveados para que quepan en el LLM. PRCA, RECOMP.
##### Large Language Model Is Not a Good Few-shot Information Extractor, but a Good Reranker for Hard Samples!
Dicen que los LLMs grandes no son buenos comparados con LLMs pequeños ajustados (SLMs) a la hora de extraer info relevante desde muchos documentos #todo -> tener en cuenta eso. Dicen que los LLMs son mejores en ejemplso difíciles (razonan) pero peores en fáciles, y la mayoría son tareas fáciles.
Proponen una estrategia en la que primero un retriever obtienen n docs, y quieren sacar únicamente la info relevante (resumen). Entonces utilizan un SLM para el resumen, si la perplejidad de la repuesta supera un límite, entonces ese ejemplo se lo mandan a un LLM #interesante.

- Rerank: demasiados docs hacen que el LLM pierda atención de lo importante -> reordenar docs para coger sólo lo más importante + compresión.
##### Lift Yourself Up: Retrieval-augmented Text Generation with Self-Memory
Proponen que el documento más cercano al contexto es al final el propio output del LLM. Por eso hacen un beam search, y tratan las respuestas del LLM en las diferentes Beams como memoria. Investigan que los tokens adicionales respecto al ground truth añadidos por el memory que no tienen los documentos del RAG no son difíciles de generar por el LLM (tiene confianza sobre estos), por eso no usan esa métrica para seleccionar las memorias, usan Bleu, rouge y otros. Proponen dos técnicas, en un encoder-decoder codfiicar en el generador x y la memoria separado por un token, o tener dos encoders (dual-encoder) para que codifique x y m de forma individual. Utilizan el NLL loss. #interesante, se podría incorporar algo así en un beam search como complemento, podría ser como un banco de memoria para la ejecución actual -> #todo mirar su integración con las otras estrategias de multi-hop.
##### Knowledge Graph-Augmented Language Models for Knowledge-Grounded Dialogue Generation
Pinta muy difícil y habría que tener BD bien hecha KG -> se podría plantear sobre BD de papers pero fumadita. Está la base de datos esa de microsoft y GNNs preentrenadas sobre OAG (actualizado a 2019 :(). OpenAlex tiene 300gb y es gratis, pinta fresco.
Hacen RAG sobre base de datos Knowledge graph (KG como neo4j). La idea es tener la base de datos en una GNN que aprenda a extraer info relevante de las tripletas, entonces se hace similitud entre losembeddings de las tripletas extraídas por la GNN y los embeddings encodeados por encoder LLM sobre el contexto de entrada m -> esa es probabilidad para extraer esa tripleta como información.
Se aplica la GNN offline sobre todas las tripletas y luego en inferencia se hace la búsqueda por similitud sobre estas tripletas, fumadón.
Se codifican en tripletas (doc - relación - doc) sin tener en cuenta el orden.
Mencionan que al hacer teacher forcing para entrenar el generador con los documentos extraídos el generador sólo recibe feedback (datos) del ground truth, sin tener en cuenta los tokens generados durante el entrenamiento e indepndientemente de los documentos que le pasan de contexto (exposure bias).
Entrenan end-to-end a la vez el retriever (GNN) - embedder de memoria - generador
![[Pasted image 20250303124857.png]]
~(Z) -> embedding del generador tras salida z
~(h) -> representación embedding de retriever apartir del estado h
Se hace sumatorio sobre representaciones negativas, z y h que no corresponden al par correcto
![[Pasted image 20250303125007.png]]
Para este cogen top k samples: 
![[Pasted image 20250303125218.png]]
##### SANTA (antes) -> entrenar retriever para structured data

## Augmentation in RAG

- En fase de preentrenamiento: todo lo de aquí entiendo que no me sirve pal TFG porque no me voy a poner a preentrenar un modelo. 
##### REALM: Retrieval-Augmented Language Model Pre-Training
Tratan los docs z como variable latente:
![[Pasted image 20250303140323.png]]
Se junta el retriever al transformer generador y se calcula el loss de forma conjunta tanto en preentrenamiento y ajuste fino. En pre lo que hacen es como en bert preecir token que falta, en ajuste fino lo que se predice es el rsultado. Utilizan MIPS (multiplicar los vectores) y aplican softmax -> el bakcpropagation se hace solo sobre los top k docs pa q no sea demasiado costoso.
##### Improving Language Models by Retrieving from Trillions of Tokens
Preentrenan un modelo junto a una BD para que haga retrieval automativamente. Se separa el input en chunks y por cada chunk se extraen top k doucmentos relevantes, que se integran en el sistema de atención dentro del propio modelo: 
![[Pasted image 20250303133134.png]]
Es una fumada, habría que mirarlo con más tiempo pero no me va a servir.

- Fase de ajuste fino: REPLUG y UPRISE ajustan el retriever. Self-Mem y Self-RAG ajustan el generador. Estos ajustan los dos, SURGE también entrena ambos, en GNN:
##### RA-DIT: RETRIEVAL-AUGMENTED DUAL INSTRUCTION TUNING
Entrenan un retriever y un generador. Dicen que el generador aprende a ignorar los documentos irrelevantes o erróneos.
Para el generador usan SFT con los docs, para el retriever usan el loss de dividir la probabilidad de y con ese documento en relación a los demás (como en la mayoría): 
![[Pasted image 20250303163335.png]]
Calcuar respecto al ground truth KL:
![[Pasted image 20250303163558.png]]
Dicen que funciona mejor que replug, pero claro están ajustando el generador también.

- En inferencia: DSP comunica LLM frozen con retriever, en plan qué pasarle como contexto. PKG lo de generar documentos con SLM. Recite lo de que los propios LLMs reciten su info.
##### From Classification to Generation: Insights into Crosslingual Retrieval Augmented ICL
Para idiomas con bajos recursos, encodean la pregunta, y buscan rag sobre docs de idiomas con muchos recursos. No tiene pinta que me sirva.

##### RETRIEVAL-GENERATION SYNERGY AUGMENTED LARGE LANGUAGE MODELS
Hacen la de alternar iteraciones de RAG-GAR, el input del rag es el query concatenado yt-1.
En algún moemnto hacen un refine con un prompt para que el LLM modifique la solución y otras veces un refresh. Esta estrategia ya se usa en otros.

##### Interleaving Retrieval with Chain-of-Thought Reasoning for Knowledge-Intensive Multi-Step Questions
Se intercalan pasos de Reason (CoT) con Retrieve. Se usa el razonamiento para buscar documentos relevantes. Hasta que diga stop el reason o hasta k pasos.
#todo, en las otras estrategias como dsp mirar si se puede tener una fase de razonamiento.

### Augmentation Data source
Dicen que pueden ser tokens, palabras, frases, documentos...
- with unstructured data: 
-FLARE hablan de extraer documentos solo cuando los tokens generados por el LLM tienen poca probabilidad. NO LEIDO. Retro hace a nivel de chunk (cuando lelga a x chunk busca docs), pinta parecido a self-rag, fumadita.
- With structured data

##### RET-LLM: Towards a General Read-Write Memory for Large Language Models
No creo que me sirva, me parece más interesante una gestión de memoria a corto / largo plazo.
Crean una gestión de memoria con relaciones -> fact1 - rel - fact2, ajustan el modelo para que sepa cuando llamar a read o write en la memoria. Primero hacen búsquedas por hashtable sobre los facts, si no encuentran buscan por embeddings.
Para crear los datos para ajustar el modelo crean {personas} - {employment, manager, investor...} - {organization} y crean preguntas tipo, quien es el CEO de bmw? -> se los pasan para que el modelo aprenda a generar los read. También le pasan statements y que aprenda a generar los write.
Está pensado para pasarle documetnos informativos inicialmente, que este los almacene y luego interactuar con él, no sé si es mejor que el RAG original, pero es una propuesta interesante. 
##### KnowledGPT: Enhancing Large Language Models with Retrieval and Storage Access on Knowledge Bases
Secuela a RET-LLM, proponen que el LLM genere código python que contenga las funciones de búsqueda / escritura, pueden buscar por relaciones también.
Dicen que generan los KBs tipo las bd con los documentos, y luego una PKB (personalized knowledge base) con lo que escribe el modelol

- Generado por el LLM:
  -SKR: tiene un training set de preguntas etiquetadas, con preguntas que pueden y no pueden ser respondidas sin ayuda, para que el LLM aprenda a cuando tiene que utilizar RAG y cuando no. Interesante pero no creo que sirva para el TFG, lo que tiene que buscar no es como los QA que puede que lo sepa, el código lo tiene que buscar.
  -GenRead:  lo de que generaba docs él mismo, esto era interesante.
  -SelfMen: Creaba el memory pool con el beam-search, esto también era interesante. 

### Augmentation process
- Aumentar con data unstructured: 
-RETRO: cogía cada chunk de texto generado docs parecidos -> esto ni de coña puedo hacer en el TFG
-ITER-RETGEN, IRCoT, muy interesantes, valorarlo pal TFG #todo.
-Graph-Toolformer -> 

##### Graph-ToolFormer: To Empower LLMs with Graph Reasoning Ability via Prompt Augmented by ChatGPT
Utilizan un agente que le pasan tools de buscar en una base de datos con una GNN, fumadita, explicado en [[Agentes]]

## Evaluación de RAG

Se puede evaluar de dos formas, evaluando separado el retriever (por hit-rate, precisión...) y el generador, o evaluando end-to-end, viendo la precisińo de la tarea a llevar. #todo, se podrían evaljuar las dos formas, la segunda ya supongo que integrado con el agente? o podría ser evaluando la pregunta si es correcta la que se le hace al sistema rag.

Se proponen varias estrategias para evaluar el RAG, basicamente hay 3 papers: 
-RGB: proponen 4 métricas para evaluar RAG.
-RAGAS: proponen usar LLMs-as-a-judge para evaluar el RAG en plan separando la respuesta frase por frase y viendo si cada una ha sido utilizada.
-ARES: la mítica de teniendo un generador ajustado al sistema rag, evaluar cuál es su perplejidad para diferentes ejemplos.

# Vocabulario

to falter, 	
to hinge on -> hinge visagra, depender
	

# Todo
survey en proceso: https://simg.baai.ac.cn/paperfile/25a43194-c74c-4cd3-b60f-0a1f27f8b8af.pdf

survey más arriba: https://arxiv.org/pdf/2403.14403 mirarse la parte de Multi-hop

http://proceedings.mlr.press/v119/guu20a/guu20a.pdf
https://proceedings.neurips.cc/paper_files/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf

artículo interesante de survey pero de un gitano: https://pub.towardsai.net/advanced-rag-techniques-an-illustrated-overview-04d193d8fec6

RAG en grafos? knowledge based graphs
Mirarse RAG de LangGraph.
Buscar si el SOTA tiene algo más.

chatgpt referencia sobre razonamiento: https://arxiv.org/pdf/2502.12521 

El video de langchain
