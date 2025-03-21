Lo más recomendable para impelementar el uso de tools desde scratch es pasarle en el system prompt la descripción de las tools con los argumentos que tienen, y luego en el chat template añadir los esquemas de json que tiene que seguir (comentan de editar los esquemas si se cree necesario -> como en lo de la demo de stocks). 

Los documentos sacados de RAG también se recomiendan que vayan en el chat template -> mencionarlos en el system prompt y luego añadirlos en el template.

Tipos de agentes: 
- Json agent: su output es el tool en json. El subtipo que le llaman function-calling agent es un agente ajustado para responder con esa estructura.
- Code Agent: En lugar de generar texto en formato json devuelven código de python que llama directamente a las funciones definidas. Entonces puede generar lógica más compleja con condicionales y bucles.

En la sección del dummy agent hay un prompt de react interesante. Los tool calls las pone dentro de comillas, supongo que con el de deepseek irá mejor con el boxed. Los thought / observation las pone con un salto de línea solo, supongo que como en el deepseek usa el \<think> entonces van mejor en formato xml.