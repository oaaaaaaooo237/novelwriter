# Contributing

## Collaboration style

这个项目默认采用“计划先行，版本推进”的协作方式。

在实现任何功能前，优先确认：

- 是否属于当前版本范围
- 是否有对应需求条目
- 是否有对应任务项
- 是否会影响已有版本边界

## Branching

建议使用以下分支命名：

- `main`：稳定主干
- `codex/<topic>`：功能分支
- `docs/<topic>`：纯文档分支

## Commit style

建议格式：

- `docs: add v0.1 planning docs`
- `feat: add project scaffold generator`
- `refactor: simplify chapter card builder`
- `fix: repair foreshadow ledger update`

## Pull request expectations

每个 PR 尽量只做一类事情：

- 需求文档调整
- 架构调整
- 单一功能实现
- 单一模块修复

PR 描述里建议说明：

- 改动目的
- 所属版本
- 对应任务
- 风险点
- 后续工作

## Version discipline

- 不跨版本偷偷塞功能
- 未写进需求或任务的改动，先补文档再实现
- 每个版本结束前更新 `CHANGELOG.md`
- 重要里程碑打 tag

## Out of scope for review

如果某个想法目前很有价值，但不属于当前版本，请先记到 `docs/tasks.md` 或后续版本，而不是直接塞进当前实现。
