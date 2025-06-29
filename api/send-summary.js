import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    const { summaryText, leadEmail, flowType } = request.body; // 1. Recibimos el flowType
    const ownerEmailsString = process.env.OWNER_EMAILS;

    if (!summaryText || !ownerEmailsString) {
      return response.status(400).json({ message: 'Falta el texto del resumen o la lista de emails del destinatario.' });
    }

    // 2. Definimos el asunto del correo dinámicamente
    const subject = flowType === 'emergency' 
      ? `🚀 Destape prioritario: ${leadEmail || 'Teléfono no capturado'}`
      : `🗓️ Nueva visita agendada: ${leadEmail || 'Teléfono no capturado'}`;

    const recipientList = ownerEmailsString.split(',').map(email => email.trim());

    const { data, error } = await resend.emails.send({
      from: 'Asistente Web <onboarding@resend.dev>',
      to: recipientList,
      subject: subject, // 3. Usamos el asunto dinámico
      html: `<p>Tu asistente virtual ha gestionado un nuevo lead:</p><pre>${summaryText}</pre>`,
    });

    if (error) {
      console.error("Error sending email:", error);
      return response.status(400).json(error);
    }

    response.status(200).json(data);

  } catch (error) {
    console.error("Internal server error:", error.message);
    response.status(500).json({ message: 'Error procesando la solicitud.' });
  }
}