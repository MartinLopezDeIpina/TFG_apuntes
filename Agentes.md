# A Survey on Large Language Model based Autonomous

Los agentes en general cumplen varios módulos de forma común: 

### Módulo de perfil

el rol que se le dice que tiene, se puede decir directamente en plan eres un experto en x.

### Módulo de Memoria

replican la memoria en los humanos, con memoria corto, largo plazo.

- Memoria a corto plazo: entiendo que puede ser solo pasarle los k mensajes más recientes. 
##### Reflective Linguistic Programming (RLP): A Stepping Stone in Socially-Aware AGI (SocialAGI)
El agente tiene como un estado de lo que quiere hacer y lo que está pasando, de forma que hace reflexińo sobre este. Está interesante, pero entiendo que los modelos razonadores hacen exactamente esto. Aún así lo de tener un estado con lo que se queire conseguir y así está interesante.
##### SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning
Proponen un sistema autónomo de robots. Dicen que cuantas más componentes se añaden al environment más difícil es añadir todo el estado en el prompt del LLM. Para resolver esto proponen tener el estado en un grafo plegado, dandole al  agente la posibilidad de desplegar las partes que necesite. También en lugar de dejarle al agente que planee todo, utilizan el algoritmo de Dijkstra para hacer el planing inicial, y posteriormente se va refinando con otras técnicas.

El grafo es en plan a nivel de piso, a nivel de habitación, a nivel de objetos -> sofá, tele... Entonces el LLM con el api puede plegar y desplegar. 

Para planear la task se usa un LLM para planear a alto nivel, como ir a la habtiación, ir a la cocina, abrir el frigo... Luego con el algoritmo dijkstra se calcula el path óptimo para cada paso. Luego evaluan de forma iterativa la viabilidad del plan, haciendo un simulador de grafo en el que se ponen restricciones como que no pueda coger un objeto si ya tiene un objeto en la mano. El planner tiene acceso a una búsqueda semántica en el grafo para ver dónde puede obtener los objetos disponibles para hacer una tarea.
#interesante, lo de plegar el grafo se podría hacer si la estructrua del proyecto software es demasiado grande. También lo de la búsqueda semántica de qué puede hacer cada fichero, con una descripción de lo que se hace en cada fichero.

-Calypso: usa una memoria a corto plazo con descripciones del estado actual de la partida de d&d

##### Describe, Explain, Plan and Select: Interactive Planning with Large Language Models Enables Open-World Multi-Task Agents
![Pasted image 20250304162831.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250304162831.png)
La idea es que un planificador dicta las tareas a alto nivel, luego un controlador intenta ejecutar las sub goals de forma secuencial. cuando da error un descriptor devuelve la descripción del error, y un explainer explica por qué ha fallado para que el planificador haga un replan. Comentan que este approach es muy superior a simplemente planear e ir incorporando el feedback.
El módulo selector se encarga de decidir cuál tarea ejecutar antes. dicen que si la tarea es chopear oak pero hay acacia al lado que el selector tiene que decidir reemplazar la tarea. Tambié, si no hay dependencias entre tareas, que el selector elija la que más cerca o accesible tiene para hacer el agente. El módulo selector es una red neuronal FC que se ha entrenado con varias trayectorias offline, dada otro set de trayerctorias, predice cuál es la mejor, pasándole también las características del estado actual extraídas de una CNN a la que se le han pasado una imagen del juego actual, lo que predice la FC es la cantidad de tiempo que costaría cada goal si fuese la siguiente, y se pasa por un softmax para sacar las probabilidades de cada uno.

Se puede ver el plan actual como la memoria a corto plazo del agente.

##### Generative Agents: Interactive Simulacra of Human Behavior
Desarrollan un entorno con 32 NPCs cada uno con su personalidad / memoria interactuando entre ellos.
Tienen un banco de memoria, donde se registran observaciones que el agente hace, como x está leyendo un libro, el frigo está vacío...
![Pasted image 20250305104031.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250305104031.png)
A la hora de decidir qué hacer, acceden al banco de memoria con un sistema rag. Cada observación tiene un score que se basa en la media de 3 métricas ponderadas: 
- Recency, en función de hace cuanto en tiempo del juego sucedió
- Importance, del 0 al 10 le promptean al LLM para que lo evalue, 0 es lavarse los dientes, 10 es dejarlo con la novia
- Relevance, cuánto importa para la acción actual, es un coseno similiarity con el contexto actual.
Entonces se añaden los top ranked memories al prompt del agente.

También registran otro tipo de memoria que le llaman reflexión. Sólo se registra cuando el score de las últimas observaciones superan un límite fijado, sucede sobre 2 o 3 veces al día. Entonces promptean un LLM para que genere 3 destacables high level questions sobre las observaciones, luego usan RAG para obtener observaciones (incluyendo las reflexiones) relacionadas con cada pregunta. Entonces con cada pregunta se promptea al LLM para genere 5 reflexoines sobre la pregunta y las memorias extraidas, y se guardan las 15 reflexiones en memoria. Las reflexiones incluyen referencias a las memorias específicas de las que se ha extraído esa reflexión.

Al inicio del día se hace un plan para el agente, primero se promptea para que lo haga de forma abstracta y luego subtareas dentro de cada tarea. Este plan se guarda en el mismo banco de memoria, depende del retriever que considere necesario para extraerlo.

