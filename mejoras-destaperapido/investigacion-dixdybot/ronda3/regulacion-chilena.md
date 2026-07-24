# Arbitraje: regulación chilena aplicable a dixdybot (bot de ventas WhatsApp)

Fecha de verificación: 2026-07-23. Método: fuentes primarias (XML oficial de LeyChile/BCN,
datos.bcn.cl, Diario Oficial, web service público del Senado, oficio de ley de la Cámara de
Diputados descargado de camara.cl, resoluciones ANCI). Cada dato tiene fuente y fecha. Regla
del dueño cumplida: ningún veredicto descansa en una sola página; los textos legales se
leyeron del original.

---

## 1. Ley 21.719 — Protección de datos personales

**Fechas (CONFIRMADO).** Promulgada el 25-nov-2024 y publicada en el Diario Oficial el
**13-dic-2024** (datos.bcn.cl/recurso/cl/ley/21719, consultado 2026-07-23; idNorma LeyChile
1209272). El artículo primero transitorio dice textual: las modificaciones a la ley 19.628
"entrarán en vigencia el día primero del mes vigésimo cuarto posterior a la publicación de
esta ley en el Diario Oficial" → **1 de diciembre de 2026**. El dato "1-dic-2026" de ambos
externos es CORRECTO.

**"Mandatario"/encargado y si aplica a un SaaS (CONFIRMADO).** El nuevo texto de la 19.628
(versión con vigencia diferida 2026-12-01, XML LeyChile idNorma 141599, descargado
2026-07-23) define en su art. 2 letra x): *"Tercero mandatario o encargado: la persona
natural o jurídica que trate datos personales, por cuenta del responsable de datos."* El
art. 15 bis regula el tratamiento por encargo: exige **contrato escrito** (objeto, duración,
finalidad, tipo de datos, categorías de titulares, derechos y obligaciones), prohíbe usar
los datos para otro fin (si lo hace, el encargado pasa a responder como responsable, personal
y solidariamente), prohíbe subdelegar sin autorización específica y escrita, y obliga al
encargado a cumplir los arts. 14 bis (secreto) y 14 quinquies (medidas de seguridad) y a
**reportar al responsable** las vulneraciones. Un SaaS que procesa datos de los clientes de
sus clientes (dixdybot con los chats/contactos de los clientes del negocio) **es exactamente
esta figura**. La Agencia publicará modelos tipo de contrato.

**Derechos de los titulares (CONFIRMADO).** Art. 4: acceso, rectificación, supresión,
oposición, portabilidad y bloqueo. Detallados: art. 5 (acceso), 6 (rectificación),
7 (supresión), 8 (oposición), **8 bis (oposición a decisiones individuales automatizadas,
incluida elaboración de perfiles**, con derecho a explicación e intervención humana — art.
directamente relevante para un bot que decide precios/ofertas), 9 (portabilidad). También
14 sexies: deber del responsable de reportar brechas de seguridad a la Agencia y, si hay
datos sensibles/menores/financieros, a los titulares.

**Multas (MATIZADO — la cifra "20.000 UTM o 4%" necesita precisión).** Art. 35 (texto
consolidado con vigencia 1-dic-2026): leves → amonestación o multa hasta **5.000 UTM**;
graves → hasta **10.000 UTM**; gravísimas → hasta **20.000 UTM**. Reincidencia: hasta 3
veces el monto. El **2% o 4% de los ingresos anuales** NO es el tope general: aplica solo a
empresas que NO sean "de menor tamaño" según la ley 20.416 (es decir, no PYME) y que
**reincidan** en infracción grave (2%) o gravísima (4%), tomándose la más gravosa entre esa
cifra y el triple de la multa. Para un micro-SaaS chileno (PYME), el techo práctico son las
UTM, no el porcentaje.

## 2. Ley 21.663 — Marco de ciberseguridad

**Fechas (CONFIRMADO).** Publicada el 08-abr-2024 (datos.bcn.cl; idNorma 1202434). La
vigencia la fijó el **DFL N° 1-21.663** (Ministerio del Interior, Diario Oficial 24-dic-2024,
CVE 2588834, PDF descargado 2026-07-23): la ley rige desde el **1-ene-2025**, EXCEPTO los
arts. 5°, 8°, 9° y el Título VII (sanciones), que rigen desde el **1-mar-2025**. La Agencia
(ANCI) inició actividades el 1-ene-2025.

