---
title: '博客部署问题'
description: '记录 Astro 博客部署到 GitHub Pages 过程中遇到的问题及解决方法。'
pubDate: '2026-04-30'
category: '其他'
tags: ['GitHub Pages', 'Astro', '部署', 'Mermaid']
---

## 问题一：Mermaid 图表无法渲染

**问题**：文章中的 ````mermaid` 代码块只显示为代码，没有渲染成图表。

**解决方法**：在文章布局文件 `src/layouts/BlogPost.astro` 中添加 Mermaid 客户端渲染脚本：

```html
<script is:inline type="module">
	(async () => {
		const blocks = document.querySelectorAll('pre[data-language="mermaid"]');
		if (blocks.length === 0) return;

		const { default: mermaid } = await import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs');

		mermaid.initialize({
			startOnLoad: false,
			theme: 'default',
			securityLevel: 'loose',
			fontFamily: 'inherit',
		});

		for (const pre of blocks) {
			const graphDef = pre.textContent.trim();
			const id = 'mermaid-' + Math.random().toString(36).substring(2, 9);

			try {
				const { svg } = await mermaid.render(id, graphDef);
				const wrapper = document.createElement('div');
				wrapper.className = 'mermaid';
				wrapper.innerHTML = svg;
				pre.replaceWith(wrapper);
			} catch (err) {
				console.warn('Mermaid render error:', err);
			}
		}
	})();
</script>
```

注意选择器使用 `pre[data-language="mermaid"]`，因为 Astro 的 Shiki 高亮会将 mermaid 代码渲染为 `pre` 标签上的 `data-language` 属性。

---

## 问题二：GitHub Pages 内置 Jekyll 构建失败，收到报错邮件

**问题**：每次 `git push` 后收到邮件提示 "GitHub Pages 构建失败"，报错 `Invalid YAML front matter in ... BlogPost.astro`。

**原因**：GitHub Pages 默认使用 Jekyll 引擎构建，会尝试解析 `.astro` 文件导致失败。

**解决方法**：

**1. 将 Pages 构建类型改为 workflow**

```bash
gh api repos/<username>/<repo>/pages -X PUT -f build_type='workflow'
```

或在 GitHub 网页端：Settings → Pages → Source 选 GitHub Actions。

**2. 在仓库根目录添加 `.nojekyll` 空文件**

```bash
touch .nojekyll
```

**3. 在 `.github/workflows/deploy.yml` 的构建步骤中添加 `.nojekyll` 到 `dist/` 目录**

```yaml
      - name: Add .nojekyll
        run: touch dist/.nojekyll
```
