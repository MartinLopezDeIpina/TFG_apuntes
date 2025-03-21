- CursorAI
### Aider
Utiliza treesitter para traducir el sistema de ficheros, parece que es mejor que devin en SWE bench.
https://aider.chat/docs/repomap.html

### SWE-bench
https://www.swebench.com/#test

### Haystack
Para añadir documentos y pasárselos automáticamente
https://haystack.deepset.ai/

### LAMB
Entiendo que mi propuesta sería más enfocada a proyectos software + proyectos de la empresa? -> habría que incorporar hard-coded la guía de código de la empresa.

#### OpenHands + codeAct
Open hands es 

### Conversational Bot for Newcomers Onboarding to Open Source Projects
Proponen un chatbot que ayude a gente nueva a buscar / integrarse a proyectos software opensource.

### SourceGraph
Ofrecen una aplicación deployeable en varios tipos (full cloud / kubernetes / docker compose...) El cual le das el repo con el código y te lo indexan en una base de datos que han configurado.
Desde esta base de datos se puden utilizar varias funcionalidades: 
- Búsquedas / navegación avanzada
- Integración de agentes LLM -> Cody. Te responde todo lo que quieras y te referencia los ficheros utilizados. También puede generar código / autocompletar código / buscar bugs.
	Permite enlazar documentos externos (como docs), pero pagando.
	
Lo de explicar funciona bastante bien.
-	Utilizan indexación por trigramas -> separar query por trigramas: Class Persona -> "Cla", "las", "ass", "Per", "ers", "rso", "son", "ona"
	Y buscan los chunks que más apariciones de esos trigramas tengan, por expresión regulares. #interesante, no usan RAG sino eso, igual podría valorarse combinarlo.
	https://github.com/sourcegraph/zoekt, los de SourceBot también usan Zoekt y parece la alternativa openSource
	También tiene en postgre: pg_trgm -> tiene dos indexaciones: 
	- GiN: hace un índice invertido, para cada trigrama pone en qué chunks aparece -> se pueden retrievear todos los chunks en los que aparece el trigrama
	- GiST: Hacen una especie de vector one hot con los trigramas que tiene cada chunk, y se indexan en forma de árbol de alguna forma. -> permite sacar k-nearest neightbours
	Los de Zoekt usan su propio algoritmo de búsqueda, se supone que está optimizado para código fuente.
	Búsqueda estructurada -> para buscar siguiendo las normas del código, pro ejemplo dentro del print(), da igual si está en 3 líneas la paréntesis, sabe si está balanceado y si está dentro dle print, Usan Comby, parece que no está implementado directamente para hacer búsqeudas indexadas.
- También utilizan búsqueda con formato LSIF. Los editores de código para realizar tareas de búsqueda / corrección de sintaxis usan protocolo LSP. Se basa en que un engine analiza el código y devuelve un JSON con el formato del código estandarizado, este json es un LSIF. 
![[Pasted image 20250317205001.png]]
Luego están todos migrando a SCIP, ques es como LSIF pero usa un lenguage de marcado llamado protobuf que se supone que lo hace mucho más ligero y eficiente que el JSON.
SCIP-cli, para dado un scip hacer varias búsquedas: https://github.com/sourcegraph/scip?tab=readme-ov-file
SCIP-python, para sacar el fichero scip desde un proyecto: https://github.com/sourcegraph/scip-python

```bash
# crea un index.scip
scip-python index . --project-name=agente_jira_mcp

scip print --json index.scip > index.json
```

Muy interesante la API de SourceGraph, deja hacer consultas con GraphQl



Al Cody le dan primero: 
- Contexto sobre el proyecto
- Documentos relevantes para la consulta del usuario
- Tools de búsqueda

### SourceBot
Como SourceGraph pero open source, no tienen funcionalidad de agentes LLM.

### Github Copilot Chat
Sólo coge contexto de las ventanas abiertas

### Github Next
Tienen varios proyectos de investigación, en Copilot Workspace pare que es como un Devin, está bastante enfocado en resolver issues en lugar de explicaciones. 



- Github copilot chat
- SourceGraph