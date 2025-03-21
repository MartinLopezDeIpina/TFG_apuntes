
![[Pasted image 20241022124039.png]]
 En el function calling, se le manda al LLM un prompt y unas utilidades (funciones). Entonces, si el LLM decide que tiene que llamar a una función, su output contiene el nombre de la función y los argumentos, y luego se le pasa de nuevo al modelo (eso lo gestiona el programador) -> lo del ReAct agent.

Lo del soporte para funciones es que los proveedores como OpenAI añaden la absracción de function calling, osea que tu le pones al modelo las funciones y este ya te da la salida de forma estructurada. También ha sido finetuneado para que entienda eso de puta madre. Se supone que se puede hacer manualmente con pydantic y LangChain.

Tiene pinta que en el ReAct es mejor implementación separar el thought de la tool para que el tool decida cual elegir después de generar el thought.

Los modelos especificamente tuneados para hacer fine-tunning, por ejemplo Raven 13B, son más eficientes y les ganan en algunas tareas de elegir la función a modelos más grandes.

Parallel function calls -> basicamente que te devuelva varias functions que se ejecuten de forma paralela.
Multiple function calls -> que tenga que elegir entre varias.
Nested function calls -> que el LLM directamente ejecute unas funciones con la salida de otras funciones, sin tener que llmarlo dos veces, ahorrando tokens.

# LLMCompiler

Un grafo para planificar las function calls de forma paralela y con sentido, pa agilizar el proceso de inferencia.
En el paper evaluan el rendimiento de su implementación, no se si la impelementación de LangGraph será tan buena.

# Ensembled Reasoning

Entonces el modelo pone tokens especiales del tool que quiere usar y estos se detectan y se hace el function call, mientras el modelo sigue generando. Luego, cuando se ha temrinado el function call se injectan en la generación en tiempo real.

Hay una implementación de un jambo, pero no se si existen modelos ajustados que integren esto de forma nativa.
https://medium.vital.ai/agents-and-ensemble-reasoning-e0036c68d569

