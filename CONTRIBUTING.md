# Contributing

## Collaboration style

这个项目默认采用“版本隔离 + 版本推进”的协作方式。

在实现任何功能前，优先确认：

- 是否属于当前版本范围
- 是否在正确的开发分支上
- 是否有对应需求条目
- 是否有对应任务项
- 是否会影响已有稳定版本

## Branching

固定规则：

- `main`：当前稳定版本
- `release/vX.Y.Z`：正式版本归档分支
- `codex/vX.Y.Z`：当前开发版本分支
- `docs/<topic>`：纯文档分支

禁止直接在已经归档的 `release/*` 上继续开发。

## Release discipline

每次版本调整后，都必须同时完成：

1. 本地创建或更新对应开发分支 / 归档分支
2. 本地创建正式 tag
3. 推送远程分支
4. 推送远程 tag

也就是说，版本不是只改一个数字，而是要在本地和远程同时留下完整轨迹。

## Commit style

建议格式：

- `docs: add release isolation workflow`
- `feat: add gui project initializer`
- `feat: add plot unit planner`
- `fix: repair foreshadow ledger update`
- `chore: release v0.2.0`

## Pull request expectations

每个 PR 尽量只做一类事情：

- 需求文档调整
- 架构调整
- 单一功能实现
- 单一模块修复
- 单一版本发布准备

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
- 每个正式版本都必须保留 `release/vX.Y.Z` 和 `vX.Y.Z` tag
- `main` 只承载已经稳定的版本，不直接做日常开发

## Recommended workflow

1. 从 `main` 切出 `codex/vNext` 开发分支。
2. 在该分支完成当前版本任务。
3. 测试通过后合并到 `main`。
4. 在 `main` 上创建 `release/vX.Y.Z` 分支和 `vX.Y.Z` tag。
5. 推送 `main`、`release/vX.Y.Z` 和 `vX.Y.Z` 到远程。

## Out of scope for review

如果某个想法目前很有价值，但不属于当前版本，请先记到 `docs/tasks.md` 或后续版本，而不是直接塞进当前实现。
