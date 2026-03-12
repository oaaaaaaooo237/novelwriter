from __future__ import annotations

import os
import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Any

from . import __version__
from .state import (
    DEFAULT_STYLE,
    GENRES,
    ProjectInitData,
    build_dashboard_metrics,
    dashboard_summary_text,
    initialize_project,
    load_project_state,
    project_file_shortcuts,
    review_draft_file,
    save_project_state,
    summarize_result,
    update_story_progress,
)


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f'Shuangwen Pipeline {__version__}')
        self.geometry('1080x760')
        self.minsize(980, 700)

        self.status_var = tk.StringVar(value='准备就绪。')
        self.project_root_var = tk.StringVar(value=str((Path.cwd() / 'projects').resolve()))
        self.title_var = tk.StringVar()
        self.genre_var = tk.StringVar(value=GENRES[0])
        self.target_wan_var = tk.IntVar(value=50)
        self.chapter_words_var = tk.IntVar(value=2000)
        self.style_var = tk.StringVar(value=DEFAULT_STYLE)
        self.current_project_dir: Path | None = None
        self.current_state: dict[str, Any] | None = None

        self._build_layout()
        self._render_release_notes()

    def _build_layout(self) -> None:
        outer = ttk.Frame(self, padding=16)
        outer.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(outer)
        header.pack(fill=tk.X)

        ttk.Label(header, text='Shuangwen Pipeline', font=('Microsoft YaHei UI', 18, 'bold')).pack(anchor='w')
        ttk.Label(
            header,
            text='长篇网文写作助手 v0.4.0 开发中：开始接入章节卡生成与章节推进。',
        ).pack(anchor='w', pady=(4, 0))

        notebook = ttk.Notebook(outer)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(16, 0))

        form_tab = ttk.Frame(notebook, padding=16)
        preview_tab = ttk.Frame(notebook, padding=16)
        release_tab = ttk.Frame(notebook, padding=16)
        notebook.add(form_tab, text='新建项目')
        notebook.add(preview_tab, text='项目仪表盘')
        notebook.add(release_tab, text='版本规则')

        self._build_form_tab(form_tab)
        self._build_dashboard_tab(preview_tab)
        self._build_release_tab(release_tab)

        footer = ttk.Label(outer, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w', padding=(8, 6))
        footer.pack(fill=tk.X, pady=(12, 0))

    def _build_form_tab(self, parent: ttk.Frame) -> None:
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)

        ttk.Label(parent, text='项目工作区').grid(row=0, column=0, sticky='w', pady=6)
        ttk.Entry(parent, textvariable=self.project_root_var).grid(row=0, column=1, columnspan=2, sticky='ew', pady=6)
        ttk.Button(parent, text='选择目录', command=self._choose_root).grid(row=0, column=3, sticky='e', pady=6)

        ttk.Label(parent, text='书名').grid(row=1, column=0, sticky='w', pady=6)
        ttk.Entry(parent, textvariable=self.title_var).grid(row=1, column=1, sticky='ew', pady=6)

        ttk.Label(parent, text='题材').grid(row=1, column=2, sticky='w', padx=(20, 0), pady=6)
        ttk.Combobox(parent, textvariable=self.genre_var, values=GENRES, state='readonly').grid(
            row=1, column=3, sticky='ew', pady=6
        )

        ttk.Label(parent, text='目标字数（万字）').grid(row=2, column=0, sticky='w', pady=6)
        ttk.Spinbox(parent, from_=1, to=1000, textvariable=self.target_wan_var).grid(row=2, column=1, sticky='ew', pady=6)

        ttk.Label(parent, text='平均章字数').grid(row=2, column=2, sticky='w', padx=(20, 0), pady=6)
        ttk.Spinbox(parent, from_=500, to=10000, increment=100, textvariable=self.chapter_words_var).grid(
            row=2, column=3, sticky='ew', pady=6
        )

        ttk.Label(parent, text='风格标签').grid(row=3, column=0, sticky='w', pady=6)
        ttk.Entry(parent, textvariable=self.style_var).grid(row=3, column=1, columnspan=3, sticky='ew', pady=6)

        ttk.Label(parent, text='一句话 premise').grid(row=4, column=0, sticky='nw', pady=6)
        self.premise_text = tk.Text(parent, height=8, wrap='word')
        self.premise_text.grid(row=4, column=1, columnspan=3, sticky='nsew', pady=6)
        parent.rowconfigure(4, weight=1)

        hint = ttk.Label(
            parent,
            text='建议先填书名、题材、目标字数和一句话卖点。系统会按 1-1000 万字范围给出建议，优先优化 100 万字以下。',
            foreground='#444444',
        )
        hint.grid(row=5, column=0, columnspan=4, sticky='w', pady=(12, 16))

        action_bar = ttk.Frame(parent)
        action_bar.grid(row=6, column=0, columnspan=4, sticky='ew')
        ttk.Button(action_bar, text='创建项目', command=self._create_project).pack(side=tk.LEFT)
        ttk.Button(action_bar, text='打开已有项目', command=self._open_project).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_bar, text='填充示例', command=self._fill_demo).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_bar, text='清空表单', command=self._reset_form).pack(side=tk.LEFT, padx=(8, 0))

    def _build_dashboard_tab(self, parent: ttk.Frame) -> None:
        action_bar = ttk.Frame(parent)
        action_bar.pack(fill=tk.X)
        ttk.Button(action_bar, text='打开已有项目', command=self._open_project).pack(side=tk.LEFT)
        ttk.Button(action_bar, text='刷新当前项目', command=self._refresh_current_project).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_bar, text='刷新章节卡', command=self._refresh_chapter_pipeline).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_bar, text='推进一章', command=self._advance_chapter).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_bar, text='运行审校', command=self._run_local_review).pack(side=tk.LEFT, padx=(8, 0))

        shortcut_bar = ttk.LabelFrame(parent, text='项目快捷入口', padding=8)
        shortcut_bar.pack(fill=tk.X, pady=(12, 12))
        self.shortcut_buttons: dict[str, ttk.Button] = {}
        shortcut_groups = [
            ['项目目录', '状态文件', '项目总览', '总纲模板', '人物圣经', '伏笔账本'],
            ['卷纲建议', '剧情单元', '章节卡模板', '最近进展', '当前章节卡', '当前章节写作提示'],
            ['总导演提示', '单元规划提示', '章节卡提示', '正文写作提示', '审校提示', '审校目录'],
        ]
        for row_index, labels in enumerate(shortcut_groups):
            row = ttk.Frame(shortcut_bar)
            row.pack(fill=tk.X, pady=(0, 6) if row_index < len(shortcut_groups) - 1 else 0)
            for label in labels:
                button = ttk.Button(
                    row,
                    text=label,
                    command=lambda current_label=label: self._open_project_shortcut(current_label),
                    state=tk.DISABLED,
                )
                button.pack(side=tk.LEFT, padx=(0, 8))
                self.shortcut_buttons[label] = button

        metrics_frame = ttk.LabelFrame(parent, text='项目指标', padding=12)
        metrics_frame.pack(fill=tk.X, pady=(12, 12))

        self.dashboard_vars = {
            key: tk.StringVar(value='--')
            for key in [
                '书名',
                '题材',
                '风格',
                '目标规模',
                '平均章字数',
                '预估章节',
                '建议卷数',
                '剧情单元',
                '当前进度',
                '规划档位',
            ]
        }

        for index, key in enumerate(self.dashboard_vars):
            box = ttk.LabelFrame(metrics_frame, text=key, padding=8)
            box.grid(row=index // 3, column=index % 3, sticky='nsew', padx=6, pady=6)
            ttk.Label(box, textvariable=self.dashboard_vars[key]).pack(anchor='w')

        for column in range(3):
            metrics_frame.columnconfigure(column, weight=1)

        content_pane = ttk.Panedwindow(parent, orient=tk.VERTICAL)
        content_pane.pack(fill=tk.BOTH, expand=True)

        volume_frame = ttk.LabelFrame(content_pane, text='卷规划概览', padding=8)
        summary_frame = ttk.LabelFrame(content_pane, text='项目摘要', padding=8)
        content_pane.add(volume_frame, weight=3)
        content_pane.add(summary_frame, weight=2)

        columns = ('title', 'range', 'words', 'goal')
        self.volume_tree = ttk.Treeview(volume_frame, columns=columns, show='headings', height=10)
        headings = {
            'title': '卷名',
            'range': '章节范围',
            'words': '建议字数',
            'goal': '卷内任务',
        }
        widths = {'title': 220, 'range': 120, 'words': 110, 'goal': 420}
        for column in columns:
            self.volume_tree.heading(column, text=headings[column])
            self.volume_tree.column(column, width=widths[column], anchor='w')

        volume_scrollbar = ttk.Scrollbar(volume_frame, orient='vertical', command=self.volume_tree.yview)
        self.volume_tree.configure(yscrollcommand=volume_scrollbar.set)
        self.volume_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        volume_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.dashboard_text = self._build_text_panel(summary_frame)

    def _build_release_tab(self, parent: ttk.Frame) -> None:
        action_bar = ttk.Frame(parent)
        action_bar.pack(fill=tk.X)
        ttk.Button(action_bar, text='刷新版本状态', command=self._render_release_notes).pack(side=tk.LEFT)

        metrics_frame = ttk.LabelFrame(parent, text='版本隔离状态', padding=12)
        metrics_frame.pack(fill=tk.X, pady=(12, 12))

        self.release_vars = {
            key: tk.StringVar(value='--')
            for key in ['当前分支', '稳定分支', '归档分支', '开发分支', '版本标签', '工作区状态']
        }

        for index, key in enumerate(self.release_vars):
            box = ttk.LabelFrame(metrics_frame, text=key, padding=8)
            box.grid(row=index // 3, column=index % 3, sticky='nsew', padx=6, pady=6)
            ttk.Label(box, textvariable=self.release_vars[key]).pack(anchor='w')

        for column in range(3):
            metrics_frame.columnconfigure(column, weight=1)

        body_frame = ttk.LabelFrame(parent, text='版本说明', padding=8)
        body_frame.pack(fill=tk.BOTH, expand=True)
        self.release_text = self._build_text_panel(body_frame)

    def _build_text_panel(self, parent: ttk.Frame) -> tk.Text:
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        text = tk.Text(frame, wrap='word')
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=text.yview)
        text.configure(yscrollcommand=scrollbar.set)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        return text

    def _choose_root(self) -> None:
        path = filedialog.askdirectory(initialdir=self.project_root_var.get() or str(Path.cwd()))
        if path:
            self.project_root_var.set(path)
            self.status_var.set(f'已选择工作区：{path}')

    def _fill_demo(self) -> None:
        self.title_var.set('高压修真局')
        self.genre_var.set('玄幻')
        self.target_wan_var.set(48)
        self.chapter_words_var.set(1800)
        self.style_var.set(DEFAULT_STYLE)
        self.premise_text.delete('1.0', tk.END)
        self.premise_text.insert(
            '1.0',
            '底层少年在残酷宗门规则中靠禁忌能力翻盘，并逐步发现自己是旧时代灾厄计划留下的钥匙。',
        )
        self.status_var.set('已填充示例数据。')

    def _reset_form(self) -> None:
        self.title_var.set('')
        self.genre_var.set(GENRES[0])
        self.target_wan_var.set(50)
        self.chapter_words_var.set(2000)
        self.style_var.set(DEFAULT_STYLE)
        self.premise_text.delete('1.0', tk.END)
        self.status_var.set('表单已清空。')

    def _populate_form_from_state(self, state: dict[str, Any]) -> None:
        meta = state.get('meta', {})
        self.title_var.set(meta.get('title', ''))
        self.genre_var.set(meta.get('genre', GENRES[0]))
        self.target_wan_var.set(meta.get('target_wan_words', 50))
        self.chapter_words_var.set(meta.get('avg_chapter_words', 2000))
        self.style_var.set(meta.get('style', DEFAULT_STYLE))
        self.premise_text.delete('1.0', tk.END)
        self.premise_text.insert('1.0', meta.get('premise', ''))

    def _set_shortcuts_enabled(self, enabled: bool) -> None:
        state = tk.NORMAL if enabled else tk.DISABLED
        for button in self.shortcut_buttons.values():
            button.configure(state=state)

    def _open_project_shortcut(self, label: str) -> None:
        if self.current_project_dir is None:
            messagebox.showwarning('尚未打开项目', '请先创建或打开一个项目。')
            return

        target = project_file_shortcuts(self.current_project_dir).get(label)
        if target is None:
            messagebox.showerror('快捷入口缺失', f'未找到快捷入口：{label}')
            return
        if not target.exists():
            messagebox.showerror('文件不存在', f'目标不存在：\n{target}')
            return

        try:
            os.startfile(target)  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror('打开失败', f'无法打开目标：\n{target}\n\n{exc}')

    def _apply_dashboard_state(self, project_dir: Path, state: dict[str, Any]) -> None:
        self.current_project_dir = project_dir
        self.current_state = state
        self.project_root_var.set(str(project_dir.parent))
        self._populate_form_from_state(state)
        self._set_shortcuts_enabled(True)

        for key, value in build_dashboard_metrics(state).items():
            self.dashboard_vars[key].set(value)

        for item_id in self.volume_tree.get_children():
            self.volume_tree.delete(item_id)

        for volume in state.get('volumes', []):
            self.volume_tree.insert(
                '',
                tk.END,
                values=(
                    volume['title'],
                    f"{volume['chapter_start']}-{volume['chapter_end']}",
                    f"{volume['suggested_words']:,}",
                    volume.get('goal', '待填写'),
                ),
            )

        self.dashboard_text.delete('1.0', tk.END)
        self.dashboard_text.insert('1.0', dashboard_summary_text(state))
        self.status_var.set(f'已载入项目：{project_dir}')

    def _open_project(self) -> None:
        initial_dir = self.project_root_var.get() or str((Path.cwd() / 'projects').resolve())
        path = filedialog.askdirectory(initialdir=initial_dir)
        if not path:
            return

        project_dir = Path(path)
        try:
            state = load_project_state(project_dir)
        except FileNotFoundError as exc:
            messagebox.showerror('不是有效项目', str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror('打开失败', f'读取项目时出错：\n{exc}')
            return

        self._apply_dashboard_state(project_dir, state)
        messagebox.showinfo('打开成功', f'已载入项目：\n{project_dir}')

    def _refresh_current_project(self) -> None:
        if self.current_project_dir is None:
            messagebox.showwarning('尚未打开项目', '请先创建或打开一个项目。')
            return

        try:
            state = load_project_state(self.current_project_dir)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror('刷新失败', f'重新加载项目时出错：\n{exc}')
            return

        self._apply_dashboard_state(self.current_project_dir, state)

    def _refresh_chapter_pipeline(self) -> None:
        if self.current_project_dir is None or self.current_state is None:
            messagebox.showwarning('尚未打开项目', '请先创建或打开一个项目。')
            return

        save_project_state(self.current_project_dir, self.current_state)
        refreshed = load_project_state(self.current_project_dir)
        self._apply_dashboard_state(self.current_project_dir, refreshed)
        messagebox.showinfo('章节卡已刷新', '当前章节卡、当前写作提示和最近进展已更新。')

    def _advance_chapter(self) -> None:
        if self.current_project_dir is None or self.current_state is None:
            messagebox.showwarning('尚未打开项目', '请先创建或打开一个项目。')
            return

        chapter_number = self.current_state['progress']['current_chapter']
        summary = simpledialog.askstring('推进一章', f'请输入第{chapter_number}章的一句话摘要：', parent=self)
        if summary is None or not summary.strip():
            return

        hook = simpledialog.askstring('推进一章', '请输入本章结尾钩子：', parent=self)
        if hook is None:
            return

        words = simpledialog.askinteger('推进一章', '请输入本章实际字数（可选，默认 0）：', parent=self, minvalue=0)
        updated_state = update_story_progress(self.current_state, summary, hook, words or 0)
        save_project_state(self.current_project_dir, updated_state)
        reloaded = load_project_state(self.current_project_dir)
        self._apply_dashboard_state(self.current_project_dir, reloaded)
        messagebox.showinfo('推进成功', f'已记录第{chapter_number}章，并推进到第{reloaded["progress"]["current_chapter"]}章。')

    def _run_local_review(self) -> None:
        if self.current_project_dir is None or self.current_state is None:
            messagebox.showwarning('尚未打开项目', '请先创建或打开一个项目。')
            return

        chapters_dir = self.current_project_dir / 'chapters'
        initial_dir = str(chapters_dir if chapters_dir.exists() else self.current_project_dir)
        draft_path = filedialog.askopenfilename(
            parent=self,
            title='选择要审校的章节草稿',
            initialdir=initial_dir,
            filetypes=[('Markdown 文件', '*.md'), ('文本文件', '*.txt'), ('所有文件', '*.*')],
        )
        if not draft_path:
            return

        try:
            review_path = review_draft_file(self.current_project_dir, self.current_state, Path(draft_path))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror('审校失败', f'生成审校报告时出错：\n{exc}')
            return

        self.status_var.set(f'已生成审校报告：{review_path}')
        try:
            os.startfile(review_path)  # type: ignore[attr-defined]
        except Exception:
            pass
        messagebox.showinfo('审校完成', f'已生成审校报告：\n{review_path}')

    def _create_project(self) -> None:
        title = self.title_var.get().strip()
        premise = self.premise_text.get('1.0', tk.END).strip()
        root_dir = Path(self.project_root_var.get().strip())

        if not title:
            messagebox.showerror('缺少书名', '请先填写书名。')
            return
        if not premise:
            messagebox.showerror('缺少 premise', '请先填写一句话故事 premise。')
            return
        if not root_dir.exists():
            messagebox.showerror('目录不存在', '请先选择存在的工作区目录。')
            return

        try:
            target_wan = int(self.target_wan_var.get())
            chapter_words = int(self.chapter_words_var.get())
        except (TypeError, ValueError):
            messagebox.showerror('数值错误', '目标字数和平均章字数必须是整数。')
            return

        if target_wan < 1 or target_wan > 1000:
            messagebox.showerror('目标字数超范围', '目标字数目前支持 1-1000 万字。')
            return
        if chapter_words < 500 or chapter_words > 10000:
            messagebox.showerror('平均章字数超范围', '平均章字数建议在 500-10000 之间。')
            return

        payload = ProjectInitData(
            title=title,
            premise=premise,
            genre=self.genre_var.get().strip() or GENRES[0],
            style=self.style_var.get().strip() or DEFAULT_STYLE,
            root_dir=root_dir,
            target_wan_words=target_wan,
            avg_chapter_words=chapter_words,
        )

        try:
            result = initialize_project(payload)
        except FileExistsError as exc:
            messagebox.showerror('项目目录冲突', str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror('创建失败', str(exc))
            return

        self._apply_dashboard_state(result.project_dir, result.state)
        self.dashboard_text.insert(tk.END, '\n## 创建结果\n' + summarize_result(result))
        messagebox.showinfo('创建成功', f'项目已创建：\n{result.project_dir}')

    def _render_release_notes(self) -> None:
        current_branch = detect_git_branch()
        branches = list_git_branches()
        tags = list_git_tags()
        release_branches = [branch for branch in branches if branch.startswith('release/')]
        dev_branches = [branch for branch in branches if branch.startswith('codex/')]
        worktree_status = detect_git_worktree_status()

        self.release_vars['当前分支'].set(current_branch)
        self.release_vars['稳定分支'].set('main')
        self.release_vars['归档分支'].set('、'.join(release_branches) if release_branches else '--')
        self.release_vars['开发分支'].set('、'.join(dev_branches) if dev_branches else '--')
        self.release_vars['版本标签'].set('、'.join(tags[-5:]) if tags else '--')
        self.release_vars['工作区状态'].set(worktree_status)

        content = (
            '版本隔离规则\n\n'
            f'- 当前 GUI 代码版本：{__version__}\n'
            f'- 当前分支：{current_branch}\n'
            f"- 当前工作区：{worktree_status}\n"
            '- main：稳定版本\n'
            '- release/vX.Y.Z：正式归档分支\n'
            '- codex/vX.Y.Z：开发分支\n'
            '- vX.Y.Z：正式标签\n\n'
            f"- 已发现 release 分支：{('、'.join(release_branches) if release_branches else '无')}\n"
            f"- 已发现开发分支：{('、'.join(dev_branches) if dev_branches else '无')}\n"
            f"- 已发现标签：{('、'.join(tags) if tags else '无')}\n\n"
            '发布原则：每次版本调整后，都要同时保留本地 Git 分支和远程 GitHub 分支 / tag。\n'
        )
        self.release_text.delete('1.0', tk.END)
        self.release_text.insert('1.0', content)


def run_git_command(args: list[str]) -> str:
    try:
        completed = subprocess.run(
            ['git', *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()
    except Exception:  # noqa: BLE001
        return ''


def detect_git_branch() -> str:
    branch = run_git_command(['branch', '--show-current'])
    return branch or 'unknown'


def list_git_branches() -> list[str]:
    output = run_git_command(['branch', '--format=%(refname:short)'])
    return [line.strip() for line in output.splitlines() if line.strip()]


def list_git_tags() -> list[str]:
    output = run_git_command(['tag', '--list'])
    return [line.strip() for line in output.splitlines() if line.strip()]


def detect_git_worktree_status() -> str:
    output = run_git_command(['status', '--short'])
    return '干净' if not output else '有未提交改动'


def main() -> int:
    app = App()
    app.mainloop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
