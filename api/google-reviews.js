/**
 * Vercel serverless: trae reseñas reales desde Google.
 *
 * Soporta dos modos según las env vars que configures:
 *   A) Service Area Business (lo más común para Destape Rápido):
 *      GOOGLE_PLACE_CID       = "14836082239400716505"     (CID numérico)
 *      → usa la Places API legacy con `cid`
 *
 *   B) Negocio con dirección física pública:
 *      GOOGLE_PLACE_ID        = "ChIJ..."
 *      → usa la Places API (New)
 *
 *   C) Cualquiera de los dos modos requiere:
 *      GOOGLE_PLACES_API_KEY  (Google Cloud → APIs → Places API + Places API (New) habilitadas)
 *
 *   D) Opcional, para forzar refresh manual:
 *      REVIEWS_REFRESH_TOKEN  = un string secreto (ej: "rivera-2026-Z9pK")
 *      → permite invalidar el cache abriendo /api/google-reviews?refresh=<TOKEN>
 *
 * Cache: 7 días (CDN edge + memoria del lambda).
 * Para refrescar antes: visita /api/google-reviews?refresh=<TOKEN> en el browser.
 */

const CACHE_TTL_MS = 7 * 24 * 60 * 60 * 1000; // 7 días
const CACHE_TTL_SEC = 7 * 24 * 60 * 60;       // mismo, en segundos para Cache-Control
let cache = { data: null, expiresAt: 0 };

export default async function handler(req, res) {
  // Detectar refresh manual con token
  const url = new URL(req.url || '/', `http://${req.headers.host || 'x'}`);
  const refreshParam = url.searchParams.get('refresh');
  const refreshToken = process.env.REVIEWS_REFRESH_TOKEN;
  const isAuthorizedRefresh =
    refreshParam && refreshToken && refreshParam === refreshToken;

  if (isAuthorizedRefresh) {
    cache = { data: null, expiresAt: 0 };
    // Si pasaron token: no cachear esta respuesta en CDN
    res.setHeader('Cache-Control', 'no-store');
  } else {
    // Cache normal en CDN edge (sirve sin tocar el lambda durante 7 días)
    res.setHeader(
      'Cache-Control',
      `public, s-maxage=${CACHE_TTL_SEC}, stale-while-revalidate=86400`,
    );
  }

  // Si está pidiendo refresh sin token válido → 403 (para que sepan que el token está mal)
  if (refreshParam && !isAuthorizedRefresh) {
    return res.status(403).json({ error: 'Invalid refresh token' });
  }

  if (cache.data && Date.now() < cache.expiresAt) {
    return res.status(200).json({ ...cache.data, cached: true });
  }

  const apiKey = process.env.GOOGLE_PLACES_API_KEY;
  const placeCid = process.env.GOOGLE_PLACE_CID;
  const placeId = process.env.GOOGLE_PLACE_ID;

  if (!apiKey) {
    return res.status(500).json({ error: 'Missing GOOGLE_PLACES_API_KEY env var' });
  }

  if (!placeCid && !placeId) {
    return res.status(500).json({
      error: 'Missing GOOGLE_PLACE_CID or GOOGLE_PLACE_ID env var',
    });
  }

  try {
    const payload = placeCid
      ? await fetchByCid(placeCid, apiKey)
      : await fetchByPlaceId(placeId, apiKey);

    cache = { data: payload, expiresAt: Date.now() + CACHE_TTL_MS };
    return res.status(200).json(payload);
  } catch (err) {
    console.error('Reviews handler error:', err);
    return res.status(err.status || 500).json({
      error: 'Cannot fetch reviews',
      message: err.message,
    });
  }
}

/* ──────────────────────────── Modo A: CID (Service Area Business) ─────────────────────────── */

async function fetchByCid(cid, apiKey) {
  const url = new URL('https://maps.googleapis.com/maps/api/place/details/json');
  url.searchParams.set('cid', cid);
  url.searchParams.set(
    'fields',
    'name,rating,user_ratings_total,reviews,url',
  );
  url.searchParams.set('language', 'es');
  url.searchParams.set('reviews_sort', 'most_relevant');
  url.searchParams.set('key', apiKey);

  const r = await fetch(url.toString());
  if (!r.ok) {
    const body = await r.text();
    const err = new Error(`Places legacy API HTTP ${r.status}: ${body}`);
    err.status = 502;
    throw err;
  }

  const json = await r.json();
  if (json.status !== 'OK') {
    const err = new Error(
      `Places legacy API status ${json.status}: ${json.error_message || ''}`,
    );
    err.status = 502;
    throw err;
  }

  const result = json.result || {};
  const reviews = (result.reviews || []).map((rev) => ({
    author: rev.author_name || 'Usuario de Google',
    photo: rev.profile_photo_url || null,
    rating: rev.rating || 5,
    text: rev.text || '',
    relativeTime: rev.relative_time_description || '',
    publishTime: rev.time ? new Date(rev.time * 1000).toISOString() : null,
  }));

  return {
    placeName: result.name || 'Destape Rápido',
    rating: result.rating || null,
    total: result.user_ratings_total || 0,
    mapsUrl: result.url || null,
    reviews,
  };
}

/* ──────────────────────────── Modo B: Place ID (Places API New) ───────────────────────────── */

async function fetchByPlaceId(placeId, apiKey) {
  const url = `https://places.googleapis.com/v1/places/${encodeURIComponent(placeId)}`;
  const fieldMask = [
    'id',
    'displayName',
    'rating',
    'userRatingCount',
    'reviews',
    'googleMapsUri',
  ].join(',');

  const r = await fetch(`${url}?languageCode=es`, {
    headers: {
      'X-Goog-Api-Key': apiKey,
      'X-Goog-FieldMask': fieldMask,
    },
  });

  if (!r.ok) {
    const body = await r.text();
    const err = new Error(`Places API (New) HTTP ${r.status}: ${body}`);
    err.status = 502;
    throw err;
  }

  const data = await r.json();
  const reviews = (data.reviews || []).map((rev) => ({
    author: rev.authorAttribution?.displayName || 'Usuario de Google',
    photo: rev.authorAttribution?.photoUri || null,
    rating: rev.rating || 5,
    text: rev.text?.text || '',
    relativeTime: rev.relativePublishTimeDescription || '',
    publishTime: rev.publishTime || null,
  }));

  return {
    placeName: data.displayName?.text || 'Destape Rápido',
    rating: data.rating || null,
    total: data.userRatingCount || 0,
    mapsUrl: data.googleMapsUri || null,
    reviews,
  };
}