En cada time step se registran las observaciones, se extraen las memorias y se decide qué acción tomar. Se le promptea al LLM para decidir si seguir con el plan actual o replanearlo dada la situación actual. Se le pasa como un summary con la descripción del agente, la hora, la observación actual y las observaciones relevantes para decidir cuál acción tomar.

Los diálogos son al final observaciones en plan x agente decide hablar con otro, este le llega la observación de que le hablan, entonces el LLM debería replanear, obtener memorias sobre esa persona, y decidir tomar la acción de conversar con el otro.

#interesante, lo del banco de memoria extayendo por varias métricas puede ser interesante. 
##### Ghost in the Minecraft: Generally Capable Agents for Open-World Environments via Large Language Models with Text-based Knowledge and Memory (GITM)
Otro en el minecraft.
Es interesante lo de que tienen primero un agente "Decomposer", que dado el objetivo define las subgoals a realizar de forma abstracta. A este le pasan info del knowledge del juego para decidir qué tiene que hacer. Luego estos subgoals se los pasan a un Plannner que tieneacceso a los tools / feedback, además del memory.
El módulo de memroia dicen que guarda las trazas anteriores, para hacerle un rag en base a cuáles tareas similares a esta que han acabado en éxito existen.
![Pasted image 20250305201859.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250305201859.png)
##### Reflexion: Language Agents with Verbal Reinforcement Learning
El mítico tutorial de langgraph basicamente donde evalúa la respuesta y otro genera feedback y se le pasa al actor.
El actor recibe también memoria corto largo plazo.
No sé si esto ya está obsoleto al usar modelos razonadores.
##### Unleashing Infinite-Length Input Capacity for Large-scale Language Models with Self-Controlled Memory System
Proponen un esquema para añadir contexto de memoria a largo-corto plazo al prompt del modelo. 
Proponen un Memory controller, que es un agente que con un prompt decide si es necesario acceder a memoria, y después, si es necesario añadir los documentos enteros o sólo el resumen.
Al acceder a la memoria se devuelve, el flash memory, que son los mensajes anteriores, y activatoin memory, que se extraen usando un rag por 2 métricas, la similitud y hace cuanto se generaron.
Las memorias contienen obseración (input del usuario), la respuesta del sistema y el embedding.

![Pasted image 20250305123526.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250305123526.png)
#interesante,es bastante sencillo,  como combina la memoria a largo y corto plazo. Lo del controlador de memoria también está bien, para decidir si es o no necesario acceder a memoria conversacional. Se podría implementar esto únicamente para memoria conversacional, no para el RAG de las docs.

##### MemoryBank: Enhancing Large Language Models with Long-Term Memory
Dicen que según la ley de olvido de Ebbinghaus Forgetting curve theory los humanos van olvidando ciertas cosas, ellos proponen hacer algo parecido actualizando la memoria a largo plazo.
Añaden un timestamp a cada objeto de memoria para facilitar actualización.
Crean una jerarquía de memoria en la que entiendo que cuanto más distante más abstracto es el resumen de las memorias.
Las memorias se acceden usando RAG.
![Pasted image 20250305143724.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250305143724.png)
dicen que la importancia para retener esa información esté definida por t (el tiempo desde que se guardó esa memoria), y s (la importancia que tiene), s dicen deinicializarlo a 1 y cada vez que se accede a esa memoria sumarle 1. 

#### Formatos de memoria
- texto natural:
##### Voyager: An Open-Ended Embodied Agent with Large Language Models
Proponen una técnica alternativa al aprendizaje por refuerzo en el que el agente aprende interactuando con el entorno y guardando habilidades en una base de datos. Usa:

- Curriculum automático -> el agente va aprendiendo skills de forma gradual, de fácil a difícil
    
- Prompting iterativo -> las skills que genera son al final funciones que se pueden llamar entre ellas. Estas pueden llamar a la api de minecraft para interactuar con el juego. El iterativo es porque primero gneera el código, lo ejecuta y analiza el resultado, con errores que puedan salir de por ejemplo me faltan palos pal crafteo. Y refina el código.
    
- Librería de skills -> Guarda las skills que va generando en una base de datos y las indexa por embeddings para poder un RAG.

##### Odyssey: Empowering Minecraft Agents with Open-World Skills
Continuación de Voyager, utilizan un Llama ajustado en lugar de gpt. Lo entrenan con preguntas y respuestas de la wiki de minecraft (generan preguntas de abc como datos de train) para que el modelo tenga conocimientos del juego.

Utilizan varios agentes:

- Planner -> dice en alto nivel los objetivos siguientes a completar
    
- Actor -> intenta ejecutar los objetivos de alto nivel con las funciones disponibles haciendo rag en los skills y decidiendo cual elegir
    
- Critic -> decide si lo que se ha ejecutado es correcto, dando feedback en plan No hay hazadas en el inventario!

- SQL: Chatdb almacenan memoria en sql y van haciendo un multi hop para hacer operaciones.
- listas estructuradas: 
-GITM -> almacenan los objetivos de una forma jerárquica.
-RETLM -> almacena tripletas de relaciones. 

#### Operaciones en memoria

