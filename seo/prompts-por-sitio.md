# Prompts por tipo de sitio — Destape Rápido

> Cómo usar este archivo: abre la pestaña del sitio donde te quieres registrar, abre Claude for Chrome (extensión) y pega el prompt de la sección correspondiente. **Antes de cualquier prompt**, abre también `seo/nap-destaperapido.md` en otra pestaña porque la IA necesita esos datos para llenar todo. Por convención, en cada prompt incluye el contenido completo de la hoja NAP pegándolo donde diga `<<HOJA NAP>>`.

> Al terminar cada registro, abre `seo/backlinks-tracker.csv` y actualiza la fila: `estado` → "publicado", `url_perfil_creado` → URL del perfil, `fecha` → hoy.

---

## 0. Prompt maestro — reglas globales (se usa al inicio de cada sesión)

Pega esto **antes** del prompt específico, una vez por sesión:

```
Vas a ayudarme a registrar mi empresa "Destape Rápido" en directorios y portales para
mejorar el SEO local y backlinks. Tengo una hoja NAP que es la fuente única de verdad.

REGLAS GLOBALES (no las rompas nunca):

1. NAP CONSISTENTE: usa siempre el mismo nombre, mismo teléfono formateado igual
   (+56 9 2846 1485 con espacios o +56928461485 sin espacios según pida el sitio),
   y la misma URL (https://www.destaperapido.cl con www, sin barra al final).

2. NO INVENTES DATOS. Si un campo obligatorio no está en mi hoja NAP, DETENTE y
   preguntame.

3. ANTI-DUPLICADO SEO: si vas a publicar una descripcion, mira el CSV de tracking
   y NO uses la misma version (A/B/C) que ya use en otro directorio del mismo nivel
   de prioridad. Mantengo 3 versiones por longitud justamente para eso.

4. CAPTCHA / SMS / OTP / LOGIN: si aparece cualquier verificacion humana, PARA,
   dime claramente en que paso estas y espera a que yo lo resuelva.

5. PASSWORDS: si pide crear cuenta, usa email contacto@destaperapido.cl pero PARA
   y pideme la contrasena (no la inventes).

6. CONFIRMACION ANTES DE PUBLICAR: antes del SUBMIT/PUBLICAR final, muestrame un
   resumen completo de todo lo que vas a enviar y espera mi OK explicito.

7. POST-PUBLICACION: cuando termines, copia la URL publica del perfil creado y
   damela en texto claro para que la guarde en el CSV de tracking.

8. ZONA HORARIA: estamos en Chile (America/Santiago). Si pide horario, marca
   "24 horas, todos los dias".

<<HOJA NAP>>
[Pega aquí el contenido completo de seo/nap-destaperapido.md]
<<FIN HOJA NAP>>

Confirma que entendiste las reglas y dime que estas listo. Aun no hagas nada.
```

---

## 1. Mapas (Google Business, Bing, Apple, Waze) — MÁXIMA PRIORIDAD

```
Estamos en [Google Business Profile / Bing Places / Apple Business Connect / Waze
for Business] y quiero registrar Destape Rapido. Sigue estos pasos:

1. Si pide crear empresa, marca el tipo "EMPRESA DE SERVICIOS / AREA DE SERVICIO"
   (NO atencion al publico en direccion fija). Esto es crucial: somos servicio a
   domicilio, no recibimos clientes en oficina.

2. Categoria principal exacta: busca y selecciona "Plumber" / "Fontanero" /
   "Gasfiter". Si esta disponible, agrega tambien "Septic system service" /
   "Servicio de fosas septicas".

3. Direccion: PRIORIDAD = ocultarla. Marca "no mostrar direccion publica" si la
   plataforma lo permite (Google Business, Bing Places, Apple Business y la mayoria
   de portales serios lo permiten para empresas de area de servicio). SOLO si la
   plataforma EXIGE direccion publica visible, usa la direccion legal:
   "Andalucia 3661, Maipu, Region Metropolitana, Chile". El RUT 77.193.424-2 va
   solo en campos administrativos/facturacion, nunca en perfil publico.

4. Area de servicio: agrega TODAS las comunas listadas en la seccion 6 de la hoja
   NAP (urbanas y rurales). Si limita a 20, prioriza las urbanas + Chicureo, Pirque,
   Buin, Talagante, Melipilla.

5. Telefono: +56 9 2846 1485.

6. Horario: marca "abierto 24 horas" todos los dias de la semana.

7. Descripcion: usa la version LARGA A de la hoja NAP (770 caracteres
   aproximadamente, dentro del limite de 750 de Google).

8. Sitio web: https://www.destaperapido.cl

9. Servicios: agrega cada servicio de la seccion 5 de la hoja NAP. Para cada uno,
   pon una descripcion corta de 1 linea con el precio "desde" si esta listado.

10. Fotos: sube en este orden (rutas en seccion 7 de la hoja NAP):
    a. Logo principal (logo.png) como foto de perfil/identidad
    b. Camion en calle como foto de portada
    c. Las 4 fotos de galeria de la hoja NAP

11. Atributos: marca todos los que apliquen:
    - Atencion 24/7
    - Servicio a domicilio
    - Servicio de emergencia
    - Factura electronica
    - Acepta tarjetas
    - Acepta transferencias

12. Verificacion: cuando llegue al paso de verificacion (SMS, llamada o postal),
    PARA y avisame. Para Google la postal puede tardar 14 dias.

Antes de hacer cualquier cosa, dame un plan corto de lo que vas a hacer y espera
mi OK.
```

