# DIXDYBOT — Ronda 3: arbitraje de los deep research externos (ChatGPT y Gemini)

**Fecha:** 23-jul-2026 · **Cómo se hizo:** Alejandro corrió el prompt de deep research en
ChatGPT (`deep-research-report.md`) y Gemini (`deep-research-gemini.md`). 9 árbitros con
orden de dirimir SOLO con fuente primaria (rate cards de Meta, Boletín Oficial, repos
reales, páginas oficiales de pricing) + 1 medidor de latencia sobre los logs del bot vivo.
Detalle en `investigacion-dixdybot/ronda3/`.

## La lección meta (valida la regla de escepticismo)

**Ninguna de las tres investigaciones fue infalible.** Nuestra ronda 1 usó la banda de
tarifas equivocada; ChatGPT citó una tabla con recargo de intermediario como si fuera de
Meta; Gemini inventó una cifra clave (40-50% de webhooks perdidos) y erró el contexto del
negocio… pero acertó donde los otros dos fallaron (tarifas de Chile, y tres claims de
papers/repos que los demás no encontraron). El método correcto quedó demostrado: **ningún
informe manda; manda la fuente primaria.**

## Veredictos que CAMBIAN el plan

1. **Tarifas Chile (ganó Gemini):** el rate card CSV oficial de Meta (effective 1-jul-2026)
   da a Chile fila propia: **marketing US$0,0889 / utility y auth US$0,0200**. Nuestra
   ronda 1 (0,074/0,0113) usaba la banda "Rest of Latin America" que NO incluye a Chile;
   la cifra de ChatGPT (0,10224/0,023) era la tarifa de Meta +15% de un BSP. Confirmado en
   doc primaria de Meta: desde el **1-oct-2026 se cobran TODOS los service messages y
   también los utility dentro de la ventana de 24h** (solo la ventana de 72h por anuncio
   CTWA sigue gratis). Presupuesto real para nuestro volumen (~960 msgs/mes):
   **~US$20/mes (~CLP 17.000) desde octubre** — recalcular cuando salgan las tarifas
   definitivas (antes del 1-sep).
2. **Coexistence (matizado a favor, con ajuste):** para ESTE cliente NO es trampa — es la
   única ruta que conserva la app del teléfono que Alejandro usa a diario; hasta el
   artículo anti-Coexistence de Spur lo recomienda para exactamente este perfil (migración
   gradual + atención manual + equipo chico). Límites reales confirmados en doc de Meta:
   20 msg/s (sobra), abrir la app cada ~14 días (se cumple solo), se pierden difusiones/
   view-once/ubicación en vivo (no los usamos); editar mensajes YA funciona. **Ajuste al
   plan: 30-sep pasa de "fecha de corte" a "fecha de DECISIÓN tras piloto en un número
   secundario"**, sin depender del history-sync (nuestro CRM ya guarda todo), con Baileys
   como fallback caliente 30-60 días y dedup vía envios.jsonl. El "40-50% de webhooks
   perdidos" de Gemini: **inventado, cero fuentes** — eliminado del expediente.
3. **"Cirugía de plataforma" (matizado):** el patrón manifest + schema-driven-UI es real
   (Shopify/WordPress/Slack/OpenAI, docs primarias), pero existe para ecosistemas de
   módulos de TERCEROS; DIXDY es first-party con clon-por-cliente → no se construye
   tenant_id ni registro con permisos. **Se insertan en E2 (+2-3 días, no semanas) tres
   convenciones:** (a) convId canónico (`identidad.js`) — desde E2 nada nuevo se escribe
   con clave jid; (b) JSON Schema junto a tarifario.json/ajustes.json y la vista Ajustes
   renderizada desde el schema (así los módulos nuevos nacen administrables, el requisito
   de Alejandro); (c) eventos.jsonl append-only como libro del embudo. E4 sigue siendo la
   cirugía real del canal; **la reescritura desde cero de Gemini queda refutada de nuevo.**
