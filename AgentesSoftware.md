
-ChatDev -> end-to-end con varios agentes colaborativos
-MetaGPT -> varios roles para supervisar código
##### Reddit
Dicen de primero darle un párrafo de "onboarding al agente" para el proyecto, basicamente decirle qué se usa, para qué y donde están las cosas.

Luego dice que hace una fase de interview en el que le pregunta al humano dudas -> esto lo podría preguntárselo a otro que tenga tool de búsqueda??

Luego que use su knowledge para ir navegando por el file system y que cree su propio resumen.

También dicen que se le podría dar acceso al log de commits?
##### Self-collaboration Code Generation via ChatGPT
Dicen que al darle un perfil al agente este actúa como un experto en el dominio. Supongo que ayuda a la hora de generar una solución más variada, pero habría que ver si merece la pena porque se pierde atención en esto. Después de varias pruebas dicen que analyst - cdoer - tester es el mejor, con compiler mejora insignificativemnte. #interesante, igual solo renta cuando se ejecutan varios en paralelo, entonce las respuestas son más variadas.  

Se comunican mediatne un blackboard, que sería equivalente al pool del otro paper. Leen las salidas del estado anterior y generan nuevas salidas #interesante, habría que definir cómo hacer la comunicación, en plan a quién le llegan los mensajes generados. 

### CODEAGENT: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges

Hacen como los otros un SOP con info retrieval - code generation - testing
- duck duck go para buscar info
- para buscar info hacen un summarize con LLM si es demasiado contexto
- Para buscar en el repo usan Tree-sitter.   

Primero buscan en la web información relevante sobre el problema a implementar, luego leen documentación y luego leen clases y funciones relevantes. Luego van navegando por el código sobre funciones relevantes para implementar.
#todo: el ciclo **web -> docs -> código -> código específico**  estaría muy bien.

### RepoAgent: An LLM-Powered Open-Source Framework for Repository-level Code Documentation Generation

Genera docs a nivel de fichero para un repositorio de python. Tiene en cuenta las dependencias entre funciones. 
Primero sacan el árbol del proyecto con AST abstract syntax tree analysis. Luego sacan con Jedi library las dependencias con las referencias. Luego cogen un prompt template en el que le van pasando para cada fichero el árbol y las dependencias.

```bash
repoagent run --model gpt-4o-mini --target-repo-path /home/martin/Jira_prueba --markdown-docs-path /home/martin/docs
```