---

## 2. Directorios chilenos generalistas (Páginas Amarillas, Infoisinfo, Mercantil, etc.)

```
Estamos en [NOMBRE DEL DIRECTORIO]. Quiero registrar Destape Rapido en su seccion
gratuita / plan basico. Pasos:

1. Busca el enlace "Agregar mi empresa", "Publica tu negocio", "Registra tu
   empresa" o similar. Si no lo encuentras en 30 segundos, avisame.

2. Si pide eleccion entre plan gratis y plan pago, ELIGE GRATIS por ahora. Tomare
   nota del plan pago para evaluarlo despues.

3. Categoria: busca "Destape de alcantarillado" o "Limpieza de fosas septicas".
   Si no existen, usa "Gasfiteria" o "Servicios sanitarios" o "Servicios para
   el hogar" en ese orden de preferencia.

4. Descripcion: usa la version MEDIA [INDICAME CUAL: A, B o C — debe ser distinta
   a la que use en otros directorios del mismo nivel].

5. Datos: copia exacto desde la hoja NAP (nombre, telefono, email, sitio).

6. Direccion: si es opcional, dejala vacia. Si es obligatoria, usa Maipu RM como
   localidad solamente, sin numero de calle.

7. Zonas de servicio: si tiene campo para multiples comunas, agregalas todas. Si
   pide UNA principal, marca "Santiago".

8. Logo: sube el logo.png de la seccion 7 de la hoja NAP. Si el sitio rechaza PNG
   y pide JPG, avisame.

9. Antes de SUBMIT: muestrame el resumen completo y espera mi OK.

10. Despues de publicar: damela URL del perfil creado.
```

---

## 3. Portales de servicios (Cronoshare, Habitissimo, Gasfiter.cl, Plomero.cl)

```
Estamos en [PORTAL]. Este es un portal de servicios que genera leads reales de
clientes, asi que el perfil debe quedar lo mas COMPLETO posible. Pasos:

1. Crea cuenta de profesional con email contacto@destaperapido.cl. Pideme la
   contrasena.

2. Perfil profesional:
   - Nombre del profesional/empresa: Destape Rapido
   - Anos de experiencia: 12
   - Zona de trabajo: Region Metropolitana (todas las comunas de la seccion 6 NAP)
   - Servicios que ofreces: marca TODOS los que existan de la seccion 5 NAP.

3. Descripcion del perfil: usa la version LARGA A de la hoja NAP.

4. Fotos del trabajo: sube las 4 fotos de galeria (seccion 7 NAP) + foto rural.

5. Certificaciones / documentos: si pide subir, indica que tenemos:
   - Resolucion sanitaria SEREMI
   - Inicio de actividades SII
   - Patente municipal Maipu
   (Si te pide subir el PDF, PARA y avisame que lo necesito).

6. Tarifas / precios: si pide rangos, usa los de seccion 5 de la hoja NAP:
   - Destape simple: desde $45.000 CLP
   - Destape cocina/grasa: desde $55.000 CLP
   - Inspeccion camara: desde $70.000 CLP
   - Hidrojet preventivo: desde $90.000 CLP
   - Indica que cotizamos antes de empezar y emitimos boleta/factura.

7. Disponibilidad: 24/7, todos los dias.

8. Si el portal envia leads por email/SMS, configura la notificacion al telefono
   +56 9 2846 1485 y email contacto@destaperapido.cl.

9. Antes de publicar perfil: resumen + mi OK.

10. Damela URL del perfil publico.
```

