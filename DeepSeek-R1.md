Para entrenar el DeepSeek-R1-Zero usaron un RL sin supervised fine tunning (SFT), con el método Group Relative Policy Optimization.

## DeepSeek-R1-Zero
### Proximal Policy Optimization (PPO)

El DQN daba el problema de que era muy inestable -> hay que limitar lo que se aprende para evitar esta inestabilidad.

En el TPRO proponían con KL, funcionaba pero era muy costoso.

En PPO se utiliza el clip que limita lo que puede aprender:
![Pasted image 20250123104653.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250123104653.png)

Se maximiza el rendimiento de la política nueva πθ minimizando los posibles cambios. 

Dentro del clip, está la relación entre la política nueva multiplicado por la ventaja (qué tan bueno es esta acción respecto al valor esperado de la política actual). Entonces se elige el mínimo entre eso y el clip con epsilon por la ventaja.
![Pasted image 20250123105154.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250123105154.png)
![Pasted image 20250123105426.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250123105426.png)

Entonces de esta forma si A es mayor a 0 se aumenta un poco, pero si A es < 0 se penaliza bastante. De esta forma penalizamos mucho los errores pero estamos cautos pq q un episodio sea bueno no significa que todos vayan a ser así.
![Pasted image 20250123105511.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250123105511.png)

### Group Relative Policy Optimization

Es lo mismo que PPO pero en grupos en lugar de con ejemplos individuales, y aplica una regularización adicional con la divergencia KL: 

![Pasted image 20250123105832.png](https://github.com/MartinLopezDeIpina/TFG_apuntes/blob/master/Imagenes/Pasted%20image%2020250123105832.png)

De esta forma, se penaliza que la política cambie bruscamente.

### Entrenamiento

Para conseguir el reward (se usa pa calcular el Advantage), se usa un modelo que depende del tipo de tarea. 
En casos de matemáticas pues el resultado correcto, en caso de código se compila y se comprueba el resultado.

Dicen que obligan al modelo a formatear sus respuestas, con formato xml metiendo los mensajes de pensamiento en \<think>\</think> y answer pa hacer un chain of thought. No usan estrategias de prompting, solo ese template para ver la efectividad del RL.

Claro entonces cuanto más largo le dejen el output mejor será el rendimiento en inferencia, ya que tiene más pasos de pensamiento. Dicen que el modelo desarrolla la reflection el solito, que en pasos de pensamiento vuelve a pasos anteriores a calificar sus resultados.

## DeepSeek-R1

El zero era un poco inestable -> el CoT a veces tenía pasos en otros idiomas o pasos ilegibles. 
Entonces en el R1 combinarios SFT con RL. Usaban el siguiente flujo: 

- Cold start: Un SFT con datos en formato CoT, donde con tokens especiales separaban el proceso de pensamiento, y añadían un resumen al final: |special_token|<reasoning_process>|special_token|\<summary>,
- Reasoning-oriented Reinforcement Learning: lo mismo que en el zero, pero añadieron un componente de consistencia del lenguaje en el reward pa q no cambiase el lenguaje -> eso lo hace un poco menos preciso pero responde en un idioma sabes. Paran cuando convergen las reasoning tasks.
- Rejection Sampling and Supervised Fine-Tuning: Cogen más data para un SFT, pero en lugar de ser solo para reasoning es para otras tareas también. El data lo sacan filtrando respuestas del checkpoint de ese R1. También ajustan el DeepSeek-V3 con nueva data, porque se supone que actúa de evaluador en algunas tareas de razonamiento.
- Reinforcement Learning for all Scenarios: se ajusta de nuevo con RL con los datos nuevos. Se añaden componentes de helpfulness y harmlessness al reward.

Luego destilan solo con SFT otros modelos como el LLama con los datos sacados del R1, y se convierten en las cabras. Dicen que aplicar el mismo proceso de RL + SFT en un modelo más pequeño da peores resultados que destilarlo con SFT solo con los ejemplos del R1 grande.

Dicen que usar greedy decoding les da repetición y variabilidad, aplican temperatura y top-p.

Dicen que usar estrategias de prompting con estos modelos (few-shot, think step-by-step) degrada su rendimiento. Hay que preguntarle directamente.