4. **Error 463 "Reachout Timelock" (Gemini acertó):** real y ACTIVO en Baileys a jul-2026
   (issues #2707/#2698/#2688): mensajes a números sin historial figuran "enviados" pero no
   llegan, y reintentar lleva a ban. **Entra a E0-E1: verificar entrega real (✓✓) en vez de
   confiar en el estado "sent", mantener solo-respondedor, prohibir outreach en frío.**
5. **Regulación chilena (vacío real nuestro, ambos externos aciertan en lo grueso):**
   - **HOY (Ley 19.496):** un bot que vende debe dar información veraz, acceso claro a
     condiciones, **confirmación escrita de cada compra**, y respetar el retracto de 10
     días en venta a distancia (90 si no hay confirmación); multas hasta 300 UTM.
   - **1-dic-2026 (Ley 21.719):** dixdybot será "tercero mandatario/encargado" (art. 15
     bis) → antes de esa fecha: contrato de encargo de tratamiento con cada cliente,
     medidas de seguridad, flujo de reporte de brechas, y capacidad en el panel de
     acceso/rectificación/supresión/portabilidad. El **art. 8 bis (decisiones
     automatizadas: derecho a explicación e intervención humana) convierte nuestro
     humano-en-el-loop en cumplimiento legal, no solo en feature.** Multas hasta 20.000
     UTM (el 2-4% solo a no-PYME reincidentes).
   - **Proyecto, no ley (boletín 16821-19, refundido con 15869-19):** el deber de
     declararse IA está textual en los arts. 4 y 11 del texto de la Cámara; no exigible
     aún, pero presentarse como asistente virtual desde ya cuesta cero y anticipa la ley.
   - La Ley 21.663 de ciberseguridad **NO** obliga a dixdybot (solo servicios esenciales).
6. **Pricing afinado (mercado chileno verificado):** tier 4-6 UF validado (Lelemon
   3,8-6,9 UF, herihe 5 UF, ScaleTech 6 UF); tier 8-12 UF defendible solo con la
   diferenciación (cotizador+panel+entregas+entrenamiento); presión a la baja en la
   entrada (Brote US$29, SuperPyme $29.990-49.990 CLP) → el tier bajo se vende como
   servicio gestionado, no como software; **agregar setup fee de implementación 5-10 UF**
   (3 actores lo validan). Ideas a copiar: onboarding por audio del dueño (Brote), primer
   mes gratis + excedente por conversación en CLP (Lelemon). El "WAI chileno" de ChatGPT
   **no existe** (descartado).

## Veredictos que RATIFICAN el plan

- **Cerebro por CLI ratificado con datos propios:** latencia real del cerebro 8-18s
  (mediana 8,2s, p90 16,6s, 0 timeouts) — Gemini incluso se quedó corto — pero el total
  que vive el cliente (mediana 22,6s, p90 46,5s) está dentro del rango humano de WhatsApp
  (30-90s) y el cuello es el **delay deliberado anti-ban**, no el cerebro. Migrar a API
  "por latencia" optimizaría el componente equivocado. (El failover E1 sigue, por los
  motivos de ToS/límites, no por velocidad.)
- **Evolución incremental ratificada por tercera vez** (la reescritura de Gemini choca con
  la auditoría real del código y con la fecha dura de canal).
- **PWA ratificada** (ChatGPT tampoco pudo refutarla).
- **Salesforce SÍ compró Fin/Intercom** (~US$3.600M, anuncio 15-jun-2026, fuentes
  primarias dobles; nuestro verificador de ronda 2 falló por bloqueos de acceso, no por
  falsedad): la consolidación enterprise valida la tesis y deja libre el nicho local.
- **ARIA tiene repo oficial** (github.com/yf-he/aria, MIT — esqueleto, referencia
  conceptual, no dependencia), y **EvoTest (ICLR 2026) y CoNL (ICML 2026) existen** —
  mismo laboratorio NUS que ARIA; inspiración para el gimnasio/caminos, sin prometer
  resultados de dominio.
- **Voz (E7):** costo real todo incluido US$0,09-0,15/min → recuperar una llamada perdida
  (~3 min) cuesta ~CLP 300-500 vs un destape de $40.000+. Piloto futuro con Retell
  (es-419, webhook → nuestro bot); ElevenLabs como candidato B (WhatsApp nativo pero exige
  API oficial). Pipecat = construir, prohibido en fase explorar.

## Correcciones a los archivos externos

- `deep-research-gemini.md`: útil en tarifas, papers y Error 463; **inventó** el 40-50%
  de webhooks y los bucles de contactos; erró el rubro del negocio ("urgencias médicas"),
  recomendó modelos 2024, y su escalera de SuperPyme estaba mal ($79.990 y "desde
  $149.990" son los tramos reales).
- `deep-research-report.md` (ChatGPT): el mejor en arquitectura/producto y Coexistence;
  **erró las tarifas** (tabla BSP+15%) y el "WAI chileno" no existe; treble.ai no publica
  precios (su cifra no se sostiene).