---

## 4. Clasificados (Doplim, OLX, Anunico, Mundoanuncio, etc.)

```
Estamos en [SITIO CLASIFICADO]. Voy a publicar un AVISO de servicio (no es un
perfil de empresa, es un anuncio que puede vencer). Pasos:

1. Categoria: "Servicios" > "Hogar" o "Construccion/Reparaciones" segun lo que
   tenga. Si hay "Gasfiteria" o "Plomeria" especifico, usalo.

2. Titulo del aviso (max 70 caracteres):
   "Destape Alcantarillado 24h Santiago — Hidrojet y Camara CCTV"

3. Descripcion del aviso: usa la version MEDIA C de la hoja NAP. Al final agrega:
   "Llama o escribe ahora: +56 9 2846 1485 (WhatsApp 24/7).
   Web: www.destaperapido.cl"

4. Telefono de contacto: +56 9 2846 1485.

5. Ubicacion del aviso: Region Metropolitana > Santiago. Si pide comuna especifica,
   marca "Maipu" o "Todas las comunas RM".

6. Precio: marca "consultar" o deja en blanco. NO pongas precio fijo.

7. Fotos: sube la foto principal (camion en calle, seccion 7 NAP) y la foto del
   subterraneo de edificio. 2-3 fotos basta para clasificados.

8. Vigencia: marca la maxima disponible (30 dias suele ser el default).

9. Antes de publicar: resumen + mi OK.

10. Damela URL del aviso publicado y la fecha de vencimiento.
```

---

## 5. Guest post / colaboracion (envio de email a blogs)

```
Voy a contactar al editor de [NOMBRE DEL BLOG, URL] para ofrecer un guest post.
Mision: redactar el email de pitch, no el articulo todavia.

1. Encuentra en el sitio del blog el email de contacto o formulario de contacto
   (busca: contacto@, hola@, editor@, prensa@ o pagina /contacto).

2. Redacta un email usando la plantilla de la seccion 11 de la hoja NAP, pero
   ADAPTALA al tono y tematica del blog. Lee 2-3 articulos del blog antes de
   escribir para captar su estilo.

3. Propon 3 ideas de articulos que sean utiles para SU audiencia, NO promocionales.
   Buenas ideas a rotar segun el blog:
   - Hogar general: "5 senales tempranas de que tu alcantarillado va a colapsar"
   - Parcelas/condominios cerrados: "Fosa septica vs biodigestor en parcela"
   - Restaurantes/gastronomia: "Mantencion de trampas de grasa: que dice la norma"
   - Edificios/administradores: "Como evitar rebalses en edificios sin gastar fortuna"
   - Tecnico: "Hidrojet vs destape mecanico: cuando usar cada uno"

4. El link a destaperapido.cl va SOLO en la bio del final (1-2 lineas). Texto
   sugerido en seccion 12 de la hoja NAP.

5. Muestrame el email antes de enviarlo. NO lo envies aun.

6. Si el blog tiene formulario en lugar de email, llena el formulario pero
   detente antes del SUBMIT para revisar.
```

---

## 6. Prensa (Comunicae, Iberian Press, notas de prensa)

```
Estamos en [PLATAFORMA DE NOTA DE PRENSA]. Voy a publicar una nota corporativa.
Pasos:

1. Crea cuenta con email contacto@destaperapido.cl si no existe.

2. Titulo de la nota (estilo periodistico, no publicitario):
   "Destape Rapido cumple 12 anos como empresa de saneamiento 24/7 en la
   Region Metropolitana"
   (o uno mejor que propongas tu en estilo periodistico).

3. Cuerpo de la nota:
   - Lead (primer parrafo): que somos, cuanto tiempo, donde operamos.
   - Parrafo 2: que nos diferencia (3 puntos de la seccion 10 hoja NAP).
   - Parrafo 3: datos publicos (5,0/5 Google, 30+ comunas, 12 anos, flota propia).
   - Parrafo 4 ("acerca de"): version LARGA B de la hoja NAP.
   - Pie con datos de contacto del NAP.

4. Categoria de la nota: "Empresas / Servicios" o "Industria / Servicios para
   el hogar".

5. Region: Chile / Region Metropolitana.

6. Imagen destacada: camion en calle (1200x630 webp). Si el sitio pide JPG, paro
   y conviertes.

7. Hashtags / keywords: usa las primarias de la seccion 4 hoja NAP.

8. Antes de publicar: muestrame la nota completa y espera mi OK.

9. Damela URL publicada y a que medios se distribuyo (algunos plataformas listan
   los medios que recibieron la nota).
```

