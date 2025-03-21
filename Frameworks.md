![[Pasted image 20250228205357.png]]

## Modelos local

- Huggingface
- vllm
- Ollama

## Indexación de datos

- Huggingface -> modelos embedders VS embedder API -> openAI embedder
- Pgvector
- Chroma / Milvus / Pinecone
- LlamaIndex

##### PostgreSQL con PgVector
Integración fácil -> con Flask ORM
Más flexibilidad para consultas con metadatos (SQL) -> las demás pueden filtrar con where como en SQL, pero mucho menos flexible para las operaciones (actualizar, buscar...)
Contras: al ser SQL los algoritmos de búsqueda no están tan optimizados, es más lento. Para escalarlo a una base de datos grande (como la de stackoverflow mejor las otras)
##### Pinecone 
Orientado a servicio, parece que se puede con docker, pero mejor que no
##### Chroma
Parece que es sencilla de usar pero no es tan potente como Milvus
##### Milvus
Parece difícil de usar pero potente, bd grande usar esto.
##### Qdrant
no tan potente como milvus pero parece flexible con los metadatos

### LlamaIndex

El llama parser para procesar los documentos -> funciona muy bien para PDFs.
Puede parsear usando lenguaje natural. No me convence, te cobran por hacer cosas que puedes hacer con NLTK en local (dividir por oraciones)

También tiene una abstracción sobre huggingface transformers para ajustar modelos embedders, menos flexible pero más rápido.

Está bien para tareas fáciles, dicen que al integrar con openai con 10 líneas lo indexas todo. Pero si quieres embedders / otras cosas personalizadas dicen que da problemas y que al final es más fácil implementar directamente.

No me convence, mejor embedder transformers / openai -> dataset / pgvector directo.
Tiene algunas funcionalidades como evaluar importancia de docs, puede que sean útiles, decidir en el momento.

### Agentes

##### Modelos prefabricados
LlamaIndex, LangChain, Huggingface Smallagents tienen agentes como ReAct prefabricados para usar tools directamente. La chicha está en personalizarlos con el prompt específico del caso.

- LangGraph + LangChain
- LLamaIndex Workflows
- AutoGPT
- Autogen: estructura orientada a chat, intuitivo parece bastante limitado a entornos orientados a chat.
- CrewAI: orientado a agentes con roles específico de forma intuitiva
- SwarmAI

- OpenHands

### LangGraph
Modo grafo, los pasos del agente son fluir por diferentes nodos.

+control total de todo
-difícil -> más lento desarrollar, para casos simples puede ser sobreingeniería, sólo para casos de investigación, casos nicho.

### LlamaIndex Workflows
![[Pasted image 20250310110055.png]]
workflows es forma de crear agentes definiendo los pasos.
![[Pasted image 20250310110436.png]]
Bastante parecido a langgraph, hay un estado, se pueden definir condicionales dentro de los steps. Es como un punto medio.
### CrewAI
Tienen interfaz que elimina boilerplate, por ejemplo clase Agent, Task, pensado para interacción entre diferentes agentes (Crew xd) 
Fácil de hacer, pero deja menos personalización. También se pueden hacer agentes personalizados, pero entonces no tiene sentido usar la librería, más complicado de personalizar. ![[Pasted image 20250310111634.png]]

+Fácil de usar, eliminar boilerplate
-Difícil de personalizar

### AutoGen
Creado por Microsoft :( -> buena docs, muchos tutoriales.
Parece más difícil, más personalización que CrewAI.

Da más funcionalidades que LangGraph, code executors, blah, blah. En langgraph eso hay que crearlo.

![[Pasted image 20250310114947.png]]

### Smolagents
Orientado a tareas sencillas, se queda corto al oquestrar muchos agentes.

+sencillo de usar
+fácil integrar con modelos de huggingface en local

-Se queda corto para tareas complejas
![[Pasted image 20250310121124.png]]

### SwarmAI
Nuevo, lilbrería "lightweight", todavía está en fase de desarrollo, parece orientado a educación.

-No establecido
-Orientado a ejemplos educacionales

### Conclusión
Agentes LLM bastante nuevos, salen frameworks de debajo de las piedras, en general todos la misma estructura agente / tool
Pa mi que no merece la pena todavía cambiar el framework de la empresa si el año que viene van a salir 5 nuevos o van a cambiar todo.
![[Pasted image 20250310112250.png]]
Usar LangGraph pal TFG

Espectro boilerplate / personalización

LangGraph -> AutoGen ->  LlamaIndex Workflows -> Smolagents -> OpenHands -> CrewAI 

+Personalizar todo
+Familiarizado

## Trace
- LangSmith
- Phoenix
- LangFuse


##### OPENHANDS: AN OPEN PLATFORM FOR AI SOFTWARE DEVELOPERS AS GENERALIST AGENTS
Menor comunidad, docs, tutoriales, un paper que sacaron. Útil para crear un agente fácil y probarlo en varios benchmarks directamente.

Una herramienta que permite ejecutar agentes con una itnerfaz visual, proporciona una interfaz para realizar comunicaciones entre agentes, herramientas (AgentSkills) prefrabricadas, e integración a benchmarks.

Benchmark SWE, proporciona un environment para ejecutar código y evaluarlos. 

Definen una interfaz de agente (step, reset, llm...) y hay un agentHub. Entonces tu subes tu agente y puedes interactuar con él con una interfaz gráfica. 

Para evaluar cada benchmark es un dataset que tiene un input query que se mete en el placeholder del agente. Proporcionan integración a los agentes.

Cómo se usan multples agentes?? -> #todo