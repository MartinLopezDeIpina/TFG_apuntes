Se puede pasar contenido multimodal a modelos multimodales. En langchain también.

Top k -> coger los k palabras más probables
Top P -> coger palabras más pequeñas hasta que sumen P de probabilidad
Temperatura -> si < 0 hace probabilidades más pronunciadas, 1 es normal y mayor a uno aumenta probabilidades de palabras raras. Era un parámetro en una fórmula en lo de transformers.
Si pones top k a uno y t a 0 entonces el modelo debería devolver siempre lo mismo.

Casos de uso: 
- Describir tickets de compra con sus imágenes
- Hacer un resumen de un vídeo
- Encontrar una aguja en un pajar -> buscar una info exacta en 45 mins de vídeo

