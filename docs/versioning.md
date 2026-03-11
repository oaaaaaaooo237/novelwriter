# Versioning And GitHub Archive

## 1. Version strategy

项目采用语义化版本思路：

- `0.x`：快速迭代阶段，功能可能调整
- `1.0.0`：形成稳定 MVP

但从现在开始，版本管理不只是 `tag`，而是“三件套”：

- `main` 上的稳定内容
- `release/vX.Y.Z` 归档分支
- `vX.Y.Z` 正式标签

## 2. Branch roles

### `main`

只保留当前稳定版本，不做日常开发堆积。

### `codex/vX.Y.Z`

下一个版本的独立开发分支。

例如：

- `codex/v0.2.0`
- `codex/v0.3.0`

### `release/vX.Y.Z`

对应正式版本的冻结归档分支。

例如：

- `release/v0.1.1`
- `release/v0.2.0`

## 3. Tag rules

正式版本使用：

- `v0.1.1`
- `v0.2.0`
- `v1.0.0`

每个 tag 都必须对应一个已经可回放的正式状态。

## 4. Local and remote requirements

每次版本调整后，都必须同时满足：

### Local Git

- 有对应开发分支或归档分支
- 有对应 tag
- 工作区干净

### Remote GitHub

- 对应分支已推送
- 对应 tag 已推送
- `main` 与正式版本状态一致

不允许只在本地有 tag，不推远程。
也不允许只推 `main`，不推版本归档分支。

## 5. Standard release flow

1. 从 `main` 切出新的开发分支 `codex/vNext`。
2. 在开发分支完成当前版本开发。
3. 合并回 `main`。
4. 从 `main` 创建 `release/vX.Y.Z`。
5. 在 `main` 打 `vX.Y.Z` tag。
6. 推送 `main`。
7. 推送 `release/vX.Y.Z`。
8. 推送 `vX.Y.Z` tag。

## 6. Initial version map

- `v0.1.1`：远程仓库重整、历史并入、当前项目重新归档
- `v0.2.0`：GUI 骨架 + 项目初始化器
- `v0.3.0`：规划生成器
- `v0.4.0`：章节流水线
- `v0.5.0`：本地审校器
- `v0.6.0`：半自动 agent 接入
- `v1.0.0`：稳定 GUI MVP

## 7. Current repository state

当前建议结构：

- 稳定版：`main`
- 当前稳定归档：`release/v0.1.1`
- 当前开发分支：`codex/v0.2.0`
- 当前正式标签：`v0.1.1`

## 8. Automation

仓库提供两个脚本骨架：

- `scripts/start_version.ps1`
- `scripts/publish_release.ps1`

用于减少手动操作失误。
