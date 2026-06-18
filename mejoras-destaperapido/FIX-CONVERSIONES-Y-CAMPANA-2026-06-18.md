# 🔧 Por qué se cayeron las conversiones de teléfono + arreglos — destaperapido.cl

**Fecha:** 2026-06-18 · Cuenta Ads `3106881217` · Contenedor GTM `GTM-PG2RQNCD`

---

## 1. La causa raíz (confirmada)

Las conversiones **"Click Teléfono"** marcaban bien hasta enero (dic: 46, ene: 26) y **cayeron a 0 desde febrero**. Comparé lo que GTM envía contra lo que la cuenta de Google Ads espera:

| Conversión | Label correcto (en Google Ads) | Label puesto en GTM | ¿OK? |
|---|---|---|---|
| Click Whatsapp | `m7BxCIqvp8YbEMuIgstB` | `m7BxCIqvp8YbEMuIgstB` | ✅ |
| Formulario | `Axi9CMTyq8YbEMuIgstB` | `Axi9CMTyq8YbEMuIgstB` | ✅ |
| **Click Teléfono** | **`Z1iuCLLEpsYbEMuIgstB`** | **`MafhCLylyuobEK7uxclC`** ❌ | **NO** |

**La etiqueta "Ads - Conversión Teléfono" de GTM tiene el Conversion Label equivocado.** Se editó por última vez ~22-ene-2026 (la de WhatsApp no se toca desde nov-2025 y por eso nunca dejó de funcionar). Desde ese cambio, cada clic en un `tel:` dispara la conversión hacia un identificador que **no existe** en la cuenta → no se registra nada.

> No es problema del sitio. Los enlaces `tel:` (339 en el sitio) están bien, el contenedor GTM se carga en todas las páginas, el trigger "Click telefono" (CONTAINS `tel:`) es genérico y correcto. **Es un solo campo mal escrito en GTM.**

El Conversion ID (`17605624907`) sí está bien; **solo hay que corregir el Label**.

---

## 2. 🛠️ TUTORIAL — Arreglar el Label en GTM (lo tienes que hacer tú)

1. Entra a **https://tagmanager.google.com** con tu cuenta.
2. Abre el contenedor **`GTM-PG2RQNCD`** (www.destaperapido.cl).
3. Menú izquierdo → **Etiquetas (Tags)** → abre **"Ads - Conversión Teléfono"**.
4. En **ID de conversión** debe decir `17605624907` (déjalo igual).
5. En **Etiqueta de conversión (Conversion Label)** verás `MafhCLylyuobEK7uxclC`.
   **Bórralo y escribe exactamente:**
   ```
   Z1iuCLLEpsYbEMuIgstB
   ```
6. **Guardar**.
7. Arriba a la derecha → **Enviar (Submit)** → ponle nombre (ej. "Fix label teléfono") → **Publicar**.

### Cómo verificar que quedó bien
1. En GTM, arriba → **Vista previa (Preview)** → escribe `https://www.destaperapido.cl` → Connect.
2. En la web que se abre, haz **clic en un botón/enlace de teléfono**.
3. En el panel de Tag Assistant, en ese evento de clic debe **dispararse "Ads - Conversión Teléfono"** (Tags Fired).
4. En Google Ads → **Objetivos → Conversiones → "Click Teléfono"**: en 24-48h el estado debe volver a **"Registrando conversiones"** y empezar a sumar.

> ⚠️ Importante: mientras esto estuvo roto (feb–jun), Maximize Conversions optimizó **a ciegas** sin la señal de teléfono. Al arreglarlo, el algoritmo recupera datos y el CPA reportado bajará (parte del "CPA alto" era medición incompleta).

---

## 3. ✅ Lo que YA dejé hecho

### En el sitio (HTML) — repo destaperapido
- **Agregué GTM a 9 páginas que no lo tenían** (no registraban NADA): `documentos.html`, `ruta-buin.html` y 7 posts de blog. Script: `scripts/fix_add_gtm.py` (idempotente). Antes: 9 páginas sin tracking → ahora: 0.
- Validé el resto: 103 páginas ya tenían GTM, los `tel:` están bien formados, no hay snippets de conversión hardcodeados que compitan con GTM.
- *(Pendiente tuyo: desplegar el sitio para que estos cambios queden online.)*

### En las campañas (cuenta Ads 3106881217)
- **Campaña 01 "Rural - Fosas y Parcelas": budget bajado $55.000 → $25.000/día.** Con 87% de impression share y solo 1,8% perdido por presupuesto, el $55k solo habilitaba el sobregasto de mayo (~$972k/mes a CPA ~$12.600). $25k sigue holgado vs la época dorada (~$13k/día). Reversible.
- **Campaña 02 "Fosas Rural - chicureo": PAUSADA.** 0 conversiones desde enero, sin demanda de búsqueda (Chicureo no se busca). Reversible.
- **NO toqué el tCPA** (está en $4.800). Se ha cambiado demasiado seguido (05-jun y 13-jun) y cada cambio reinicia el aprendizaje. **Déjalo quieto 3-4 semanas.**

---

## 4. La historia del CPA (resumen del análisis de 8 meses)

- **Época dorada (dic-2025 → mediados ene-2026):** CPA **$2.000–$3.500**, tracking completo, CPC ~$1.500. Es el benchmark.
- **Caída:** un **parón de ~2 meses (feb→abr)** reseteó el aprendizaje de Smart Bidding; al relanzar en abril el CPC explotó a **$3.954** y el CPA llegó a **$11.000–$16.000**.
- En paralelo, **se rompió el tracking de teléfono (feb)**, agravando todo.
- **Daño estimado:** ~$875.000 CLP de sobregasto en las 6 semanas malas (abr-may).

*(Detalle semana a semana en `fullfosas/google-ads/ANALISIS-DESTAPERAPIDO-2026-06-18.md`.)*

---

## 5. Recomendaciones que quedan (para aplicar después)

| # | Acción | Quién | Estado |
|---|---|---|---|
| 1 | **Arreglar label de teléfono en GTM** | Tú (tutorial arriba) | 🔴 Pendiente — lo más importante |
| 2 | Desplegar el sitio (GTM en las 9 páginas) | Tú | 🟠 Pendiente |
| 3 | Bajar budget a $25k | ✅ Hecho | — |
| 4 | Pausar Chicureo | ✅ Hecho | — |
| 5 | **No cambiar el tCPA por 3-4 semanas** | Tú (no hacer nada) | 🟠 Política |
| 6 | **No volver a pausar la campaña por semanas** (resetea aprendizaje). Si hay que frenar, bajar budget | Tú | 🟠 Política |
| 7 | Tras 2 semanas con tracking arreglado + budget estable, reevaluar CPC/CPA | Nosotros | 🟢 Seguimiento |
| 8 | Considerar enlaces de teléfono que llamen a `gtag_report_conversion` (clic más fiable) — opcional, el trigger GTM ya cubre | — | 🟢 Opcional |

---

## 6. Nota técnica — por qué WhatsApp sobrevivió y teléfono no

Mismo mecanismo (GTM LINK_CLICK), pero la etiqueta de WhatsApp conservó su label correcto (`m7BxCIqvp8YbEMuIgstB`) desde noviembre, mientras que la de teléfono fue editada en enero y quedó con un label inválido. Por eso la curva de WhatsApp siguió sana y la de teléfono se fue a cero. Es la prueba de que el resto del setup (contenedor, triggers, sitio) funciona.