---

## 7. Redes sociales (Facebook, Instagram, LinkedIn, YouTube)

```
Estamos creando la pagina de empresa en [RED SOCIAL]. Pasos:

1. Tipo de pagina: "Empresa local" / "Servicios". NO "marca personal".

2. Nombre exacto: "Destape Rapido"

3. Usuario / @ (si esta disponible): @destaperapido — sino @destaperapidocl

4. Categoria principal: "Fontanero / Plumber" o "Servicios para el hogar".
   Agrega categorias secundarias: "Servicio de emergencia", "Empresa de
   saneamiento".

5. Bio / Acerca de: usa la version MEDIA B de la hoja NAP. Si hay limite de
   150 caracteres (Instagram), usa la version CORTA B.

6. Sitio web: https://www.destaperapido.cl

7. Telefono / WhatsApp: +56 9 2846 1485 (marca como WhatsApp donde se pueda).

8. Email: contacto@destaperapido.cl

9. Direccion: si es opcional, dejala vacia (somos area de servicio). Si es
   obligatoria, Maipu RM.

10. Horario: 24/7.

11. Foto de perfil: logo.png cuadrado. Foto de portada: camion en calle (recorta
    a 1200x630 si la red lo exige).

12. NO publiques aun. Solo deja creada la pagina y damela URL.
```

---

## 8. Checklist post-registro (manual, todos los sitios)

Despues de cada registro, abre `seo/backlinks-tracker.csv` y completa la fila:

- `estado` → `publicado` (o `pendiente_verificacion` si quedo esperando SMS/postal)
- `url_perfil_creado` → URL publica
- `fecha` → fecha de hoy en formato YYYY-MM-DD
- `notas` → cualquier detalle (ej: "verificacion postal en camino, llega ~14 dias")

Una vez al mes, abre el CSV y filtra por `estado=publicado`. Esos son tus backlinks
vivos. Si algun perfil cayo en `inactivo` o `removido`, vuelve a entrar y
reactivalo (los directorios suelen dar de baja perfiles sin actividad por 6 meses).

---

## 9. Orden de ataque recomendado (4 semanas)

### Semana 1 — Mapas + redes sociales (sin esto nada mas tiene sentido)
- Dia 1: crear Facebook + Instagram + LinkedIn empresa (15 min cada uno)
- Dia 2: Google Business Profile (verificacion empieza a viajar)
- Dia 3: Bing Places + Apple Business Connect + Waze
- Dia 4: actualizar hoja NAP seccion 9 con las URLs de redes
- Dia 5: subir 2-3 videos cortos a YouTube (un destape, un hidrojet, intro empresa)

### Semana 2 — Directorios CL top
Doplim, Infoisinfo, Buscatuempresa, Indizze, Mercantil, Directorio Empresas Chile,
ChileServicios, Empresas y Ejecutivos, Kom, Paginas Amarillas. ~30 min por sitio
con la extension.

### Semana 3 — Portales de servicio (los que dan leads)
Cronoshare, Habitissimo, Gasfiter.cl, Plomero.cl, Homify, Yapo. Aqui sobre todo
completa el 100% del perfil con fotos.

### Semana 4 — Guest posts + nota de prensa
- Lunes: lanzar nota de prensa via Comunicae o Iberian Press.
- Mar-Jue: enviar 5 pitches de guest post a blogs de hogar/construccion.
- Viernes: medir resultados en Google Search Console.

### Mensual
- Verificar perfiles existentes (sin caidas).
- Renovar avisos en clasificados que vencieron.
- Pedir 2-3 resenas nuevas a clientes recientes en Google Business + Trustpilot.
- Pitchear un guest post nuevo.
