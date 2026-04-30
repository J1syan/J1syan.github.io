# 我的博客

这是 J1syan 的个人博客基础框架，使用 Astro + Markdown/MDX 构建，支持文章、分类、标签、RSS、sitemap 和 GitHub Pages 自动部署。

## 本地运行

```bash
cd /home/j1syan/Documents/J1syan.github.io
npm install
npm run dev
```

本地开发地址默认是 `http://localhost:4321/`。

## 常用命令

| 命令 | 作用 |
| --- | --- |
| `npm run dev` | 启动本地开发服务 |
| `npm run build` | 构建生产版本到 `dist/` |
| `npm run preview` | 本地预览生产构建 |
| `npm run astro -- --help` | 查看 Astro CLI 帮助 |

## 写文章

在 `src/content/blog/` 下新建 Markdown 或 MDX 文件，例如：

```md
---
title: '文章标题'
description: '文章摘要'
pubDate: '2026-04-30'
category: '学习笔记'
tags: ['Java', 'Spring Cloud']
draft: false
---

这里写正文。
```

字段说明：

- `title`：文章标题
- `description`：文章摘要，用于首页、列表页、SEO 和 RSS
- `pubDate`：发布日期
- `updatedDate`：可选，更新日期
- `category`：文章分类
- `tags`：文章标签
- `draft`：设为 `true` 时不会发布

## 部署

目标仓库建议使用：

```text
J1syan/J1syan.github.io
```

首次推送：

```bash
cd /home/j1syan/Documents/J1syan.github.io
git branch -M main
git remote add origin git@github.com:J1syan/J1syan.github.io.git
git add .
git commit -m "init blog"
git push -u origin main
```

推送后，在 GitHub 仓库的 `Settings -> Pages` 中选择 `GitHub Actions` 作为部署来源。之后每次推送到 `main` 分支都会自动部署。

更详细的使用说明见 [docs/使用文档.md](docs/使用文档.md)。
