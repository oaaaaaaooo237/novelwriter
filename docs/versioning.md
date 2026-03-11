# Versioning And GitHub Archive

## 1. Version strategy

项目采用语义化版本思路：

- `0.x`：快速迭代阶段，功能可能调整
- `1.0.0`：形成稳定 MVP

推荐节奏：

- 文档基建版本也记入 changelog
- 每个里程碑结束时打 tag
- 不同版本之间必须有明确边界

## 2. Initial version map

- `v0.1.0`：策划与仓库基建
- `v0.2.0`：项目初始化器
- `v0.3.0`：规划生成器
- `v0.4.0`：章节流水线
- `v0.5.0`：本地审校器
- `v0.6.0`：半自动 agent 接入
- `v1.0.0`：稳定 MVP

## 3. GitHub archive rules

### Branch

- 默认主分支：`main`
- 功能分支：`codex/<topic>`
- 文档分支：`docs/<topic>`

### Tag

使用如下格式：

- `v0.1.0`
- `v0.2.0`
- `v1.0.0`

### Release notes

每次 release 至少包含：

- 本版本目标
- 完成内容
- 已知限制
- 下一版本重点

## 4. Commit discipline

建议在 GitHub 上按小步提交：

- `docs: bootstrap v0.1 project docs`
- `feat: add project initializer`
- `feat: add plot unit planner`
- `feat: add chapter card generator`
- `feat: add review engine`

## 5. Recommended release process

1. 在当前版本范围内完成任务。
2. 更新 `CHANGELOG.md`。
3. 确认 `VERSION` 文件。
4. 提交变更。
5. 创建 git tag。
6. 推送代码与 tag 到 GitHub。
7. 在 GitHub Release 页面填写版本说明。

## 6. Notes for current environment

当前工作区可以先完成本地 Git 初始化、版本文档和本地 tag。

真正推送到 GitHub 仍然需要：

- 远程仓库地址
- 可用认证
- 用户确认是否要推送
