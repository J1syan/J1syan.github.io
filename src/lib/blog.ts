import { getCollection, type CollectionEntry } from 'astro:content';

export type BlogPost = CollectionEntry<'blog'>;

export async function getPublishedPosts() {
	const posts = await getCollection('blog', ({ data }) => !data.draft);
	return sortPosts(posts);
}

export function sortPosts(posts: BlogPost[]) {
	return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

export function getCategories(posts: BlogPost[]) {
	const counts = new Map<string, number>();

	for (const post of posts) {
		const category = post.data.category || '未分类';
		counts.set(category, (counts.get(category) ?? 0) + 1);
	}

	return [...counts.entries()]
		.map(([name, count]) => ({ name, count }))
		.sort((a, b) => a.name.localeCompare(b.name, 'zh-CN'));
}

export function getTags(posts: BlogPost[]) {
	const counts = new Map<string, number>();

	for (const post of posts) {
		for (const tag of post.data.tags) {
			counts.set(tag, (counts.get(tag) ?? 0) + 1);
		}
	}

	return [...counts.entries()]
		.map(([name, count]) => ({ name, count }))
		.sort((a, b) => a.name.localeCompare(b.name, 'zh-CN'));
}

export function getPostsByCategory(posts: BlogPost[], category: string) {
	return posts.filter((post) => post.data.category === category);
}

export function getPostsByTag(posts: BlogPost[], tag: string) {
	return posts.filter((post) => post.data.tags.includes(tag));
}

export function postUrl(post: BlogPost) {
	return `/blog/${post.id}/`;
}

export function categoryUrl(category: string) {
	return `/categories/${encodeURIComponent(category)}/`;
}

export function tagUrl(tag: string) {
	return `/tags/${encodeURIComponent(tag)}/`;
}
