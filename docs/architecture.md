# Architecture

## 1. Chosen architecture

当前阶段采用：

`本地文件系统状态层 + Python 核心引擎 + Tkinter 桌面 GUI + 后续可接 Agent/Prompt 执行层`

## 2. Why this architecture

长篇写作最重要的是长期状态，而不是单次生成能力。

当前先选 Tkinter，不是因为它最终一定最好，而是因为：

- Python 标准库自带，当前就能跑
- 能先把 GUI 工作流验证出来
- 不会被第三方依赖安装卡住
- 后续如果需要更强 GUI，再迁移到 PySide6 也更有把握

## 3. Logical modules

### Module A: project bootstrap

职责：

- 创建作品目录
- 写入基础模板
- 初始化状态文件

### Module B: story state

职责：

- 保存目标字数与规划档位
- 保存总纲
- 保存卷纲
- 保存剧情单元
- 保存人物圣经
- 保存伏笔账本
- 保存章节进度

### Module C: planning engine

职责：

- 按目标字数规划卷数与章节规模
- 控制爽点与回收节奏
- 控制单元长度与事件跨度
- 针对不同字数档位输出不同建议

### Module D: desktop GUI

职责：

- 项目创建向导
- 项目预览
- 版本规则展示
- 后续扩展为完整写作工作台

### Module E: chapter pipeline

职责：

- 定位当前章节所处卷/单元
- 输出章节卡
- 记录章节完成情况

### Module F: review engine

职责：

- 检测 AI 味
- 检测节奏问题
- 检测解释过满
- 检测结尾钩子强度

### Module G: automation adapter

职责：

- 连接外部 LLM
- 装配上下文
- 触发写作 / 审校 / 修订流程

## 4. Proposed directory shape

```text
repo/
├─ docs/
├─ projects/
├─ scripts/
├─ src/
│  └─ novel_writer/
├─ templates/
├─ tests/
└─ samples/
```

## 5. Data flow

```text
GUI form
  -> project init
  -> story state
  -> markdown templates
  -> later chapter cards
  -> draft
  -> review
  -> progress update
```

## 6. State design principles

- 一个状态只保留一个权威来源
- 结构化数据和可读文档都要有
- 长期资料与当前章节上下文分开
- GUI 只作为操作入口，不取代状态文件本身

## 7. Future evolution

后续如果 GUI 需求变复杂，优先保留现在的状态层和核心引擎，再替换界面层，而不是推翻重来。
