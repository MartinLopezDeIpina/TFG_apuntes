# Mastering AI agents

Diferencian los diferentes tipos de agentes en función de su propóstio (además de ReAct, acceso a memoria conversacional): 

- Agentes con tools: se apoyan en estas para obtener información
- Agentes Environment controllers: utilizan sus tools para interactuar con el entorno, no solo para obtener info.
- Agentes self-learners: tienen la capacidad de evolucionar en sus iteraciones -> por ejemplo el voyager.

## Fremeworks

- LangGraph: dicen que puede parecer el más complejo por su estructura de grafos para los flujos.
- Autogen: estructura orientada a chat, intuitivo parece bastante limitado a entornos orientados a chat.
- CrewAI: orientado a agentes con roles específico de forma intuitiva

Hace una comparación muy detallada de las funcionalidades de los 3 (igual tendría que añadir esto a la memoria) -> yo diría que langgraph es el que más personalización permite.

## Memoria

Además de guardar los mensajes en short-term, mencionan otros mecanismos: 
- Long-term memory: guardar solo los learnings de interacciones pasadas.
- Entity memory: guardar detalles sobre entidades específicas
- Memoria contextual: de alguna forma combinar log-term, short-term y entity.

Se supone que LangChain ya tiene una impelementación de estas memorias incluida. 

## Evaluación de agentes

Utilizan GalileoCallbacks para guardar el stacktrace de los agentes y luego utilizan un LLM que evalua esta traza (está prebuilt, no se mencionan las métricas que utiliza)

Métricas: 
- Success rate -> depende el contexto específico habría que definir las métricas propias
- Task completion rate -> bien o mal
- Steps per task

- Evaluación de la calidad del output

- Evaluación del tool interaction (tool selection / argument selection / tool success rate)

## Errores típicos
- Objetivos / restricciones / outputs deben definirse de forma clara.
- Complejidad del planning, es necesario mucha capacidad de razonamiento. Recomiendan que primero un agente divida la tarea en diferentes subtareas, y luego estas tengan cada uno un plan. Recomiendan reflection para esta tarea.


# AI Agents in Action

Hace una introducción de muchas utilidades que existen para crear agentes, podría mencionarlas en la intro de frameworks de la memoria: AutoGen, Semantic Kernel

Varios tipos de control de systemas IA; árboles de decisión, blackboard system... parece que el flujo de LangGraph es lo más flexible.

Es posible separar los documentos en chunks para hacer rag sobre los chunks, hay utilidades para separar los documentos de forma lógica.

Semantic memory augmentation -> si el chat es todo largo convierte el input en preguntas usando otro agente y lo busca con rag en la base de datos de embeddings. Hay un paper hablando de esto que tiene buena pinta: Augmenting Language Models with
Long-Term Memory

Memory / knowledge compression -> cuando hay demasiada información mucha info puede ser repetitiva y redundante, entonces Nexus ha impelementado una forma de compresión en la que los documentos se clusterizan y luego se utiliza una función de compresión (un LLM) para reducir la cantidad de documentos.

Se menciona que el prompt tenga ls siguiente estructura (esto ponerlo con el chat template supongo): 
- Persona -> qué tiene que hacer y las reglas uqe tiene que seguir
- Tools
- Memory && knowledge
- agent reasoning + feedback -> cómo el agente tiene que actuar, creo que con los modelos razonadores esto era lo que se comentaba que no era necesario y usarlo empeoraba el rendimiento.

Usa un modelo o1 como agente y recibe una respuesta incorrecta. Le pide a otro agente que genere feedback (pasándole al respuesta correcta), y usa ese feedback para añadirlo al prompt -> quizás se podría hacer algo así pero con un rag, parecido a lo del voyager.

# Curso evaluate agents

Le añade programáticamente quitar boilerplate del final, quizás se podría hacer eso para corregir cuando el LLM no añade las llaves del formato JSON bien, en el paso de validar con pydantic.
Para tracear se puede definir en LangGraph lo que se detecta y lo que no.

### Métricas
- Basadas en código: expresiones regulares / Parsear JSON / contiene palabras clave -> Se podría añadir en el validador de Pydantic en el ciclo de retry, que cuente las veces que ha fallado para añadirlo como métrica. 
- El código generado es ejecutable / está bien??
- Resultado esperado: Match directo / similaridad de coseno, BertScore, fog-metrica??
- LLM-as-a-Judge: Meterle un prompt de si este resultado es correcto -> supongo que se puede hacer teniendo la respuesta correcta y comparando o directamente, mencionan de preguntarle a un LLM si los documentos obtenidos por RAG son relevantes o irrelevantes. Mencionan de SIEMPRE usar valores discretos y no contínuos porque los LLM no tienen el sense de cuanto es 80 / 100.
- Human label: Se podrían etiquetar algunos datos como ground truth y luego utilizarlos para evaluar los agentes.

### Evaluar routers
- Han utilizado la tool correcta?
- Han llamado a los argumentos correctos?  
- Rutas correctas?


![[Pasted image 20250221172110.png]]
Crear varias querys similares y definir optimal path -> evaluar el porcentaje de veces que entra en ese rango.

### Evaluate development

Basicamente tener un dataset con ejemplos y el resultado obtenido.

Dicen de mejorar el LLM-as-a-judge comparandolo con la evaluation por ground truth -> ejecutas cada uno por su lado y vas probando mejoras para que se parezca lo máximo posible al ground truth evaluation.

### Monitoring agents

Dicen que por el cambio en el códgio de los proyectos se puede degradar el rendimiento de los agentes -> seguir evaluándolos en producción, también se pueden integrar en CI / CD