# IndexNow — destaperapido.cl

> La clave NO es secreta: se publica en el `.txt` en la raíz del sitio (estándar IndexNow).
> Sirve para avisar a Bing/Yandex (y por ellos a ChatGPT) cada vez que se publica o cambia una URL.

- **Clave:** `08b52d2c0230edeb4b9d84f3f37bbe47`
- **Archivo en el repo:** `public/08b52d2c0230edeb4b9d84f3f37bbe47.txt` (contenido = la clave)
- **URL pública tras el deploy:** `https://www.destaperapido.cl/08b52d2c0230edeb4b9d84f3f37bbe47.txt`
- **Creada:** 2026-07-07 (generada con `scripts/indexnow-ping.py --genkey` del maestro)
- **Host canónico:** `www.destaperapido.cl` (el apex hace 308 → www; usar siempre `www` en
  `--site` y en las URLs para que `host`/`keyLocation` coincidan con lo que se avisa).
  **Corregido 2026-07-17:** ese 308 valía para todas las rutas MENOS la raíz — `/` en el apex
  respondía 200 (la regla `"source": "/:path*"` de `vercel.json` no matchea `/`), así que la
  home vivía duplicada en 3 hosts. Arreglado con una regla explícita `"source": "/"`; desde
  hoy la afirmación de arriba sí es cierta también para la home.

## Estado

✅ **Operativo desde 2026-07-17.** El `.txt` está publicado y responde 200 en
`https://www.destaperapido.cl/08b52d2c0230edeb4b9d84f3f37bbe47.txt`; el primer ping real
(pasada del constructor, tarea t13) respondió 200. Ya se puede pinguear al publicar.

## Comando de ping (listo para usar tras el deploy)

```bash
# URLs puntuales (lo normal al publicar un cambio):
python3 /Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/indexnow-ping.py \
  --site https://www.destaperapido.cl \
  --key 08b52d2c0230edeb4b9d84f3f37bbe47 \
  https://www.destaperapido.cl/pagina-cambiada

# Todo el sitemap (primera vez / cambios masivos):
python3 /Users/alejandroriveracarrasco/SaSS/DIXDY/scripts/indexnow-ping.py \
  --site https://www.destaperapido.cl \
  --key 08b52d2c0230edeb4b9d84f3f37bbe47 \
  --sitemap

# Probar sin enviar: agrega --dry-run a cualquiera de los dos.
```

## Para el flujo del constructor (opcional)

Agregar a `scripts/.env.local` de este clon (no es secreto, pero el archivo sí es gitignored):

```
INDEXNOW_KEY=08b52d2c0230edeb4b9d84f3f37bbe47
SITE_URL=https://www.destaperapido.cl
```

Nota: el script del maestro lee el `.env.local` del **maestro**, no el del clon — por eso el
comando de arriba pasa `--site` y `--key` explícitos y funciona desde cualquier carpeta.
