import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    const { summaryText, leadEmail } = request.body;
    // Leemos la nueva variable de entorno que contiene los correos
    const ownerEmailsString = process.env.OWNER_EMAILS;

    if (!summaryText || !ownerEmailsString) {
      return response.status(400).json({ message: 'Falta el texto del resumen o la lista de emails del destinatario.' });
    }

    // Convertimos el string de correos separados por coma en un array
    const recipientList = ownerEmailsString.split(',').map(email => email.trim());

    // Enviamos el correo a la lista de destinatarios
    const { data, error } = await resend.emails.send({
      from: 'Lead Notifier <onboarding@resend.dev>',
      to: recipientList, // Aquí usamos la lista de correos
      subject: `Nuevo Lead Calificado: ${leadEmail || 'Email no capturado'}`,
      html: `<p>¡Felicitaciones! Tu chatbot ha calificado un nuevo lead.</p><pre>${summaryText}</pre>`,
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