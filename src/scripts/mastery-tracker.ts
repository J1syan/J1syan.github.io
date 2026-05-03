/**
 * Mastery Tracker — 博客算法题目"已掌握"打勾功能
 *
 * 功能：
 * 1. 扫描文章中所有 h2 标题，识别题目标题格式
 * 2. 在题目标题旁注入复选框
 * 3. 顶部显示进度条 + 隐藏已掌握按钮
 * 4. localStorage 持久化勾选状态
 */

// ============ 配置 ============

/** 匹配题目标题的正则：数字开头 或 剑指 Offer 开头 */
const PROBLEM_HEADING_RE = /^(\d+\.|剑指 Offer [\d\-]+\.)/;

/** localStorage key 前缀 */
const STORAGE_PREFIX = 'mastery:';

/** 防抖写入间隔 (ms) */
const SAVE_DEBOUNCE_MS = 300;

// ============ 状态 ============

let initialized = false;
let problemHeadings: HTMLHeadingElement[] = [];
let problemIds: string[] = [];
let checkedIds: Set<string> = new Set();
let hideMastered = false;
let toolbar: HTMLElement | null = null;
let countSpan: HTMLElement | null = null;
let fillBar: HTMLElement | null = null;
let toggleBtn: HTMLElement | null = null;

// ============ 工具函数 ============

function isProblemHeading(text: string): boolean {
	return PROBLEM_HEADING_RE.test(text.trim());
}

function getProblemId(h2: HTMLHeadingElement): string {
	// 优先使用前面的 <a id="..."> 锚点
	const prev = h2.previousElementSibling;
	if (prev && prev.tagName === 'A' && prev.id) {
		return prev.id;
	}
	// 回退：从标题文本生成 ID
	const text = h2.textContent?.trim() || '';
	const match = text.match(/^(\d+)\./);
	if (match) return 'p-' + match[1];
	const offerMatch = text.match(/^剑指 Offer ([\d\-]+)\./);
	if (offerMatch) return 'offer-' + offerMatch[1].replace(/\s*-\s*/g, '-');
	// 最终回退
	return 'prob-' + text.slice(0, 20).replace(/[^a-zA-Z0-9\u4e00-\u9fff]/g, '-');
}

function getSlug(): string {
	const path = window.location.pathname;
	const match = path.match(/\/blog\/([^/]+)/);
	return match ? match[1] : path.replace(/\/+$/, '').split('/').pop() || 'unknown';
}

function loadState(): string[] {
	try {
		const raw = localStorage.getItem(STORAGE_PREFIX + getSlug());
		return raw ? JSON.parse(raw) : [];
	} catch {
		return [];
	}
}

function saveState() {
	localStorage.setItem(
		STORAGE_PREFIX + getSlug(),
		JSON.stringify([...checkedIds])
	);
}

let saveTimer: ReturnType<typeof setTimeout> | null = null;
function debouncedSave() {
	if (saveTimer) clearTimeout(saveTimer);
	saveTimer = setTimeout(saveState, SAVE_DEBOUNCE_MS);
}

// ============ DOM 注入 ============

function injectCheckbox(h2: HTMLHeadingElement, problemId: string) {
	h2.classList.add('problem-heading');
	h2.dataset.problemId = problemId;

	// 将标题文字包裹在 span 中，方便添加删除线
	const titleSpan = document.createElement('span');
	titleSpan.className = 'problem-title';
	titleSpan.textContent = h2.textContent;

	// 创建复选框
	const label = document.createElement('label');
	label.className = 'mastery-check';

	const input = document.createElement('input');
	input.type = 'checkbox';
	input.dataset.problemId = problemId;

	const checkmark = document.createElement('span');
	checkmark.className = 'checkmark';

	label.appendChild(input);
	label.appendChild(checkmark);

	// 清空 h2，重新组装
	h2.textContent = '';
	h2.appendChild(label);
	h2.appendChild(titleSpan);

	// 事件
	input.addEventListener('change', () => {
		if (input.checked) {
			checkedIds.add(problemId);
			h2.classList.add('mastered');
		} else {
			checkedIds.delete(problemId);
			h2.classList.remove('mastered');
		}
		// 同步 section 状态
		const section = h2.closest('.problem-section');
		if (section) {
			section.classList.toggle('mastered', input.checked);
		}
		updateProgress();
		debouncedSave();
	});
}

