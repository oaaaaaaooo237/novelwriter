# Shuangwen Pipeline

一个面向长篇网络爽文创作的项目化写作助手仓库。

当前稳定版本是 `v0.1.1`，当前开发分支是 `codex/v0.2.0`，正在推进第一个可运行 GUI 原型。

## 当前开发重点

`v0.2.0` 目标：先把 GUI 和项目初始化跑通。

这一版已经转向：

- 桌面 GUI 入口
- 可配置目标字数（`1-1000 万字`）
- 项目目录初始化
- 打开已有项目
- 项目仪表盘与卷规划概览
- 项目文档快捷入口
- 版本隔离状态面板
- 状态文件落盘
- 总纲 / 人物 / 伏笔 / 卷纲 / 剧情单元模板生成

## 版本隔离规则

从现在开始，项目采用三层版本隔离：

1. `main`
   只保留当前稳定版本。
2. `release/vX.Y.Z`
   每个正式版本都保留一个独立归档分支。
3. `codex/vX.Y.Z`
   下一个版本在独立开发分支推进，不直接污染稳定版。

配套要求：

- 每个正式版本必须有 `vX.Y.Z` tag
- 本地 Git 和远程 GitHub 都必须同步保留分支与 tag

## 当前仓库结构

```text
.
├─ .github/
├─ docs/
├─ projects/
├─ samples/
├─ scripts/
├─ src/
├─ templates/
├─ tests/
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ LICENSE
├─ README.md
├─ VERSION
└─ pyproject.toml
```

## 如何运行开发版 GUI

```powershell
$env:PYTHONPATH='src'
python -m novel_writer
```

如果后面要安装成命令，也可以使用：

```powershell
python -m pip install -e .
shuangwen-pipeline
```

## 当前文档入口

- 项目计划：[docs/project-plan.md](/D:/python%20programs/codex/novel%20writer/docs/project-plan.md)
- 需求说明：[docs/requirements.md](/D:/python%20programs/codex/novel%20writer/docs/requirements.md)
- 任务拆分：[docs/tasks.md](/D:/python%20programs/codex/novel%20writer/docs/tasks.md)
- 架构说明：[docs/architecture.md](/D:/python%20programs/codex/novel%20writer/docs/architecture.md)
- 版本归档：[docs/versioning.md](/D:/python%20programs/codex/novel%20writer/docs/versioning.md)
- 发布流程：[docs/release-process.md](/D:/python%20programs/codex/novel%20writer/docs/release-process.md)

## 版本路线

- `v0.1.1`：远程仓库重整、历史并入、当前项目重新归档
- `v0.2.0`：GUI 骨架、本地项目初始化器、基础目录结构
- `v0.3.0`：总纲/卷纲/剧情单元/伏笔账本生成强化
- `v0.4.0`：章节卡生成与进度推进
- `v0.5.0`：本地审校器与一致性检查
- `v0.6.0`：外部 LLM 接口与半自动流水线
- `v1.0.0`：可稳定使用的长篇爽文写作 GUI MVP