**A quién obliga (CONFIRMADO, con matiz importante).** Art. 4: la ley se aplica a
instituciones que presten **servicios calificados como esenciales** y a las calificadas como
**operadores de importancia vital (OIV)**. La lista de servicios esenciales privados incluye
"telecomunicaciones; infraestructura digital; **servicios digitales y servicios de tecnología
de la información gestionados por terceros**", lo que en abstracto podría rozar a un SaaS;
PERO la propia ley encarga a la ANCI identificar "mediante resolución exenta... las
infraestructuras, procesos o funciones específicas que serán calificadas" y calificar los OIV
por resolución (arts. 4-6). En la práctica la ANCI ha corrido procesos formales de
calificación: Res. Ex. 24/2025 (inicia primer proceso OIV), Res. Ex. 50/2025 (nómina
preliminar + consulta pública), **Res. Ex. 87/2025 (nómina definitiva del primer proceso)**
y Res. Ex. 85/2026 (segunda etapa) — anci.gob.cl/normativa/resoluciones/, consultado
2026-07-23. **Un micro-SaaS como dixdybot NO está hoy bajo estas obligaciones salvo que
aparezca en una calificación expresa de la ANCI** (no plausible a su escala). Conviene
monitorear las resoluciones si el SaaS crece hacia infraestructura digital de terceros.

**Plazo de reporte de 3 horas (CONFIRMADO el plazo; MATIZADO el alcance).** Art. 9 textual:
el deber de reportar al CSIRT Nacional recae en "todas las instituciones públicas y privadas
señaladas en el artículo 4°" (o sea, solo esenciales/OIV, no cualquier empresa). Esquema:
**alerta temprana máx. 3 horas** desde que se conoce el incidente de efecto significativo;
actualización a las **72 horas** (24 horas si es OIV con servicio esencial afectado); informe
final a los **15 días corridos**. Exigible desde el 1-mar-2025. Multas del Título VII: leves
hasta 5.000 UTM (10.000 si OIV), graves 10.000 (20.000 OIV), gravísimas 20.000 (40.000 OIV).

## 3. Proyecto de ley de IA

**Boletín y estado (CONFIRMADO).** Boletín **16821-19** ("Regula los sistemas de
inteligencia artificial"), mensaje presidencial ingresado el 07-may-2024 por la Cámara de
Diputados, **refundido con el 15869-19 (matriz)**. Estado real verificado en el web service
oficial del Senado (tramitacion.senado.cl/wspublico, consultado 2026-07-23): aprobado en
primer trámite por la Cámara el **13-oct-2025** (Oficio de ley N° 20.843 al Senado); hoy en
**segundo trámite constitucional, Senado, Comisión de Desafíos del Futuro, Ciencia,
Tecnología e Innovación (primer informe pendiente)**, con urgencia simple renovada por última
vez el 07-jul-2026. **NO es ley**; a este ritmo no lo será en 2026.

**¿La obligación de declarar "soy una IA" está en el texto? (CONFIRMADO: está textual).**
Del texto aprobado por la Cámara (Oficio 20.843, DOCX descargado de camara.cl el
2026-07-23):
- Art. 4 N°4 (principio de "Transparencia e identificación"): los sistemas de IA "deberán
  **identificarse como agentes artificiales en cada oportunidad en que interactúen con seres
  humanos**, de modo tal que éstos puedan conocer de forma clara y precisa y sean conscientes
  de que se comunican o interactúan con un sistema de IA".
- Art. 11 (Título IV, usos de **riesgo limitado** — donde caería un chatbot de ventas): los
  sistemas de riesgo limitado "deberán garantizar condiciones de transparencia y seguridad...
  de modo tal que **las personas sean informadas de forma clara y precisa y les permitan
  reconocer que están interactuando con un sistema de IA**".
- Art. 5: obligación adicional de que el contenido sintético (audio/imagen/video/texto) sea
  identificable como generado artificialmente.
- Art. 17 (sanciones del proyecto): leves hasta 5.000 UTM, graves hasta 10.000, gravísimas
  hasta 20.000, graduadas por tamaño y ventas del operador.
No es "interpretación": la obligación está escrita. Pero es **proyecto, aún no ley**.

## 4. Normativa de consumo aplicable HOY a un bot que vende

Verificado sobre el texto consolidado de la **Ley 19.496** (XML LeyChile idNorma 61438,
consultado 2026-07-23):
- **Art. 3 letra b)**: derecho del consumidor a "información veraz y oportuna" sobre bienes,
  servicios, precio y condiciones de contratación. Aplica a lo que el bot afirme en el chat.
- **Art. 12 A** (contratación por medios electrónicos): el consentimiento **no se forma** si
  el consumidor no tuvo antes "acceso claro, comprensible e inequívoco de las condiciones
  generales"; el proveedor debe enviar **confirmación escrita** del contrato (copia íntegra y
  legible). Una venta cerrada por WhatsApp es contratación por medios electrónicos.
