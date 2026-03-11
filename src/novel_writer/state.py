from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

GENRES = [
    '玄幻',
    '仙侠',
    '都市',
    '都市异能',
    '末世',
    '历史',
    '科幻',
    '悬疑',
    '其他',
]

DEFAULT_STYLE = '番茄系强钩子爽文'
INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]')
VOLUME_TITLES = [
    '开篇立钩',
    '规则压制',
    '第一次反打',
    '资源争夺',
    '关系洗牌',
    '身份突破',
    '真相逼近',
    '旧账反噬',
    '局势抬升',
    '卷末清算',
    '新地图重压',
    '核心秘密外露',
    '高层博弈',
    '终局铺压',
    '终局翻盘',
]

PROFILE_RULES = [
    {
        'max_words': 100_000,
        'label': '短中篇模式',
        'focus': '强调单卷完整体验，适合 1-2 卷强钩子故事。',
        'volume_range': (1, 2),
        'unit_chapter_range': (2, 5),
        'chapter_cycle': '2-5章一个小事件，10-20章一个阶段高潮。',
    },
    {
        'max_words': 300_000,
        'label': '轻长篇模式',
        'focus': '适合快速建立世界观并保持持续追读。',
        'volume_range': (2, 4),
        'unit_chapter_range': (3, 8),
        'chapter_cycle': '3-8章一个剧情单元，15-30章一个卷内高潮。',
    },
    {
        'max_words': 600_000,
        'label': '标准网文模式',
        'focus': '适合番茄式持续追读节奏，强调中段拉扯和卷末翻盘。',
        'volume_range': (4, 6),
        'unit_chapter_range': (5, 12),
        'chapter_cycle': '5-12章一个单元，25-45章一个卷级回报。',
    },
    {
        'max_words': 1_000_000,
        'label': '长篇连载模式',
        'focus': '优先优化这一档，既能拉长线，又不至于失控。',
        'volume_range': (6, 8),
        'unit_chapter_range': (8, 18),
        'chapter_cycle': '8-18章一个单元，35-60章一个卷级高潮。',
    },
    {
        'max_words': 3_000_000,
        'label': '超长篇扩展模式',
        'focus': '适合多地图、多势力、多阶段升级，但需要更强状态管理。',
        'volume_range': (8, 12),
        'unit_chapter_range': (10, 25),
        'chapter_cycle': '10-25章一个单元，50-90章一个卷级高潮。',
    },
    {
        'max_words': 10_000_000,
        'label': '超大型连载模式',
        'focus': '支持 1000 万字以内规划，但优先保证结构可拆分与可维护。',
        'volume_range': (12, 20),
        'unit_chapter_range': (15, 30),
        'chapter_cycle': '15-30章一个单元，80-150章一个大阶段。',
    },
]


@dataclass(slots=True)
class ProjectInitData:
    title: str
    premise: str
    genre: str
    style: str
    root_dir: Path
    target_wan_words: int
    avg_chapter_words: int

    @property
    def target_words(self) -> int:
        return self.target_wan_words * 10_000


@dataclass(slots=True)
class ProjectResult:
    project_dir: Path
    state: dict[str, Any]
    created_files: list[Path]


def safe_filename(value: str) -> str:
    cleaned = INVALID_FILENAME_CHARS.sub('_', value.strip())
    cleaned = cleaned.rstrip(' .')
    return cleaned or '未命名项目'


def distribute(total: int, buckets: int) -> list[int]:
    buckets = max(buckets, 1)
    base = total // buckets
    remainder = total % buckets
    values = [base] * buckets
    for index in range(remainder):
        values[index] += 1
    return values


def planning_profile(target_words: int) -> dict[str, Any]:
    for item in PROFILE_RULES:
        if target_words <= item['max_words']:
            return dict(item)
    return dict(PROFILE_RULES[-1])


def estimate_volume_count(target_words: int, chapter_count: int, profile: dict[str, Any]) -> int:
    suggested = round(chapter_count / 40) if chapter_count > 0 else 1
    min_count, max_count = profile['volume_range']
    return max(min_count, min(max_count, suggested))


def volume_title(index: int) -> str:
    if index <= len(VOLUME_TITLES):
        return VOLUME_TITLES[index - 1]
    return f'阶段推进 {index}'


