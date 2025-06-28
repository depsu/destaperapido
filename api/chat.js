export default async function handler(request, response) {
  // Solo permitir peticiones POST
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    const userPayload = request.body;
    const GEMINI_API_KEY = process.env.GEMINI_API_KEY; // Carga la clave segura desde Vercel

    if (!GEMINI_API_KEY) {
      throw new Error("API key not configured");
    }

    const apiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userPayload)
    });

    if (!apiResponse.ok) {
        const errorBody = await apiResponse.text();
        console.error("Google API Error:", errorBody);
        throw new Error(`Google API responded with status ${apiResponse.status}`);
    }

    const data = await apiResponse.json();
    response.status(200).json(data);

  } catch (error) {
    console.error("Internal Server Error:", error.message);
    response.status(500).json({ message: "Error processing your request.", details: error.message });
  }
}