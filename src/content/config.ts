import { defineCollection, z } from 'astro:content';

const casosCollection = defineCollection({
    type: 'content', // v2.5.0+ feature, but safe for 'markdown' content
    schema: z.object({
        title: z.string(),
        category: z.enum(['urbano', 'rural', 'empresas']),
        location: z.string(),
        image: z.string(),
        badgeColor: z.string().optional(), // Can drive this from category if cleaner
        badgeText: z.string().optional(),
        problem: z.string(),
        solution: z.string(),
        meta: z.string(), // e.g. "Tiempo: 2.5 horas"
    }),
});

export const collections = {
    'casos': casosCollection,
};
