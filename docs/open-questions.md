# Open Questions

## Product questions

1. `story state` 的权威来源是单个 JSON 文件，还是“结构化数据 + 可读 markdown 双轨”模式？
2. `v0.2.0` 是否先只做模板生成，还是直接带基础状态文件？
3. 初期是否限定单书项目，还是一开始就支持多书并行？

## Automation questions

1. 第一批接入的 LLM 是 OpenAI 兼容接口，还是先做纯 prompt 导出？
2. 自动写正文时，是否要求每章都人工确认后再推进？
3. 审校器第一版做启发式规则，还是直接接模型 reviewer？

## Writing-strategy questions

1. 默认先优化哪一类题材：玄幻、都市异能、末世，还是通用？
2. 节奏规则要不要做成可替换 profile？
3. 伏笔账本是否要区分“作者真相”和“读者表层认知”？

## Repository questions

1. 什么时候连接远程 GitHub 仓库？
2. 是否需要补充 issue labels 和 milestones 模板？
3. 是否在 v0.2.0 开始补测试骨架？
