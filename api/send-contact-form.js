import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);
const ownerEmailsString = process.env.OWNER_EMAILS; // Usamos la misma lista de correos

export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    const { name, email, phone } = request.body;

    if (!name || !email) {
      return response.status(400).json({ message: 'El nombre y el email son requeridos.' });
    }

    const recipientList = ownerEmailsString.split(',').map(e => e.trim());
    const phoneInfo = phone ? `<p><strong>Teléfono:</strong> ${phone}</p>` : '<p><strong>Teléfono:</strong> No proporcionado</p>';

    await resend.emails.send({
      from: 'Formulario Web <onboarding@resend.dev>',
      to: recipientList,
      subject: `Nuevo Mensaje del Formulario de ${name}`,
      html: `
        <h2>Nuevo Lead desde el Formulario de Contacto</h2>
        <p><strong>Nombre:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        ${phoneInfo}
        <p>Por favor, ponte en contacto a la brevedad.</p>
      `,
    });

    return response.status(200).json({ message: 'Correo enviado exitosamente.' });

  } catch (error) {
    console.error("Error al enviar correo del formulario:", error);
    return response.status(500).json({ message: 'Error en el servidor.' });
  }
}