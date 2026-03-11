from __future__ import annotations

import subprocess
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from . import __version__
from .state import DEFAULT_STYLE, GENRES, ProjectInitData, initialize_project, summarize_result


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
            text='长篇网文写作助手 v0.2.0 骨架：先做项目初始化、状态落盘和 GUI 工作台。',
        ).pack(anchor='w', pady=(4, 0))

        notebook = ttk.Notebook(outer)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(16, 0))

        form_tab = ttk.Frame(notebook, padding=16)
        preview_tab = ttk.Frame(notebook, padding=16)
        release_tab = ttk.Frame(notebook, padding=16)
        notebook.add(form_tab, text='新建项目')
        notebook.add(preview_tab, text='项目预览')
        notebook.add(release_tab, text='版本规则')

        self._build_form_tab(form_tab)
        self.preview_text = self._build_text_panel(preview_tab)
        self.release_text = self._build_text_panel(release_tab)

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
        ttk.Button(action_bar, text='填充示例', command=self._fill_demo).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(action_bar, text='清空表单', command=self._reset_form).pack(side=tk.LEFT, padx=(8, 0))

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

        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', summarize_result(result))
        self.status_var.set(f'项目已创建：{result.project_dir}')
        messagebox.showinfo('创建成功', f'项目已创建：\n{result.project_dir}')

    def _render_release_notes(self) -> None:
        current_branch = detect_git_branch()
        content = (
            '版本隔离规则\n\n'
            f'- 当前 GUI 代码版本：{__version__}\n'
            f'- 当前分支：{current_branch}\n'
            '- main：稳定版本\n'
            '- release/vX.Y.Z：正式归档分支\n'
            '- codex/vX.Y.Z：开发分支\n'
            '- vX.Y.Z：正式标签\n\n'
            '发布原则：每次版本调整后，都要同时保留本地 Git 分支和远程 GitHub 分支 / tag。\n'
        )
        self.release_text.delete('1.0', tk.END)
        self.release_text.insert('1.0', content)


def detect_git_branch() -> str:
    try:
        completed = subprocess.run(
            ['git', 'branch', '--show-current'],
            check=True,
            capture_output=True,
            text=True,
        )
        branch = completed.stdout.strip()
        return branch or 'unknown'
    except Exception:  # noqa: BLE001
        return 'unknown'


def main() -> int:
    app = App()
    app.mainloop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
