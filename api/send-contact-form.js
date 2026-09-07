import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);
const ownerEmailsString = process.env.OWNER_EMAILS;

// Página desde la que se envió el formulario: lo que declara el propio formulario
// (body.page = location.href) o, si falta, el Referer del navegador (mismo origen → URL completa).
export function paginaOrigen(headers, body) {
  const declarada = body && typeof body.page === 'string' ? body.page : '';
  const referer = (headers && (headers.referer || headers.referrer)) || '';
  const raw = (declarada || referer).trim();
  if (!raw) return { url: '', etiqueta: '' };
  try {
    const u = new URL(raw);
    const ruta = u.pathname.replace(/\.html$/, '').replace(/\/$/, '');
    const host = u.host.replace(/^www\./, '');
    return { url: u.href, etiqueta: ruta ? host + ruta : host + ' (portada)' };
  } catch {
    return { url: '', etiqueta: '' };
  }
}

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
    const body = request.body || {};
    const { name, email, phone, service, comuna, message, website } = body;

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

    const pagina = paginaOrigen(request.headers, body);
    const rows = [
      ['Página', pagina.url ? `<a href="${sanitize(pagina.url)}">${sanitize(pagina.etiqueta)}</a>` : 'no informada'],
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

    // Resend NO lanza excepción cuando rechaza: devuelve { error }. Sin mirarlo, el
    // formulario decía "enviado" y el lead se perdía en silencio.
    const { error } = await resend.emails.send({
      from: 'Formulario Web <onboarding@resend.dev>',
      to: recipientList,
      subject: `${pagina.etiqueta ? '[' + pagina.etiqueta + '] ' : ''}Nuevo lead web: ${safe.name}${safe.comuna ? ' · ' + safe.comuna : ''}`,
      html,
    });
    if (error) {
      console.error('[send-contact-form] Resend rechazó el envío:', error);
      return response.status(502).json({ message: 'El proveedor de email rechazó el envío.' });
    }

    return response.status(200).json({ message: 'Correo enviado exitosamente.' });

  } catch (error) {
    console.error("Error al enviar correo del formulario:", error);
    return response.status(500).json({ message: 'Error en el servidor.' });
  }
}