- **Art. 3 bis letra b)**: **retracto de 10 días** en contratos a distancia/medios
  electrónicos (desde recepción del bien o contratación del servicio); si el proveedor no
  envía la confirmación del 12 A, el plazo se **extiende a 90 días**.
- **Art. 24 (multas)**: regla general hasta **300 UTM**; publicidad falsa por medios masivos
  hasta 1.500 UTM (2.250 UTM si afecta salud/seguridad). La cifra "300 UTM" de los externos
  es correcta como multa general por infracción.
- **Reglamento de Comercio Electrónico**: Decreto 6 (2021) del Ministerio de Economía,
  publicado el **23-sep-2021** (datos.bcn.cl, idNorma 1165504) — detalla deberes de
  información previa (precio total, costos de envío, etc.). Existencia y fecha confirmadas en
  BCN; el texto íntegro no se pudo descargar en esta sesión por rate-limit de LeyChile (la
  fecha de su entrada en vigencia, reportada por SERNAC como marzo 2022, queda sin
  verificación primaria directa).

---

## Obligaciones CONCRETAS para dixdybot

**Vigente HOY (jul-2026):**
1. Ley 19.496: que el bot dé información veraz y oportuna (precio, condiciones); acceso
   claro a términos ANTES de aceptar (art. 12 A); enviar confirmación escrita de cada compra
   (correo/PDF); respetar retracto de 10 días en ventas a distancia (o el plazo sube a 90
   días sin confirmación). Multas típicas: hasta 300 UTM por infracción (más si hay
   publicidad engañosa).
2. Ley 21.663: NO obliga a dixdybot (no es servicio esencial calificado ni OIV en las
   nóminas ANCI 2025-2026). El "reporte en 3 horas" es real pero ajeno: solo instituciones
   del art. 4.
3. Ley 19.628 actual (pre-reforma) sigue vigente hasta el 30-nov-2026: base legal débil y
   sin agencia fiscalizadora — riesgo bajo hoy, pero no excusa para diseñar mal.

**Vigente el 1-dic-2026 (Ley 21.719 — hay que llegar preparados):**
4. Firmar con cada cliente (negocio) un **contrato de encargo de tratamiento** (art. 15 bis):
   dixdybot es "tercero mandatario o encargado". Sin contrato o usando datos para otro fin,
   dixdybot responde como responsable, personal y solidariamente.
5. Implementar medidas de seguridad (art. 14 quinquies), secreto (14 bis) y canal para
   reportar brechas al negocio responsable (y este a la Agencia, art. 14 sexies).
6. Soportar derechos de los titulares: acceso, rectificación, supresión, oposición,
   portabilidad, bloqueo (arts. 4-9) — el SaaS debe poder ubicar/exportar/borrar los datos de
   un consumidor final cuando el negocio lo pida.
7. Ojo con decisiones automatizadas (art. 8 bis): si el bot decide solo (precios, negar
   venta, perfilar), el titular puede oponerse y pedir explicación e intervención humana.
8. Exposición a multas: hasta 5.000/10.000/20.000 UTM (leve/grave/gravísima); el 2%-4% de
   ingresos solo golpea a no-PYME reincidentes.

**Proyecto, aún NO ley (no exigible; sí dirección de viento):**
9. Proyecto de IA (boletín 16821-19, refundido con 15869-19; segundo trámite en el Senado a
   jul-2026): traería la obligación EXPLÍCITA de que el bot se identifique como IA en cada
   interacción (arts. 4 N°4 y 11) y de marcar contenido sintético (art. 5), con multas
   hasta 20.000 UTM (art. 17). Recomendación barata: que dixdybot ya se presente como
   asistente virtual — cuesta cero y anticipa la ley.

## Fuentes primarias usadas (todas consultadas 2026-07-23)
- datos.bcn.cl/recurso/cl/ley/21719 y /21663 (metadatos oficiales BCN: fechas).
- LeyChile XML: idNorma 1209272 (Ley 21.719), 141599 versión 2026-12-01 (Ley 19.628
  consolidada futura), 1202434 (Ley 21.663), 61438 (Ley 19.496).
- Diario Oficial 24-dic-2024, CVE 2588834: DFL N° 1-21.663 (vigencia 21.663).
- tramitacion.senado.cl/wspublico/tramitacion.php?boletin=16821 (estado del proyecto).
- camara.cl, ficha del proyecto prmID=17429: Oficio de ley N° 20.843 (13-oct-2025, texto
  aprobado íntegro, DOCX).
- anci.gob.cl/normativa/resoluciones/ y /normativa/decretos/ (resoluciones OIV, DFL).
- datos.bcn.cl SPARQL: Decreto 6/2021 Economía, "Aprueba Reglamento de Comercio
  Electrónico", publicado 23-sep-2021, idNorma 1165504.
