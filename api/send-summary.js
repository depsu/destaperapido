import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(request, response) {
  // Solo permitir peticiones POST
  if (request.method !== 'POST') {
    console.log('Intento de acceso con método no permitido:', request.method);
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  console.log('--- Iniciando /api/send-summary ---');

  try {
    const { summaryText, leadEmail } = request.body;
    console.log('Payload recibido del frontend:', request.body);

    const ownerEmailsString = process.env.OWNER_EMAILS;
    const resendApiKey = process.env.RESEND_API_KEY;

    // --- LOGS CLAVE ---
    console.log('1. Texto del resumen (summaryText):', summaryText);
    console.log('2. Email/Teléfono del lead (leadEmail):', leadEmail);
    console.log('3. Correos de destino (OWNER_EMAILS):', ownerEmailsString);
    console.log('4. ¿Existe la RESEND_API_KEY?', !!resendApiKey);


    if (!summaryText || !ownerEmailsString) {
      console.error('Error Crítico: Faltan datos. Revisar summaryText y ownerEmailsString en los logs de arriba.');
      return response.status(400).json({ message: 'Falta el texto del resumen o la lista de emails del destinatario.' });
    }

    const recipientList = ownerEmailsString.split(',').map(email => email.trim());
    console.log('5. Lista de destinatarios procesada:', recipientList);

    console.log('6. Intentando enviar correo con Resend...');
    const { data, error } = await resend.emails.send({
      from: 'Lead Notifier <onboarding@resend.dev>',
      to: recipientList,
      subject: `Nuevo Lead Calificado: ${leadEmail || 'Teléfono no capturado'}`,
      html: `<p>¡Felicitaciones! Tu chatbot ha calificado un nuevo lead.</p><pre>${summaryText}</pre>`,
    });

    if (error) {
      console.error("Error devuelto por Resend:", error);
      return response.status(400).json(error);
    }

    console.log('7. ¡Correo enviado exitosamente! Respuesta de Resend:', data);
    response.status(200).json(data);

  } catch (error) {
    console.error("Error catastrófico en la función /api/send-summary:", error.message);
    response.status(500).json({ message: 'Error procesando la solicitud.', details: error.message });
  }
}