def build_volume_plan(chapter_count: int, avg_chapter_words: int, volume_count: int) -> list[dict[str, Any]]:
    chapter_slices = distribute(chapter_count, volume_count)
    volumes: list[dict[str, Any]] = []
    current_chapter = 1
    for index, current_count in enumerate(chapter_slices, start=1):
        chapter_start = current_chapter
        chapter_end = current_chapter + current_count - 1
        volumes.append(
            {
                'id': f'V{index:02d}',
                'title': f'第{index}卷：{volume_title(index)}',
                'chapter_start': chapter_start,
                'chapter_end': chapter_end,
                'chapter_count': current_count,
                'suggested_words': current_count * avg_chapter_words,
                'goal': '待填写该卷核心问题、主要反派和卷末钩子。',
            }
        )
        current_chapter = chapter_end + 1
    return volumes


def build_story_state(data: ProjectInitData, project_dir: Path) -> dict[str, Any]:
    chapter_count = math.ceil(data.target_words / data.avg_chapter_words)
    profile = planning_profile(data.target_words)
    volume_count = estimate_volume_count(data.target_words, chapter_count, profile)
    return {
        'meta': {
            'title': data.title,
            'premise': data.premise,
            'genre': data.genre,
            'style': data.style,
            'target_words': data.target_words,
            'target_wan_words': data.target_wan_words,
            'avg_chapter_words': data.avg_chapter_words,
            'estimated_chapters': chapter_count,
            'estimated_volumes': volume_count,
            'project_dir': str(project_dir),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'planning',
        },
        'planning_profile': profile,
        'progress': {
            'current_chapter': 1,
            'completed_chapters': 0,
            'completed_words': 0,
        },
        'concept': {
            'selling_point': '',
            'protagonist_hook': '',
            'world_hook': '',
            'ending_truth': '',
        },
        'volumes': build_volume_plan(chapter_count, data.avg_chapter_words, volume_count),
    }


def render_overview(state: dict[str, Any]) -> str:
    meta = state['meta']
    profile = state['planning_profile']
    return (
        f"# {meta['title']} 项目总览\n\n"
        f"- 题材：{meta['genre']}\n"
        f"- 风格：{meta['style']}\n"
        f"- 目标字数：{meta['target_words']:,} 字（{meta['target_wan_words']} 万字）\n"
        f"- 平均章字数：{meta['avg_chapter_words']:,} 字\n"
        f"- 预估章节：{meta['estimated_chapters']} 章\n"
        f"- 建议卷数：{meta['estimated_volumes']} 卷\n"
        f"- 规划档位：{profile['label']}\n"
        f"- 节奏说明：{profile['chapter_cycle']}\n"
        f"- 策略重点：{profile['focus']}\n\n"
        f"## 故事一句话\n{meta['premise']}\n"
    )


def render_master_outline(state: dict[str, Any]) -> str:
    meta = state['meta']
    profile = state['planning_profile']
    return f"""# 总纲模板

## 基本信息

- 书名：{meta['title']}
- 题材：{meta['genre']}
- 风格：{meta['style']}
- 目标字数：{meta['target_wan_words']} 万字
- 建议卷数：{meta['estimated_volumes']} 卷
- 节奏档位：{profile['label']}

## 一句话卖点

{meta['premise']}

## 主角核心执念

待填写。

## 世界核心规则

待填写。

## 核心钩子

待填写。

## 最终真相

待填写。

## 结局反证

待填写。
"""


def render_character_bible() -> str:
    return """# 人物圣经

| 名称 | 角色定位 | 想要什么 | 害怕什么 | 对主角态度 | 说话风格 | 隐藏秘密 | 未来转折 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 主角 | 核心视角 | 待填写 | 待填写 | 自身 | 待填写 | 待填写 | 待填写 |
| 核心同伴 | 长线关系 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |
| 前期压制者 | 卷内对手 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 |
"""


def render_foreshadow_ledger() -> str:
    return """# 伏笔账本

| ID | 首埋位置 | 表层解释 | 真实解释 | 预计回收卷 | 回收方式 | 当前状态 |
| --- | --- | --- | --- | --- | --- | --- |
| F01 | 第1卷前期 | 待填写 | 待填写 | 第3卷 | 待填写 | planned |
| F02 | 第1卷中段 | 待填写 | 待填写 | 第4卷 | 待填写 | planned |
| F03 | 第1卷末尾 | 待填写 | 待填写 | 第5卷 | 待填写 | planned |
"""


