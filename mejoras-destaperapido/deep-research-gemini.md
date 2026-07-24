# Deep research Gemini — Rediseño dixdybot (pegado por Alejandro, 23-jul-2026)

> NOTA DE PROCEDENCIA: texto generado por Gemini Deep Research con los 2 MD de las rondas
> como adjuntos. NO verificado — contiene señales de alucinación detectadas a simple vista
> (llama al bot "urgencias médicas chilenas"; recomienda "Claude 3.5 Sonnet", modelo 2024;
> repo de ARIA que nuestro verificador no encontró). Ver el arbitraje en
> DIXDYBOT-RONDA3-CONTRASTE.md antes de usar cualquier dato de aquí.

## Refutaciones que plantea (resumen fiel)

1. **Gateway propio = error**; adoptar BSP/plataforma con pasarela a Cloud API.
2. **PWA insuficiente**: push en segundo plano poco fiable en iOS/Android; pide contenedor
   nativo (Capacitor/React Native) con APNs/FCM para el pausa-y-pregunta.
3. **Editor sin canvas = opacidad**; propone híbrido: cascada vertical / bloques
   colapsables (coincide en rechazar el canvas de nodos arrastrables).
4. **Coexistence inviable como default**: regla de abrir la app cada 14 días o la API
   expira; afirma "40-50% de webhooks perdidos con tráfico alto" (SIN fuente citada);
   bloquea mensajes temporales/view-once/grupos/estados; bucles de sincronización de
   contactos duplicados. Recomienda migración limpia y definitiva a Cloud API.
5. **Cerebro por CLI/suscripción inviable**: violación de ToS multi-tenant (coincide con
   nuestro plan E6), "latencia 5-10s" (contradice nuestros datos reales), recomienda
   "Claude 3.5 Sonnet / Claude 3 Haiku" (⚠️ modelos de 2024 — señal de obsolescencia).
6. **Evolución incremental = antipatrón**; reescritura limpia multi-tenant desde cero
   (⚠️ llama al bot "urgencias médicas chilenas" — leyó mal el contexto).

## Datos que aporta (a verificar)

- Tarifas Meta Chile: marketing US$0,0889 / utility y auth US$0,0200; service gratis hasta
  30-sep-2026, luego cada mensaje de servicio a tarifa utility (~$19 CLP).
- Meta Business Agent: US$2/M tokens desde 1-ago-2026, ~$0,04-0,05/mensaje (20-25k tokens
  por inferencia); pymes lo reportan como "soporte pasivo" sin flujos transaccionales.
- Baileys: detección por ausencia de retraso de escritura, lectura sincrónica perfecta, y
  "Error 463 Reachout Timelock" (envío a números sin historial reporta enviado pero no
  llega; reincidencia = ban permanente).
- White-label: Stammer AI ($300-500 USD/mes por cliente, 0% revenue share), Botsify,
  Relevance AI (Team $349/mes, 7.000 acciones + $70 créditos).
- Mercado chileno granular (SuperPyme/Wati/Treble): $14.990 CLP (menú fijo) → $29.990 (IA
  FAQ) → $49.990 (cotizador con Sheets) → $53-125 mil (integrado ecommerce) → $150-350 mil
  (a medida con CRM). Implementaciones $49.990-390.000 CLP.
- Salesforce compró Intercom/Fin por US$3.600M — anuncio 15-jun-2026, cierre ~Q4 FY2027.
- ARIA: repo público "github.com/yf-he/aria" MIT (⚠️ nuestro verificador no lo encontró).
- Voice AI: Retell (~600ms, $0,055/min base, total $0,115-0,15/min), Bland ($0,14/min +
  planes $299/$499), Vapi ($0,05/min base, total $0,25-0,33/min).
- Ley 21.719 datos personales: vigencia 1-dic-2026, dixdybot = "mandatario", DPAs
  obligatorios, derechos ARCO+P en panel, multas hasta 20.000 UTM o 4% facturación global.
- Ley 21.663 ciberseguridad: reporte de incidentes al CSIRT en 3 horas (servicios
  esenciales), multas hasta 20.000 UTM.
- Proyecto ley IA (Boletín 16821-19): segundo trámite en Senado; prohibición biometría
  remota; obligación de transparencia conversacional (declarar que es IA).
- Frameworks: "CoNL (ICML 2026)" self-play para habilidades de venta; "EvoTest (ICLR
  2026)" aprendizaje evolutivo en inferencia (⚠️ existencia por verificar).
