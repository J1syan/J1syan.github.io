---
title: '其他'
description: '记录使用 Astro 搭建博客并部署到 GitHub Pages 过程中遇到的常见问题及解决方案。'
pubDate: '2026-04-30'
category: '技术笔记'
tags: ['GitHub Pages', 'Astro', '部署', '踩坑', 'Mermaid']
---

## 博客部署问题

最近用 Astro 搭建个人博客并部署到 GitHub Pages，期间遇到了几个典型问题，逐一排查解决。如果你也在做类似的事情，希望能帮你少走弯路。

---

### 问题一：Mermaid 图表无法渲染

**现象**：文章中用 ` ```mermaid` 编写的流程图、架构图在部署后只显示为代码块，没有渲染成图形。

**原因**：Astro 的静态构建不会自动处理 Mermaid 语法，需要引入 Mermaid.js 在客户端进行渲染。

**解决方案**：在文章布局文件中添加 Mermaid 客户端渲染脚本：

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

**踩坑点**：选择器要用 `pre[data-language="mermaid"]` 而不是 `pre > code.language-mermaid`。因为 Astro 的 Shiki 语法高亮器会将 mermaid 代码块渲染为 `<pre data-language="mermaid">`，class 不在 `code` 标签上。

---

### 问题二：GitHub Pages 内置 Jekyll 构建失败

**现象**：每次 `git push` 后都会收到一封邮件，提示 "GitHub Pages 构建失败"，报错信息为 `Invalid YAML front matter in ... BlogPost.astro`。

**原因**：GitHub Pages 默认会用 Jekyll 引擎构建站点。你的 Astro 项目有自己的 GitHub Actions 工作流来构建部署，但 GitHub 内置的 Jekyll 构建也会同时触发，尝试解析 `.astro` 文件的 frontmatter 时自然会失败。

**解决方案**：

#### 1. 将 Pages 构建类型改为 workflow

通过 GitHub API 或仓库设置页面，将 `build_type` 从 `legacy` 改为 `workflow`：

```bash
# 通过 gh CLI
gh api repos/<username>/<repo>/pages -X PUT -f build_type='workflow'
```

或者在 GitHub 网页端：Settings → Pages → Build and deployment → Source 选 GitHub Actions。

#### 2. 在仓库根目录添加 `.nojekyll` 文件

这是一个空文件，告诉 GitHub 不要用 Jekyll 处理：

```bash
touch .nojekyll
```

#### 3. 在 GitHub Actions 构建步骤中添加 `.nojekyll` 到 `dist/` 目录

```yaml
jobs:
  build:
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Build with Astro
        uses: withastro/action@v6

      - name: Add .nojekyll
        run: touch dist/.nojekyll
```

**为什么两处都需要**：
- 仓库根目录的 `.nojekyll` 防止 GitHub Pages 的旧版静态站点逻辑触发 Jekyll
- `dist/` 里的 `.nojekyll` 确保 Astro 构建产物部署后不会被 Jekyll 重新处理

---

### 总结

| 问题 | 核心原因 | 解决方案 |
|---|---|---|
| Mermaid 不渲染 | 静态站点缺少客户端渲染 | 添加 Mermaid.js 脚本，用 `pre[data-language="mermaid"]` 选择器 |
| Pages 构建失败邮件 | GitHub 默认 Jekyll 与 Astro 冲突 | 加 `.nojekyll` + 设 `build_type=workflow` |

如果你的博客也是基于 Astro / Vite / Next.js 等非 Jekyll 框架部署到 GitHub Pages，大概率也会遇到同样的问题，希望这篇总结能帮到你。
