### Evaluar tool calls agentes

-Gorilla -> evaluar tools / args llamados en forma de subárboles
-Api-bank -> 

### Evaluar respuestas agentes / sistema entero

- Evaluar con LLM-as-a-judge con prefereiblemente ground truth
- Usar métricas BLAU, ROUGE-L
- Usar similitud semántica con BERTscore??
- Tiempo / dinero de ejecución del sistema / agente


##### Gorilla: Large Language Model Connected with Massive APIs
Entrenan un Llama 7b para que dada una query decida qué api de las disponibles llamar y genere la respuesta. 
Lo entrenan utilizando RAT (pasándole los documentos obtenidos de las docs de las apis disponibles desde el RAG), el modelo decide si los docs son útiles o no. Dicen que la info de las apis está también al final en en los pesos del modelo. Dicen de utilizarlo en retriever o no retriever mode. En los documentos contieenn las constraints de cada api que es muy importante, además estos están actualizados.

Para evaluar representan las tools y argumentos como árboles. Entonces generan un árbol de la predicción del modelo, y compreuban si la predicción es subarbol del ground truth con todas las posibles apis y argumentos. Creo que también hay argumentos opcionales que no se tienen en cuenta en el check. #todo, valorar esta estrategia de evaluación si ajusto un modelo para llamar a las funciones.

##### API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs
Dicen que cuando a un LLM se le pasan unas pocas tools se le pueden pasar todas en el prompt, pero que cuando hay unas cuantas es mejor implementar un sistema de retrieval para las tools maś interesantes para la tarea.
![[Pasted image 20250308125221.png]]
Proponen crear un sistema de agentes para generar datos sobre api calls.
Manualmente:
Le dicen a agentes anotadores pasándole APIs random que generen una query que pueda ser resuelta por esa api, la llaman y valoran la respuesta para anotarlo como dato. Para casos de plan + retrieval + call, les pasan las apis y les dicen que generen una query compleja, luego que la dividan en subqueries y cada una la resuelvan con una api. 
Con agentes más o menos usan el mismo sistema.
#interesante, pero fumadita, no creo que me pueda hacerlo pal TFG.

##### TOOLLLM: FACILITATING LARGE LANGUAGE MODELS TO MASTER 16000+ REAL-WORLD APIS
Crean ToolBench (dataset de instrucciones con llamadas), y entrenan Llama para obtener ToolLlama. Dicen que generaliza a APIs no vistas en el entrenamiento.
El dataset lo generan con chatgpt, cogen las apis, generan isntrucciones y generan soluciones anotando los paths.
Proponen dos métricas de evaluación, ambos con llm-as-a-judge:
- Pass rate: proporción de instrucciones que el agente completa con éxito.
- Win rate: le pasan métricas de evaluación a chatgpt y que decida cuál es mejor. No sé contra quien se mide xd, podría ser contra una solución anotada?
Utilizan anotaciones humanas para evaluar la fiabilidad del evaluador automático.

##### RestGPT: Connecting Large Language Models with Real-World RESTful APIs
Para evaluar el tool calling, en lugar de mirar si predicción es parte del gold, miran si el gold es parte de predicción.
También proponen métrica solution_len, la cantidad de llamadas adicionales respecto al gold standard.
![[Pasted image 20250308134215.png]]

-OpenAGI: ClipScore y VitScore para evaluar comprensión de imágenes