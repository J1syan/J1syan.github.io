import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			category: z.string().default('未分类'),
			tags: z.array(z.string()).default([]),
			draft: z.boolean().default(false),
			password: z.string().optional(),
			heroImage: z.optional(image()),
		}),
});

export const collections = { blog };
