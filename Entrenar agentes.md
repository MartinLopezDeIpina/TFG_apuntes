
### LORA: LOW-RANK ADAPTATION OF LARGE LAN-GUAGE MODELS
Requiere menos memoria de GPU porque no se calculan los gradientes de todos los pesos, solo los de los que queremos entrenar.
Dicen que con lora pueden cambiar de tarea muy facilmente porque cambian los parámetros para cambiar de modelo eficientemente.
Entonces siendo W dxk la matriz de pesos congelada, se le suma en inferencia los B dxr X A rxk -> si W es (0.3, 1) y BA da (0.2, 2) entonces se usaría W con el valor (0.5, 3).
La tasa de aprendizaje se define como alpha / r -> entonces al modificar el tamaño de r no es necesario buscar una nueva tasa de aprendizaje, se supone que sigue consistente.
Dicen que aplican esto en transformers a Wk, Wq, Wv y Wo (siendo Wo la de una transformación lineal tras un módulo de atención)

### FireAct: Toward Language Agent Fine-tuning

Parecido a agenttuning, ajustan modelos con trace cot + tools (react) generados por gpt4, desde una base de datos QA y algunos más.

Dicen que el coste de inferencia se reduce cuando los tuneas, ya que por ejemplo en el 3.5 como no incluían few-shots el coste se reducía como un 70%.

Entrenar full model mejores resultados que LORA pero mucho más caro. 15% mejor.

Diferentos métodos: 
- Solo react: Han hecho pruebas con datasets de size (n ∈ {100, 200, 500, 1000}), dicen que el 3.5 GPT aprende con 200, pero que el Llama necesita las 1000.
- React + Reflexion: añaden 500 de react + 500 con algunos en los que cuando el react era muy largo añadían ejemplos de reflexion
La mejor combinación depende del modelo base.

Recomiendan usar LLMs off the shelf para tareas exploratorias y LLMs ajustados para explotación, dicen que el 3.5 lo han ajustado con 10$.

Claro dicen que esto lo han hecho para un tool y un único agente, que no saben para orquestaciones de varios agentes.

### AGENTTUNING: ENABLING GENERALIZED AGENT ABILITIES FOR LLMS

Ajustan modelo LllamaChat2 70b para tareas de agente ReAct held in (tareas presenten en los datos de entrenamiento) y taras held out (tareas no presentes). 

Creo que el gold standard lo generan mediante gpt4 filtrando los resultados.

En held-in el LLama tuneado en algunas tareas le gana a gpt4 (en media no por un poco), en held-out si que gpt4 es superior, y en tareas generales se lo come.

No leído entero, pero muestra potencial de ajuste fino en lugar de usar api.

implementación interesante de react en langchain: 
https://github.com/THUDM/AgentTuning/blob/main/eval_heldout/hotpotQA/src/agent_arch.py

### Agent-FLAN: Designing Data and Methods of Effective Agent Tuning for Large Language Models

- Cuando se usa estructura ReAct se le saca al modelo de su tarea original, entonces al tunearlo dicen que avanza diferente su capacidad de razonamineto y adaptarse al formato, como que se sobreajusta al formato sin aprender nada más.
- Separan en instruction following (formato), reasoning (thought quality), retrieval (select correct function), understanding (parameters inputs pa funciones) -> instruction más fácil, reasoning lo complicado.
 - Suelen halucinar en forma de overfiting muchas veces. 

Entonces propuesieron las siguientes soluciones: 
- En el training data la mayooría de los ejemplos ponerlos en formato de chat y solo unos pocos en formato json -> el modelo aprende a cambiar formato sin problemas y se centra en razonar bien, como lo habían entrenado originalmente.
- Descomponen los datos en las habilidades anteriores, y priorizan las más difíciles para ahorrar entrenamiento, pq reducir las de formato no afecta en nada.
- Unas métrica para las halucinaciones, una para el formato y otro para las acciones (en posibilidades de tool / no tool). Usan keywords para saber si está sobreajustando que necesita usar tools. El score es una combinación de ambas métricas. Se le añaden al corpus ejemplos donde el usuario pide uso de tools y no hay disponibles, para enseñar al modelo a no inverntarse tools. También cuando se proveen tools y el usuario requiere una conversación sin tools.

Parece ser que llega un punto en el que añadir más datos no renta tanto, importa más calidad -> los modelos base no entienden de tareas de agentes al principio.

En el dataset público en la partición del agentflan se puede ver la separación de tareas que comentaban. Se le preguntan en formato de chat en lugar de formato react.  Se supone que se incluyen también ejemplos de respuesta en formato json para que luego sepa hacer eso.

### AGENTGYM: Evolving Large Language Model-based Agents across Diverse Environments

Han creado un "framework" para crear agentes con su estrategia. Tienen 14 environments y datos como ejemplos.

Usan RL pero en lugar de token a token hacen que la solución esté bien o mal, encapsulan los pasos intermedios. Se supone que es porque da igual el token que ha hecho justo que vaya bien, lo que importa es que vaya bien.

Entonces lo primero que hacen es entrenar un modelo base que aprenda a seguir instrucciones en forma de agente react. Para esto usan el crossEntropy para que sepa seguir instrucciones, pero no sabe seguir las que no ha visto.
Luego utilizan un off-policy method (basado en inferencia, habría que mirarlo), crean ejemplos dejando al agente interactuar con el entorno y llegando a ejemplos hasta el final, y luego actualizan los pesos de forma ponderada.

Claro en los demás papers el modelo se adaptaba para esos casos con esos tools, parámetros, etc. Con el RL puedes cambiar las tools y no necesitarías sacar las traces nuevas, con que tengas las respuestas vale y que el agente interactue con el entorno para saber la política óptima.

#### RETROFORMER: RETROSPECTIVE LARGE LANGUAGE AGENTS WITH POLICY GRADIENT OPTIMIZATION
Añaden un módulo de reflexión y le ponen el feedback al prompt del siguiente. Utilizan RL para entrenar el reflector.
Usan memoria corto plazo (instrucción actual) y largo plazo (reflexión-respuestas) anteriores. 
Está bien lo de pasarle el feeedback de anteriores, pero los feedbacks de los otros papers tenían mejor pinta.

### Ideas proyecto

Dataset con bugs de repos python, con id commit que crearon y commit que resolvió (no tienen descripción del erro): https://github.com/soarsmu/BugsInPy

Mirarlos un poco por encima, los anteriores pa mi que tenían más chicha:
-CoH
-RET-LLM
-WebShop
-EduChat

MIND2WEB y SQL-PaLM dicen que los agentes adquieren capacidades muy avanzadas en el dominio específico en el que se ajustan, no pinta que rente leerlos pal TFG.

-Can Language Models Teach Weaker Agents? Teacher
Explanations Improve Students via Personalizatio -> podría mirarlo