function wrapSectionsInDivs() {
	const prose = document.querySelector('.prose');
	if (!prose) return;

	const children = Array.from(prose.children);
	let currentSection: HTMLDivElement | null = null;
	let currentIsProblem = false;

	for (const child of children) {
		if (child.tagName === 'H2' && child.classList.contains('problem-heading')) {
			// 遇到新的题目 h2，开始新的 section
			// 先把之前的 section 关闭
			currentIsProblem = true;
			currentSection = document.createElement('div');
			currentSection.className = 'problem-section';
			currentSection.dataset.problemId = (child as HTMLHeadingElement).dataset.problemId || '';
			prose.insertBefore(currentSection, child);
			currentSection.appendChild(child);
		} else if (child.tagName === 'H2' || child.tagName === 'H1') {
			// 遇到非题目的 h2/h1，关闭当前 section
			currentSection = null;
			currentIsProblem = false;
		} else if (currentIsProblem && currentSection) {
			// 属于当前题目 section
			currentSection.appendChild(child);
		}
		// 非 section 内容保持原位
	}
}

function injectToolbar(total: number) {
	const prose = document.querySelector('.prose');
	if (!prose || !prose.parentElement) return;

	toolbar = document.createElement('div');
	toolbar.id = 'mastery-toolbar';

	const progressWrap = document.createElement('div');
	progressWrap.className = 'mastery-progress';

	fillBar = document.createElement('div');
	fillBar.className = 'mastery-progress-fill';
	progressWrap.appendChild(fillBar);

	const infoRow = document.createElement('div');
	infoRow.className = 'mastery-toolbar-info';

	countSpan = document.createElement('span');
	countSpan.className = 'mastery-count';

	toggleBtn = document.createElement('button');
	toggleBtn.className = 'mastery-toggle';
	toggleBtn.textContent = '隐藏已掌握';
	toggleBtn.addEventListener('click', () => {
		hideMastered = !hideMastered;
		prose.classList.toggle('hide-mastered', hideMastered);
		if (toggleBtn) toggleBtn.textContent = hideMastered ? '显示全部' : '隐藏已掌握';
	});

	infoRow.appendChild(countSpan);
	infoRow.appendChild(toggleBtn);

	toolbar.appendChild(progressWrap);
	toolbar.appendChild(infoRow);

	prose.parentElement.insertBefore(toolbar, prose);
}

// ============ 进度更新 ============

function updateProgress() {
	if (!countSpan || !fillBar) return;
	const checked = checkedIds.size;
	const total = problemIds.length;
	countSpan.textContent = `${checked} / ${total}`;
	const pct = total > 0 ? (checked / total) * 100 : 0;
	fillBar.style.width = pct + '%';
}

// ============ 状态恢复 ============

function restoreState() {
	const saved = loadState();
	checkedIds = new Set(saved);

	for (const h2 of problemHeadings) {
		const id = h2.dataset.problemId || '';
		const input = h2.querySelector('input[type="checkbox"]') as HTMLInputElement;
		if (saved.includes(id)) {
			if (input) input.checked = true;
			h2.classList.add('mastered');
			const section = h2.closest('.problem-section');
			if (section) section.classList.add('mastered');
		}
	}
}

// ============ 主入口 ============

export function initMasteryTracker() {
	if (initialized) return;

	const prose = document.querySelector('.prose');
	if (!prose) return;

	// 1. 扫描 h2，识别题目
	const allH2s = prose.querySelectorAll('h2');
	for (const h2 of allH2s) {
		const text = h2.textContent?.trim() || '';
		if (isProblemHeading(text)) {
			const id = getProblemId(h2);
			problemHeadings.push(h2);
			problemIds.push(id);
			injectCheckbox(h2, id);
		}
	}

	// 无题目则不注入任何 UI
	if (problemHeadings.length === 0) return;

	initialized = true;

	// 2. 包裹 section
	wrapSectionsInDivs();

	// 3. 注入进度条
	injectToolbar(problemIds.length);

	// 4. 恢复状态
	restoreState();

	// 5. 更新进度
	updateProgress();
}

// 兼容密码保护文章：监听 content:revealed 事件
document.addEventListener('content:revealed', () => {
	initMasteryTracker();
});
