import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);
const ownerEmailsString = process.env.OWNER_EMAILS;

function sanitize(v) {
  if (typeof v !== 'string') return '';
  return v
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .slice(0, 2000);
}

export default async function handler(request, response) {
  if (request.method !== 'POST') {
    return response.status(405).json({ message: 'Method Not Allowed' });
  }

  try {
    const { name, email, phone, service, comuna, message, website } = request.body || {};

    // Honeypot anti-spam
    if (website) {
      return response.status(200).json({ message: 'OK' });
    }

    if (!name || !phone) {
      return response.status(400).json({ message: 'El nombre y el teléfono son requeridos.' });
    }

    if (!ownerEmailsString) {
      console.error('OWNER_EMAILS no configurado');
      return response.status(500).json({ message: 'Error de configuración del servidor.' });
    }

    const recipientList = ownerEmailsString.split(',').map(e => e.trim()).filter(Boolean);

    const safe = {
      name: sanitize(name),
      email: sanitize(email),
      phone: sanitize(phone),
      service: sanitize(service),
      comuna: sanitize(comuna),
      message: sanitize(message)
    };

    const rows = [
      ['Nombre', safe.name],
      ['Teléfono', safe.phone || 'No proporcionado'],
      ['Email', safe.email || 'No proporcionado'],
      ['Servicio', safe.service || '-'],
      ['Comuna', safe.comuna || '-'],
      ['Mensaje', safe.message ? safe.message.replace(/\n/g, '<br>') : '-'],
    ];

    const html = `
      <h2>Nuevo Lead desde el Formulario de Contacto</h2>
      <table cellpadding="6" style="border-collapse:collapse;font-family:sans-serif;font-size:14px">
        ${rows.map(([k, v]) => `<tr><td style="border:1px solid #ddd"><strong>${k}</strong></td><td style="border:1px solid #ddd">${v}</td></tr>`).join('')}
      </table>
      <p style="margin-top:16px">Por favor, ponte en contacto a la brevedad.</p>
    `;

    await resend.emails.send({
      from: 'Formulario Web <onboarding@resend.dev>',
      to: recipientList,
      subject: `Nuevo lead web: ${safe.name}${safe.comuna ? ' · ' + safe.comuna : ''}`,
      html,
    });

    return response.status(200).json({ message: 'Correo enviado exitosamente.' });

  } catch (error) {
    console.error("Error al enviar correo del formulario:", error);
    return response.status(500).json({ message: 'Error en el servidor.' });
  }
}