def render_volumes(state: dict[str, Any]) -> str:
    lines = [
        '# 卷纲建议',
        '',
        '| 卷 | 章节范围 | 建议字数 | 核心任务 | 卷末钩子 |',
        '| --- | --- | --- | --- | --- |',
    ]
    for volume in state['volumes']:
        lines.append(
            f"| {volume['title']} | {volume['chapter_start']}-{volume['chapter_end']} | {volume['suggested_words']:,} | 待填写 | 待填写 |"
        )
    return '\n'.join(lines) + '\n'


def render_plot_units(state: dict[str, Any]) -> str:
    profile = state['planning_profile']
    lines = [
        '# 剧情单元模板',
        '',
        f"建议单元跨度：{profile['unit_chapter_range'][0]}-{profile['unit_chapter_range'][1]} 章。",
        '',
    ]
    for volume in state['volumes']:
        lines.extend(
            [
                f"## {volume['title']}",
                '',
                '- 单元 1：开场立钩 / 规则压制',
                '- 单元 2：第一次反打 / 资源争夺',
                '- 单元 3：关系洗牌 / 中段反噬',
                '- 单元 4：卷末翻盘 / 下一卷钩子',
                '',
            ]
        )
    return '\n'.join(lines)


def render_chapter_card_template() -> str:
    return """# 章节卡模板

## 本章目的

待填写。

## 本章冲突

待填写。

## 信息释放

待填写。

## 伏笔推进

待填写。

## 不能说破

待填写。

## 结尾钩子

待填写。
"""


def write_project_files(project_dir: Path, state: dict[str, Any]) -> list[Path]:
    created: list[Path] = []
    for folder in [
        project_dir,
        project_dir / 'docs',
        project_dir / 'chapters',
        project_dir / 'chapter_cards',
        project_dir / 'reviews',
        project_dir / 'prompts',
    ]:
        folder.mkdir(parents=True, exist_ok=True)

    file_map = {
        project_dir / 'story_state.json': json.dumps(state, ensure_ascii=False, indent=2),
        project_dir / 'docs' / '00_项目总览.md': render_overview(state),
        project_dir / 'docs' / '01_总纲模板.md': render_master_outline(state),
        project_dir / 'docs' / '02_人物圣经.md': render_character_bible(),
        project_dir / 'docs' / '03_伏笔账本.md': render_foreshadow_ledger(),
        project_dir / 'docs' / '04_卷纲建议.md': render_volumes(state),
        project_dir / 'docs' / '05_剧情单元模板.md': render_plot_units(state),
        project_dir / 'docs' / '06_章节卡模板.md': render_chapter_card_template(),
        project_dir / 'prompts' / 'README.md': '# Prompts\n\n后续版本会在这里生成或维护 agent prompt。\n',
    }

    for path, content in file_map.items():
        path.write_text(content, encoding='utf-8')
        created.append(path)
    return created


def initialize_project(data: ProjectInitData) -> ProjectResult:
    project_name = safe_filename(data.title)
    project_dir = data.root_dir / project_name
    if project_dir.exists() and any(project_dir.iterdir()):
        raise FileExistsError(f'项目目录已存在且不为空：{project_dir}')

    state = build_story_state(data, project_dir)
    created_files = write_project_files(project_dir, state)
    return ProjectResult(project_dir=project_dir, state=state, created_files=created_files)


def summarize_result(result: ProjectResult) -> str:
    meta = result.state['meta']
    profile = result.state['planning_profile']
    lines = [
        f"项目已创建：{result.project_dir}",
        '',
        f"书名：{meta['title']}",
        f"题材：{meta['genre']}",
        f"目标字数：{meta['target_wan_words']} 万字",
        f"平均章字数：{meta['avg_chapter_words']} 字",
        f"预估章节：{meta['estimated_chapters']} 章",
        f"建议卷数：{meta['estimated_volumes']} 卷",
        f"规划档位：{profile['label']}",
        f"节奏建议：{profile['chapter_cycle']}",
        '',
        '已生成文件：',
    ]
    for path in result.created_files:
        lines.append(f'- {path}')
    return '\n'.join(lines)


def state_preview(state: dict[str, Any]) -> str:
    payload = {
        'meta': state['meta'],
        'planning_profile': state['planning_profile'],
        'volumes': state['volumes'],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def exportable_init_payload(data: ProjectInitData) -> dict[str, Any]:
    payload = asdict(data)
    payload['root_dir'] = str(data.root_dir)
    payload['target_words'] = data.target_words
    return payload