- Lectura de memoria: Lo de tener eRQ4: The Effect of Interactionn cuenta recency, relevance e importancia -> esto 100% meterlo #todo
![Pasted image 20250305202453.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250305202453.png)
- Escritura en memoria: 
-GITLM -> se guardan las acciones exitosas en la memoria para cada goal. Cuando llegan a 5 se agregan usando un LLM para resumir.
##### Memory Augmented Large Language Models are Computationally Universal
Proponen usar un LLM como si fuese una cpu y la memoria como la ram, escribiendo valores en memoria (en lugar de direcciones nombres pa q sepa)
No hacen un agente que resuelva problemas, sino una máquina de turing que puede interpretar cualquier problema, le tienes que ir metiendo los prompts en una dirección de memoria como si fuesen instrucciones xd.
Lo interesante es que como usa variables como direcciones de memoria no se puede repetir la memoria, esto ni de coña usarlo en el TFG.

-RETLM -> eliminan la memoria no usada en forma de fifo, no se yo si eso es buena idea xd, osea para la memoria en corto plazo vale, pero de largo plazo no.

- Reflexión sobre memoria: 
-Generative agents que generaban queries sobre sus propias memorias, esto hacerlo si o si #todo

##### ExpeL: LLM Agents Are Experiential Learners

Proponen pasarle al agente ejemplos few-shot sacados de un pool con rag, para pasarle ejemlos lo más parecidos posibles. #todo
Además, antes de crear el pool hacen un agente que le dan acceso a un ejemplo bueno y uno malo para la misma tarea, y le dicen que saque insights y reglas, proponen un método de añadir, modificar, elimianr reglas actuales. Luego esos insights los pasan comom normas a seguir al LLM en inferencia. #interesante
Luego hacen un ajuste fino del agente con las experiencias anteriores.

### Módulo de planning

- planning sin feedback:

##### Planning with Large Language Models via Corrective Re-prompting
![Pasted image 20250306095451.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306095451.png)
Proponen, que LLM generativo decida qué hacer en el siguiente paso, pasarlo por un clasificador (RoBERTa) para que de la siguiente acción. Luego lo pasan por un módulo que chequea si la acción es posible (han creado sus propias rules), si gneera un error, se le pasa a un módulo de prompting (otro LLM), que decide lo que está mal, egnera una propuesta para reemplazar y lo pasan otra vez por el clasificador. #interesante, lo de que te de error con reglas y luego feedback está muy bien, no se si se podría aplicar en el TFG, pq no se si hay una environment con unas reglas fijas. Lo de clasificar al salida del LLM no se yo, osea al final le puedes pasar al LLM las tools directamente y no tienes que entrenar el clasificador. Supongo que un una tarea muy específica podría funcoinar mejor.
Definen 3 niveles de dar feedback, diciendo el error y ya está, dando la acción que ha fallado con el objeto relacionado, dando la acción, el objeto y la razón por la que ha fallado. dicen que la mejor depende de la capacidad del LLM que genera el feedback del error.
En los entornos en los que no hay unas reglas directamente definidas (full NLP), proponen medir si la acción es correcta o no mediante una combinación del log-likelihood y el cosine similarity (no sé yo si esto va muy bien):
![Pasted image 20250306100809.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306100809.png)
También proponen re-sampling: cuando falla una acción, pasar al Roberta y pillar las k acciones más probables en base a la ecuación anterior e ir probando.

##### ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models
Dicen que los agentes ReAct gastan muchos tokens en el proceso de observación, proponen saltarse esta parte. Entonces un agente primero genera un plan cno los diferentes workers a los que va a llamar, los workers hacen su movida y luego un solver coge todas las soluciones y resuelve el problema.
![Pasted image 20250306101954.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306101954.png)
Argumentan que es más efectivo ajustar su planner que el agente react, ya que este se ajusta para el think - action - observation con las tools integradas, las observaciones dependen de las tools específicas que se estśen usando para eje ejemplo. En cambio el planner pues no usa tools específicas del ejemplo, osea en lugar de las tools y sus observaciones esepcíficas se expone a los workers y sus tareas, es como un razonamiento más abstracto. 

##### S WIFT S AGE : A Generative Agent with Fast and Slow Thinking for Complex Interactive Tasks
Intentan imitar el comportamiento del humano de dual-process Theory -> el cerebro tiene dos sistemas de pensamiento, el rápido y el lento.
Utilizan primero un módulo Swift rápido, que es un agente T5 (700M) ajustado con trazas ground truth. Este intenta sacar la siguietne acción. Si la acción falla, entonces llaman al módulo lento que es GPT4 con un agente planificador.
#interesante, se podría analizar si incorporar algo así reduce el tiempo y no afecta a la precisión, pero supongo que no hay tiempo para este tipo de pruebas.
Para el planner proponen 5 preguntas, las primeras dos sacan info del estado, la 3 le dice que haga un step by step plan, la 4 le dice que monitoree si se ah dejado algo. la 5 es como reflexión de si el plan es correcto. #interesante forma de planear. Dicen que meten las 5 preguntas en un solo input y lo sacan con un solo ouput para consultas más eficientes.
Dicen que luego le pasan el plan a un grounder para que genere el plan ejecutable (tiene sentido)
Dicen de utilizar el agente lento cuando: no obtiene una reward en 5 pasos (reward como una forma de evaluar el progreso en la tarea, la proporcoina el environment, un poco ambigüo esto, supongo que depende de la tarea específica), la acción es inválida, la acción es crítica (por ejemplo la solución al problema), la obsevación de la acción es inesperada.

##### SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS
![Pasted image 20250306114205.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306114205.png)
Basicamente varias ejecuciones paralelas para lo mismo con temp alta y quedarse con la respuesta más frecuente. 
#interesante, entiendo que se podría añadir a otro agente de forma sencilla.

