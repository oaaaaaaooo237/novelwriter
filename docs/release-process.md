# Release Process

## Goal

每次版本变更后，都做到：

- 版本隔离
- 本地 Git 有记录
- 远程 GitHub 有记录
- 稳定版和开发版彼此分开

## Standard workflow

### 1. 开始新版本

在稳定版基础上创建新开发分支：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start_version.ps1 -Version 0.2.0
```

这一步会：

- 确认工作区干净
- 从 `main` 切出 `codex/v0.2.0`
- 可选推送到远程

### 2. 在开发分支完成该版本任务

只在 `codex/vX.Y.Z` 上开发，不直接在 `main` 上开发。

### 3. 准备发布

完成测试后，将开发分支合并到 `main`。

### 4. 发布正式版本

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\publish_release.ps1 -Version 0.2.0
```

这一步会：

- 检查当前位于 `main`
- 检查工作区干净
- 创建 `release/v0.2.0`
- 创建 `v0.2.0` tag
- 推送 `main`
- 推送 `release/v0.2.0`
- 推送 `v0.2.0` tag

## Mandatory checks

发布前至少确认：

- `VERSION` 已更新
- `CHANGELOG.md` 已更新
- 当前版本任务已完成
- 本地工作区干净
- `main` 已包含目标版本内容

## Current baseline

当前已经具备：

- `main`
- `release/v0.1.1`
- `codex/v0.2.0`
- `v0.1.0`
- `v0.1.1`
