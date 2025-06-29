import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);

export default async function handler(request, response) {
  // Solo permitir peticiones POST
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  console.log('--- INICIO: /api/send-summary ---');

  try {
    const { summaryText, leadEmail, flowType } = request.body;

    // --- LOGS DE DEPURACIÓN ---
    console.log('1. DATOS RECIBIDOS DEL FRONTEND:');
    console.log({ summaryText, leadEmail, flowType });

    const ownerEmailsString = process.env.OWNER_EMAILS;
    console.log('2. CORREOS DE DESTINO:', ownerEmailsString);

    if (!summaryText || !ownerEmailsString) {
      console.error('ERROR CRÍTICO: Falta el resumen (summaryText) o los correos de destino (ownerEmailsString).');
      return response.status(400).json({ message: 'Falta el texto del resumen o la lista de emails del destinatario.' });
    }

    const subject = flowType === 'emergency' 
      ? `🚨 NUEVO DESTAPE URGENTE: ${leadEmail || 'Teléfono no capturado'}`
      : `🗓️ NUEVA VISITA AGENDADA: ${leadEmail || 'Teléfono no capturado'}`;
    
    console.log('3. ASUNTO DEL CORREO:', subject);
    
    const recipientList = ownerEmailsString.split(',').map(email => email.trim());
    console.log('4. LISTA DE DESTINATARIOS PROCESADA:', recipientList);

    console.log('5. INTENTANDO ENVIAR CORREO A TRAVÉS DE RESEND...');
    const { data, error } = await resend.emails.send({
      from: 'Asistente Web <onboarding@resend.dev>',
      to: recipientList,
      subject: subject,
      html: `<p>Tu asistente virtual ha gestionado un nuevo lead:</p><hr><pre style="white-space: pre-wrap; font-family: monospace;">${summaryText}</pre><hr>`,
    });

    if (error) {
      console.error('ERROR DEVUELTO POR RESEND:', JSON.stringify(error, null, 2));
      return response.status(400).json(error);
    }

    console.log('6. ¡ÉXITO! Correo enviado. Respuesta de Resend:', data);
    response.status(200).json(data);

  } catch (error) {
    console.error("ERROR CATASTRÓFICO EN LA FUNCIÓN:", error.message);
    response.status(500).json({ message: 'Error procesando la solicitud.', details: error.message });
  }
}