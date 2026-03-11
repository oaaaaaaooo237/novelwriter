# Architecture

## 1. Chosen architecture

第一阶段采用：

`文件系统状态层 + CLI 编排层 + Prompt/Agent 执行层`

## 2. Why this architecture

长篇写作最重要的是长期状态，而不是单次生成能力。

文件化架构有几个优势：

- 容易检查
- 容易版本化
- 容易恢复
- 容易给不同 agent 切上下文
- 不依赖某个对话窗口记忆

## 3. Logical modules

### Module A: project bootstrap

职责：

- 创建作品目录
- 写入基础模板
- 初始化状态文件

### Module B: story state

职责：

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

### Module D: chapter pipeline

职责：

- 定位当前章节所处卷/单元
- 输出章节卡
- 记录章节完成情况

### Module E: review engine

职责：

- 检测 AI 味
- 检测节奏问题
- 检测解释过满
- 检测结尾钩子强度

### Module F: automation adapter

职责：

- 连接外部 LLM
- 装配上下文
- 触发写作 / 审校 / 修订流程

## 4. Proposed directory shape

```text
repo/
├─ docs/
├─ src/
│  └─ novel_writer/
├─ templates/
├─ samples/
├─ tests/
└─ projects/
```

## 5. Data flow

```text
seed idea
  -> project init
  -> story bible
  -> volume outline
  -> plot units
  -> chapter card
  -> draft
  -> review
  -> progress update
  -> next chapter card
```

## 6. State design principles

- 一个状态只保留一个权威来源
- 结构化数据和可读文档都要有
- 长期资料与当前章节上下文分开
- 章节生成时只装配必要信息，防止上下文过载

## 7. Future evolution

后续如果需要 GUI，也应建立在已经稳定的状态层和 CLI 之上，而不是绕开它重做一套逻辑。