##### Tree of Thoughts: Deliberate Problem Solving with Large Language Models
![Pasted image 20250306115028.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306115028.png)
 #interesante, se podría valorar en algún lado pero muy costoso y supongo que difícil de evaluar.
El ToT es crear un árbol con cada nodo como un pensamiento. Las implementaciones específicas deben definir lo siguiente: 
- cómo descomponer los pensamientos -> depende el caso pueden ser unas pocas palabras
- cómo generar los pensamiento -> se supone que se puede o samplear varios sobre el mismo paralelamente o proponer secuencialmente e ir sacando thoughts sobre los pasos anteriores.
- evaluar los estados -> con un valor para cada estado de forma independiente, o votando entre todos los estados cuál es el mejor.
- Algoritmo de búsqueda -> Mencionan dos estrategias de búsqueda,l como en el beam search de ir sacando los más prometedores en cada step, o como en monte carlo de ir a un estado final desde un step y luego ir a otro.

##### RecMind: Large Language Model Powered Agent For Recommendation
Proponen una modificación al ToT para que los estados tengan la ifnormación de todos los estados anteriores, independientemente de si fueron descartados, porque se suopne que podrían tener información útil.
![Pasted image 20250306122004.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306122004.png)
Tenerlo en cuenta si hago algo de ToT / self-consistency

##### Graph of Thoughts: Solving Elaborate Problems with Large Language Models
El código está público, se puede usar en forma de librería para hacer una implemetnación rápida.
![Pasted image 20250306125000.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250306125000.png)
Proponen representar el razonamiento del LLM en forma de grafo: Los vértices son soluciones a problemas intermedios / finales, mientras que los edges son relaciones de input para la siguiente solución: t1 - t2 -> entonces el input de t2 contiene el output de t1. También cada V puede pertenecer a una clase específica, por ejemplo si se quiere escribir párrafos, ponen el ejemplo de que los vértices puedan ser de tipo planear escritura o escritura de párrafo.
Luego proponen transformaciones sobre el grafo, que es ir añadiendo o modificando vértices para por ejemplo resumir:
- Agregar -> desde varias cadenas de pensamiento pasar a una con los edges, entonces se supone que se combinan sus puntos fuertes eliminando las desventajas.
- Refinar -> no añade nuevos vértices, modifica el actual, se crea una arista del propio nodo a si mismo? 
- Generar -> ir generando en la propia chain más pensamientos, como en el self-consistency, o ToT 
Mencionan también que implementan un sistema de evaluación para evaluar con una función un pensamiento respecto a todo el grafo. 
También dicen de rankear los pensamientos en el grafo, devolviendo k vértices para todo el grafo. 

Proponen la siguiente estructura:
- Prompter: encodea el grafo para enviarlo al LLM. Mencionan que en su implemetnación le da acceso a todo el grafo para que depende el caso de uso específico pueda usar todo lo que necesite.
- Parser: Construye el el estado de pensamiento con la información extraído de la llamada del LLM, para actualizar el Graph Reasoning State. 
- Score y validación: validar si el pensamiento satisface condiciones específicas.
- Controlador: Es el que decide la estrategia de qué pensamientos extraer, y cuales transformacoines aplicar. También decide si parar o seguir.

GoT al final es un marco teórico de estructuración de los pensamientos de un LLM. Con lanGraph entiendo que sería relativamente sencillo de implementar.
##### Algorithm of Thoughts: Enhancing Exploration of Ideas in Large Language Models
Proponen implementar algoritmos de razonamiento pero con una sola llamada, como CoT. 
Dicen que a veces es mejor que la propia cadena de llamadas y que es mucho más barato (no se yo)

##### Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents
Proponen que los LLM tienen suficiente conocimiento interno como para saber como planear tareas de forma abstracta.
Entonces cogen un LLM que genere subtareas en lengauje natural, y luego con un Roberta hacen un rag sobre las acciones disponibles.
Dicen que generan varios planes paralelos, como en SC, y luego cogen el que mayor log-probabilidad + similitud de coseno tiene (importante, van generando los steps de forma autorregresiva, osea primero eligen con los samples el paso uno, y luego con ese input generan el paso 2, beam search aquí en verdad vendría de locos??) -> log prob del step para el agente planner y similitud del step con la acción real que se elige. #todo -> esto es muy interesante, considerarlo. Decían la misma estrategia en Re-prompting. 
Dicen tambien que le meten few-shots con similaridad al query actual.
##### Generating Executable Action Plans with Environmentally-Aware Language Models
Es una mejora del anterior, añaden few shots dinámicos respecto al entorno.
Proponen primero coger los k ejemplos más parecidos por el query, y luego comparar el entorno de los ejemplos con el actual. Para comparar los estados proponen la intersección, supongo que aquí también se podría aplicar la similitud. Entonces una vez calculada la similitud de los dos, cogen el que tenga la mayor suma ponderada de estos dos.
Utilizan la misma estrategia para mapear el objeto de la acción con el entorno. Promptean al planner que haga acción-objeto (pueden ahber varios objetos), y calculan con similitud el objeto del entorno más parecido. Se podría comparar el obejto como los argumentos de la función y la acción como la acción del tool. #interesante Esto está también muy bien, pero no se donde podría llegar a meterlo en el TFG porque mi entorno no se si tiene objetos  

