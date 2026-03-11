# Shuangwen Pipeline

一个面向长篇网络爽文创作的项目化写作助手仓库。

这个项目当前不追求“一次让 AI 写完 40-50 万字”，而是先把真正决定成败的部分做成可管理的工程系统：

- 长程规划
- 卷纲与剧情单元
- 人物一致性
- 伏笔账本
- 章节卡
- 节奏审校
- 人机协同与后续自动化
- GUI 写作工作台

## 当前阶段

当前稳定版本：`v0.1.1`

当前开发分支：`codex/v0.2.0`

当前状态：稳定版和开发版已经隔离，后续每次版本推进都同时走本地 Git 和远程 Git。

## 版本隔离规则

从现在开始，项目采用三层版本隔离：

1. `main`
   只保留当前稳定版本。
2. `release/vX.Y.Z`
   每个正式版本都保留一个独立归档分支。
3. `codex/vX.Y.Z`
   下一个版本在独立开发分支推进，不直接污染稳定版。

再配合：

- `vX.Y.Z` tag：精确标记正式发布点
- 本地 Git：保留分支和 tag
- 远程 GitHub：同步保留分支和 tag

这意味着以后每次版本调整后，都会有：

- 一个稳定主线
- 一个版本归档点
- 一个明确的开发分支
- 一个本地和远程都一致的版本记录

## 计划中的产品形态

第一阶段决定采用：

`本地文件化工作流 + Python 核心引擎 + GUI + Prompt/Agent 编排`

不先做重云端，原因是长篇写作最需要的是：

- 可追溯
- 可检查
- 可回滚
- 可分工
- 可版本化

## 仓库结构

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

## 核心目标

1. 用结构化状态代替聊天记忆。
2. 把“总纲-卷纲-剧情单元-章节卡-正文-审校”做成流水线。
3. 让 AI 只做窄任务，不直接无限自由发挥。
4. 保留人工总导演位置，保证长期节奏和人物活人感。
5. 用 GUI 承载日常使用场景。
6. 能够按版本隔离持续迭代，而不是一次性试验。

## 文档入口

- 项目计划：[docs/project-plan.md](/D:/python%20programs/codex/novel%20writer/docs/project-plan.md)
- 需求说明：[docs/requirements.md](/D:/python%20programs/codex/novel%20writer/docs/requirements.md)
- 任务拆分：[docs/tasks.md](/D:/python%20programs/codex/novel%20writer/docs/tasks.md)
- 架构说明：[docs/architecture.md](/D:/python%20programs/codex/novel%20writer/docs/architecture.md)
- 版本归档：[docs/versioning.md](/D:/python%20programs/codex/novel%20writer/docs/versioning.md)
- 发布流程：[docs/release-process.md](/D:/python%20programs/codex/novel%20writer/docs/release-process.md)
- 项目清单：[docs/project-checklist.md](/D:/python%20programs/codex/novel%20writer/docs/project-checklist.md)
- 未决问题：[docs/open-questions.md](/D:/python%20programs/codex/novel%20writer/docs/open-questions.md)

## 版本路线

- `v0.1.1`：远程仓库重整、历史并入、当前项目重新归档
- `v0.2.0`：GUI 骨架、本地项目初始化器、基础目录结构
- `v0.3.0`：总纲/卷纲/剧情单元/伏笔账本生成
- `v0.4.0`：章节卡生成与进度推进
- `v0.5.0`：本地审校器与一致性检查
- `v0.6.0`：外部 LLM 接口与半自动流水线
- `v1.0.0`：可稳定使用的长篇爽文写作 GUI MVP

## 当前开发约定

- 稳定版只在 `main`
- 正式版本都打 `tag`
- 每个正式版本都建 `release/vX.Y.Z`
- 新版本开发只在 `codex/vX.Y.Z`
- 本地提交后必须同步远程分支和远程 tag

## 下一步建议

下一轮优先进入 `v0.2.0`，开始落第一个可运行 GUI 原型：

- 新建项目向导
- 可配置目标字数
- 项目状态文件
- 总纲/人物/伏笔模板初始化
- GUI 页面骨架
