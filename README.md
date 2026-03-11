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

## 当前阶段

当前版本：`v0.1.0`

当前状态：项目策划与仓库骨架阶段

这一版先把正式项目需要的文档、版本节奏、任务拆解、需求边界和 GitHub 协作约定落地，方便后续按版本推进实现。

## 为什么先做成项目

长篇网文创作失败，通常不是因为单章写不出来，而是因为：

- 没有长线规划
- 伏笔没有账本
- 爽点和压迫节奏不稳定
- 每章都写成闭环短篇
- 人物动机和关系线逐渐漂移

所以这个项目的第一目标不是“写一章”，而是“建立一个可持续产出 200-300 章的写作流水线”。

## 计划中的产品形态

第一阶段决定采用：

`本地文件化工作流 + Python CLI + Prompt/Agent 编排`

不先做重前端，原因是长篇写作最需要的是：

- 可追溯
- 可检查
- 可回滚
- 可分工
- 可版本化

## 仓库结构

```text
.
├─ .github/
│  ├─ ISSUE_TEMPLATE/
│  └─ PULL_REQUEST_TEMPLATE.md
├─ docs/
│  ├─ architecture.md
│  ├─ project-checklist.md
│  ├─ project-plan.md
│  ├─ requirements.md
│  ├─ tasks.md
│  └─ versioning.md
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ README.md
└─ VERSION
```

## 核心目标

1. 用结构化状态代替聊天记忆。
2. 把“总纲-卷纲-剧情单元-章节卡-正文-审校”做成流水线。
3. 让 AI 只做窄任务，不直接无限自由发挥。
4. 保留人工总导演位置，保证长期节奏和人物活人感。
5. 能够按 GitHub 版本持续迭代，而不是一次性试验。

## 文档入口

- 项目计划：[docs/project-plan.md](/D:/python%20programs/codex/novel%20writer/docs/project-plan.md)
- 需求说明：[docs/requirements.md](/D:/python%20programs/codex/novel%20writer/docs/requirements.md)
- 任务拆分：[docs/tasks.md](/D:/python%20programs/codex/novel%20writer/docs/tasks.md)
- 架构说明：[docs/architecture.md](/D:/python%20programs/codex/novel%20writer/docs/architecture.md)
- 版本归档：[docs/versioning.md](/D:/python%20programs/codex/novel%20writer/docs/versioning.md)
- 项目清单：[docs/project-checklist.md](/D:/python%20programs/codex/novel%20writer/docs/project-checklist.md)

## 版本路线

- `v0.1.0`：项目策划、需求、任务、版本规范、GitHub 骨架
- `v0.2.0`：本地项目初始化器与基础目录结构
- `v0.3.0`：总纲/卷纲/剧情单元/伏笔账本生成
- `v0.4.0`：章节卡生成与进度推进
- `v0.5.0`：本地审校器与一致性检查
- `v0.6.0`：外部 LLM 接口与半自动流水线
- `v1.0.0`：可稳定使用的长篇爽文写作 MVP

## 现在可以怎么用

当前这版最适合做两件事：

1. 作为项目蓝图确认方向。
2. 作为实现阶段的任务依据，逐版本推进。

## 下一步建议

下一轮优先进入 `v0.2.0`，开始落第一个可运行原型：

- `init` 项目
- 生成基础资料目录
- 写入总纲模板、人物模板、伏笔模板
- 让仓库从“计划”进入“可操作”