##### Reasoning with Language Model is Planning with World Model
Dicen de utilizar un LLM para predecir cuál va a ser la reacción del entorno. en math problem el estado son los números de las operacoines intermedias, en un razonamiento lógico el estado es el facto en el que nos estamos enfocando, y la acción la siguiente deduciión. 
Calculan el reward de cada deducción com la log probabilidad del modelo y aplican una búsqueda por montecarlo. Dicen que pueden coger las respeustas más prometedoras y luego agregarlas de alguna forma.
#interesante, es como el ToT al final, pero lo de la logprobabilidad tiene buena pinta. Lo que no sé es cómo se podría utilizar con los modelos razonadores, quizás en lugar de cada deducción, debería ser cada nodo varias deducciones? pero entonces tendría que ser un proceso de pesnamiento bastante largo para lo que supongo que iría mejor dividir manualmente el flujo...

- Planeadores externos:
  
##### LLM+P: Empowering Large Language Models with Optimal Planning Proficiency
![Pasted image 20250307102828.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250307102828.png)
Proponen primero definir el entorno en un formato PDDL. 
Le pasan al LLM la descripción del entorno y el problema, este tiene que definir la descripción del problema en formato PDDL.
Luego un solver PDDL crea el plan para resolver el problema en formato PDDL.
Finalmente el LLM traduce este plan a lenguaje natural.
Entiendo que funciona mucho mejor en entornos bien definidos  y con una estructura fija, en más abiertos no creo aque funcione. Supong que se podría definir un entorno para pensamientos, per no sé.
Al final el LLM es solo como el traductor, es como automatizar el proceso de crear el problema en formato PDDL.
#interesante, supongo que debe funcionar muy bien para ese tipo de tareas.
#####  Dynamic Planning with a LLM
Proponen extender el anterior para que el LLm en lugar de ser únicamente el traductor participe activamente en el plan generando observaciones.
![Pasted image 20250307111008.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250307111008.png)


##### BUILDING COOPERATIVE EMBODIED AGENTS MODULARLY WITH LARGE LANGUAGE MODELS
Dividen el módulo de memoria en semantic (knowledge del entorno), episodic (episodios pasados), procedural (cómo realizar acciones específicas) -> #todo, en varios otros papers también usan una separación similar. entiendo qeu el knowledge del entorno podría ser la docs del proyecto, pero lo interesante es que se podría separar la memoria en acciones pasadas y el módulo de largo plazo como tal, osea tener el módulo de largo plazo con la búsqueda RAG por ideas comprimidas, y luego se podría buscar para few shots ejemplos exitosos anteriores.
![Pasted image 20250307113541.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250307113541.png)

Perception module: pasarle el estado actual, ellos usan una CNN para pasarle info visual
communication module: podría ser el agente usando tools para obtener info relevante 
Planning module: planean con LLM a alto nivel (como en otros)
Execution module: transformar cada tarea de alto nivel a acciones primitivas (como en otros).

El execution module entiendo que es un LLM que le pasan la memoria en la que tiene acciones pasadas y utilidades del entorno para poder descomponer el plan de alto nivel a bajo nivel.
#todo -> muy interesante lo de dividir el planning en primero alto nivel para defiinir el goal y luego que un execution planner genere a bajo nivel con toda la info. Entiendo que se podría guardar en memoria las tools con su descripción semántica para poder proveerle al agente las diferentes tools y que decida. Habría que valorar en el ejemplo específico si merece la pena hacer esta separación de planner alto-bajo nivel o si es mejor pasarle directamente las tools al ReAct.

- Planning con feedback:
  -React que tiene en cuenta las observaciones pasadas para decidir qué hacer
##### Voyager
Interesante de planning es que en su flujo proponen 3 tipos de feedback: 
- Feedback del entorno: aunque no haya fallado el código de la skill, puede que el resultado sea inesperado. Utilizan un agente que da feedback al resultado obtenido de la acción ejecutada.
- Errores de ejecución: si da error la acción ejecutada entonces se tiene que generar feedback sobre lo que ha pasado.
- Self-verification: proponen promptear a otro agente para confirmar que la acción ejecutada se ha llevado acabo correctamente.
#interesante el acoplar en una ejecución dinámica el planning y la ejecución par obtener feedback y adaptar dinámicamente las acciones. Entiendo que es algo parecido a lo que se hace en ReAct, pero de forma más compuesta.

-En Ghost in the minecraft también acoplan al planner con el feedback, #todo, ver si esto peude ser alternativa más compleja a ReAct.
-En SayPlan el feedback lo sacan de un environment simulado con las restricciones y estados, para restringir las acciones que se pueden hacer.

##### LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models
Proponen de nuevo hacer un plan a alto nivel y luego uno a bajo nivel. Para el alto nivel usan few shots con RAG y logit biases (añadir un sesgo positivo a los logits de los tokens presentes en el enunciado para que sea más probable que salgan, creo que el api de openai deja hacer esto, entonces como en el prompt le ponen los posibles objetos y acciones funciona mejor)
Proponen que entre high y low level planning haya un replanning si el loop en el low level con su porpio feedback falla demasiado.
![Pasted image 20250307122329.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250307122329.png)
#todo: muy interesante, habría que definir un loop de feedback entre el low-level y el entorno respecto las acciones ejecutadas. Luego, tras fallar x veces se podría generar un resumen con los x fallos de qué está pasando, y pasar al high level planner para que razone y genere el plan de nuevo desde el paso actual.

