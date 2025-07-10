export async function getAIRecommendations(query) {
  const response = await fetch('/public/ai/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!response.ok) {
    throw new Error('Error al obtener recomendaciones');
  }
  return await response.json();
} 