##### Inner Monologue: Embodied Reasoning through Planning with Language Models
Definen dos tipos de feedback: 
- Success feedback -> si la acción ha funcionado o no
- Feedback específico de la escena -> pasivo (descripción del entorno), activo (el agente pide información del entorno al humano, este le da el feedback  #interesante, se podría incorporar en human-in-the-loop)
Esto lo internan en un bucle cerrado en el que el agente va ejecutando acciones y observando el resultado.
#todo -> incorporar este tipo de feedback en el low level planer.

- Feedback proporcionado por el propio modelo: 
##### SELF-REFINE: Iterative Refinement with Self-Feedback
![Pasted image 20250307125953.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250307125953.png)
Proponen parecido a reflexion, 3 LLMs, uno genera otro critica con feedabck y el otro refina la respuesta.
Podría estar bien incorporar algo de esto o Reflexion en alguno de los módulos, pero habría que tener cuidado con no solapar los modelos razonadores.

##### SELFCHECK: USING LLMS TO ZERO-SHOT CHECK THEIR OWN STEP-BY-STEP REASONING
Dicen que preguntarle al LLM directamente de que diga si está bien o no, aunque sea pasándole ejemplos, no funciona muy bien. Entonces proponen un método mult-step para verificar cada step en el plan:
- Extraer el target del step: le pasan la pregunta, los steps hasta ahí y le piden que diga la acción que se quiere tomar (reformulando la acción mencionada en el step)
- Extraer información relevante: se le pasa la pregunta, los steps y la info, y se le pide que extraiga la info relevante para este paso
- Se le pide a otro LLM sin ahber visto el step original, pasándole la pregunta, steps e info relevante que genere un step nuevo.
- Comparación de resultados: promptear para ver si un step es complementario o contradictorio al otro.
Luego si contradice le ponen multiplicador -1, si no está relacionado 0, y si lo complementa 0, así sacan un confidence score de qué tan buena es la solución:
![Pasted image 20250307144032.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250307144032.png)
No se mencoina, pero supongo que también se podría usar la log probabilidad multiplicada por estos.
#interesante, pero no sé hasta que punto es esto mejor que simplemente un self-consistency para cada nivel de step, osea al final se está haciendo un self consistency pero con varias llamadas que lo hace más caro. Quizás se podría incorporar a la hora de hacer el plan esta estrategia de forma paralela por varios, y aplicar la fórmula? #todo

##### ChatCoT: Tool-Augmented Chain-of-Thought Reasoning on Chat-based Large Language Models
Proponen que el feedback sea otro modelo, hacen un CoT reasoning pero en formato de chat entre 2 modelos.
No me ha convencido.

### Módulo de acción

Lo de que pueden llamar a acciones para ejecutar funciones predefinidas, hablar con otro LLM, hablar con el humano

- Acción mediante recolección de memoria:
##### Communicative Agents for Software Development
Hacen un ChatCoT pero a lo grande con muchos roles para resolver un problema de ingeniería del software.
Mencionan que como en ChatCoT, los LLMs no dejan de hablar entre ellos aunque hayan sacado el resultado -> Self-Reflection para basado en el contexto, cuál es la respuesta.
#interesante Supongo que podría crear algo así donde varios agentes con varios roles interactuan entre ellos para llegar a una conclusión final, se podría usar la estrategia de ChatCoT en la que el prompt inicial tiene formato de prompt.
##### METAGPT: META PROGRAMMING FOR MULTI-AGENT COLLABORATIVE FRAMEWORK
Este paper es god.
Dicen que los humanos han inventado standarized operating procedures (SOP) que funcionan muy bien -> lo del paper anterior.
Todos los agentes con estilo ReAct, con sus tools específicas.

Dicen que a diferencia de ChatDev (el anterior), ellos definen una interfaz de comunicación entre los agentes de forma estructurada, porque dicen que con lenguaje natural pasa lo del teléfono descacharrado.
En lugar de comunicarse directamente los agentes uno a uno, utilizan un pool de mensajes, para facilitar la coordinación. Para no haber information overload, implementan un sistema publisher-subscriber, en el que a cada agente solo se le notifica cuando hay un mensaje del tipo que a él le interesa. 
![Pasted image 20250308105425.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250308105425.png)
#todo, el sistema por roles es muy interesante y curioso. Entiendo que lo más efectivo y avanzado sería implementar un sistema de estos y luego dentro de cada agente estrategias de planificación / memoria / rag, de los agentes anteriores. Esto sería lo más efectivo, pero no sé si igual es demasiado difícil pal TFG.
Se podría implementar el pool para que los diferentes agentes investigadores de información vayan buscando info y sacando conclusiones de forma paralela cada uno en su fuente de información.
Habría que buscar un SOP para el caso del TFG.

- Acción mediante seguimiento de planes:

DEPS y GITM, lo de que primero se genera un plan a alto nivel, y luego se va descomponiendo y siguiendo a bajo nivel.

Ambas técnicas son muy interesantes (planes y memoria), lo más guapo supongo que sería combinar las dos, pero es fumadita.

- Acciones con tools externas:

-HuggingGPT: le da al modelo la tool de buscar en huggingface modelos y que este los descargue y utilice para resolver la tarea que quiera. Curioso pero pinta tremenda fumadita y no se hasta que punto es efectivo (tiene pinta que mejor poner tú los modelos uqe te interesan)
##### WebGPT: Browser-assisted question-answering with human feedback
Entrenan un agente para que busque en internet (api BING) (SFT, RL, rejection sampling, reward modeling??)
Dicen que en algunos casos esto puede ser más beneficioso que RAG -> más info y los motores de búsqueda ya tienen estrategias de similitud semántica.
Al agente se le pasan documentos (con el enlace a la web, el título...) y este puede tomar varias acciones como scrollear (más info de esa web), referenciarlo, buscar otra query, ir a un enlace mencionado...
Tiene muy buena pinta pero estás que hago algo así pal TFG. Quizás un agente de búsqueda más simple, o reutilizar este.
##### Graph-ToolFormer: To Empower LLMs with Graph Reasoning Ability via Prompt Augmented by ChatGPT
#interesante, tiene pinta de mucho potencial, la idea es copiar el código del framework y luego crear una funcionalidad avanzada para el dominio específico. Tiene muy buena pinta pero pinta fumadón, se podría intentar ver si funciona el código e ajustarlo para una tarea avanzada en específico. Entiendo que también se podría utilizar en lugar de usando los modelos ajustados para el agente con LLM enorme de caja negra.
En github está el código del framework, el código para ajustar los modelos, el dataset para ajustarlos y los propios modelos en Zip -> está todo basicamente.
Mencionan 3 tipos de prompts tunning: discrete tunning (ajustar todos los paráemtros del modelo con ese tipo de prompt), continuous tunning (ajustar solo unos pocos), primte tunning (few-shots)
Para llamar a las funcoinalidades del raoznamiento en grafo usan tools que les llaman cno los tokens especiales <\API>,  pueden hacer varias tool calls seqeunciales, paralelas o anidadas.

Proponen darle al agente varias tools: 
- Graph loading: dados unos documentos se cargan en forma de grafo, se crea una "base de datos" al vuelo para la consulta actual en la que el modelo puede interactuar.
- Graph property reasoning: con GR(grafo, toolx:propiedad_deseada) el agente puede obtener la info que quiere sobre el grafo que quiera. Las propiedades disponbles son: densidad, shortes path, eccentrity, diámetro, radio, centro, periferia
- advances graph reasoning tasks: proporcionan ejemplos de cómo usar su framework de forma avanzada, la idea es que se implementen utilidades como estas en un dominio específico. En el ejemplo de bibliographic paper, se utiliza una base de datos de grafos de papers pre-cargada, se llama a GL y en lugar de computar todo con el agente se carga de una. También se carga un GNN preentrenado con bert para utilizar esta funcoinalidad. Se añaden tasks específicas al agente de esta funcoinalidad avanzada, como podrían ser explícame x paper. Se crean plantillas de input para asjutar el modelo del agente para que utilice las tools avanzadas, entonces este solo las puede usar de esa forma.

Utilzan chatgpt para aumentar los datos de entrenamiento de llamadas a la api, proporcionan el prompt. Obtienen 5000 datos de entrenamiento que filtran para qeudarse con ~2800.
El proceso de entrenamiento es como en los demás de entrenar agentes. Se les pasa trazas de ejemplo donde se ejecutan las tools, para que el modelo aprenda dónde ejecutar las tools, cuáles ejecutar en cada momento y con qué argumentos ejecutarlas.
También se incluyen datos de entrenamiento QA sobfre las propiedades de los grafos para que el modelo aprenda a utilizarlos. Los datos orginales entiendo que eran enmascarando las llamadas que el modelo tiene que hacer con un token especial.
Cuando se incluye -> en la salida del modelo significa que la salida de la tool call debe incluirse en la salida del modelo, en lugar de ejecutarse solo en el backend.
![Pasted image 20250304142628.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250304142628.png)
Se usan varios "hubs" que son como bases de datos con información del sistema.
-está el graph data hub que son las bases de datos para las funcoinalidades avanzadas, en el caso de los papers usan el BERT GNN para acceder a los datos, aquí es donde el modelo con la directiva GL puede añadir los datos, tiene más sentido cuando no se utiliza una base de datos ya creada.
-en el graph task hub están las tareas hard-codeadas de qué hacer en cada una. Esta llama a las sub tareas del praph model hub, las que usan los modelos bert graph para las tareas específicas.
Entonces el graph task hub es como una interfaz donde se definen las tareas que luego van a llamar al graph model hub.
-El working memory tiene los resultados de las tareas que no incluyen la directiva -> r, son las tareas intermedias, se guardan ahí para acceder luego. La gracia es que guarda resultados de queries intensivas computacionalmente, usando la GNN, entonces si luego hay una tarea parecida que quiere lo mismo, se puede sacar de ahí. Tiene espacio limitado, actúa como FIFO para eliminar datos.
Explican cómo evaluar el sistema.
##### TPTU: Task Planning and Tool Usage of Large Language Model-based AI Agent's
Proponen dos tipos de agente, uno planeador y otro que tiene una set de tools para resolver un problema. Entonces proponen la estrategia de que uno haga el plan, y llame a los otros agentes (creo que el propio planer define el prompt de los otros agentes y las tools que estos tienen #interesante)

-TaskMatrix.AI -> proponen conectar al agente converacional a una bd de tools grande, y que el decida, supongo que chatgpt funciona así.

##### RKL Systems A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning
Proponen que un agente router lea el query, y decida a qué agentes llamar. Es como que las tools sean otros agentes, si no encuentran un agente specífico para lo que quieren llaman a un agente general.
#todo, esto sería muy interesante hacerlo, supongo que no es algo que hayan inventado en este paper. Los de MetaGPT supongo que hacían algo parecido (el router sería planner arquitecto), pero estos definen más la jerarquía de router - agente. 

##### OpenAGI: When LLM Meets Domain Experts
Lo mismo que el anterior, pero usan RL con PPO para mejorar el planner.

-VigerGPT -> preguntas sobre imágenes vídeos. Dicen que no confían en end-to-end impelementations en los modelos, entonces cogen un codex y le dan funciones linkeadas a modelos devisión por computador. El modelo codex se encarga de la lógica de la query.
-MM-React -> más o menos lo mismo, agente react con tools de visión por computador.

##### User Behavior Simulation with Large Language Model based Agents
![Pasted image 20250308173202.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250308173202.png)
3 tipos de memoria: 
- sensory memory -> observaciones el entorno resumidos con LLM (supongo que cada sentence se pasa a un LLM para que saque las observaciones). Se les pone un score de qué tan importantes son + score timestamp.
- short term memory -> si un agente se encuentra varias veces con memorias parecidas en short-memory, pasan a long-term memory. Se añade Mi a M, si se añade otro Mi con similiaridad de coseno pasando cierto umbral, entonces se dice que ese Mi enhancea al otro, se añade a su grupo. Luego cuando hay k de ese grupo, se pasan por un LLM para que se añadan a long term.
- long term memory -> se puede aplicar reflexión sobre estos.
Hablan de ponerle personalidades al perfil del agente. Igual si le digo de acutar de diferente forma a cada agente, hay resultados más variados.
Fórmula para calcular olvido, la exponencial en el beta hace que las memorias más recientes sean más propensas a ser olvidadas:
![Pasted image 20250309101146.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250309101146.png)
Al acceder a memoria se incluyen, top k de long term memory y todas de short-term memory.
La reflexión en la memoria de largo plazo es generar ideas abstractas, Usan misma estrategia que Generative agents para resumir la info.
Le pasan profile / memory / instruction / context (del entorno)
#todo, mirar este sistema de memoria

##### Do As I Can, Not As I Say: Grounding Language in Robotic Affordances
Multipican probabilidad de LLM (say) con prbabilidad de RL (can) de cada acción, la idea es que el RL te diga si ejecutas la acción si va a ser succesful o no. Esto no me sirve xd.

-RAH -> podría ser interesante el sistema de feedback, parecido a DEPS
-RoCo -> también hacen lo de incorporar el feedback al prompt del agente.

##### PREFER: Prompt Ensemble Learning via Feedback-Reflect Refine
![Pasted image 20250309113725.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250309113725.png)
Parten de un prompt base para resolver una tarea. Se le pasan al agente queries de entrenamiento, cuando el ejemplo es difícil y el agetne falla se pasa por un reflector con acceso al ground truth que genera feedback. Este feedback se utiliza por un refinador que retoca el prompt para mejorarlo en la tarea.
Al tener un conjunto de prompts, se ejecuta la tarea con varios agentes paralelos, los cuales cada uno generan una respuesta.
Una vez varias respuestas, se pide al LLM que evalue cada respuesta hacia delante (diciendole a ver qué tan buena es la respuesta) y hacia atrás (diciendo a ver qué tan mala es la respuesta -> pidiendole contra argumentos), entonces se resta una con la otra y se obtiene el score de la respuesta, se elige el mejor.
Es interesante pero no creo que me rente.

##### Improving Factuality and Reasoning in Language Models through Multiagent Debate
Proponen que diferentes agentes respondan a la misma pregunta y que luego comparen sus respuestas. Se le pasa en el prompt las respuestas de los demás agentes, y se les pide que valoren estas respuestas, y que refinen las suyas en consecuencia.
#interesante, se podría valorar meter algo así en lo del pool de varios agentes con roles.

##### MemPrompt: Memory-assisted Prompt Editing with User Feedback
Dicen que para el mismo modelo, dos queries similares deberían reproducir el mismo error en la comprensión.
Entonces proponen guardar el feedback a cada query y si se hace un query parecido añadir el feedback en el prompt del agente para que no cometa el mismo error.
#interesante, mirar si añadir una sección de feedback al few-shots del agente.

##### Mindstorms in Natural Language-Based Societies of Mind
Hacen también lo de que varios agentes discutan entre ellos para llegar a un acuerdo.ç
Dicen que en grupo siempre vas a tener mejores ideas que en solitario.
Se les va un poco la olla y dicen que tienen diferentes jerarquías sociales como monarquías o democracias. Parece que las monarquías van mejor xd.

##### Executable Code Actions Elicit Better LLM Agents
Proponen agente de código, las tools las ejecuta en código de python generado directamente. De locos en SWE benchmark.

Supongo que esto va muy bien si hay que hacer interaciones complejas con las tools -> sacar 5 veces info de bd, hacer un loop para una lista...
Para otras no se si renta tanto.
#todo, si hay alguna tarea de este tipo valorar usarlo. Proporcionan ellos el Llama7b ajustado, que se podría usar.

También lo ponen en el escenario de crear código python para resolver problemas, con otros benchmarks. Entonces el observation es la salida del intérprete de python, se autodebugea.











to tailor -> para adaptar
to boast -> presumir / alardear
intricate -> algo que tiene muchas pequeñas partes juntas que hacen algo complejo -> intricate problem
to bolster -> support / improve / make something stronger

