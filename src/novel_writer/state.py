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
STATE_FILENAME = 'story_state.json'
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
        'volume_word_range': (40_000, 70_000),
        'chapter_per_volume_range': (12, 28),
        'unit_count_range': (2, 4),
        'unit_chapter_range': (2, 5),
        'chapter_cycle': '2-5章一个小事件，10-20章一个阶段高潮。',
        'small_payoff_cycle': '1-2章一个小回报',
        'mid_payoff_cycle': '4-8章一个中回报',
        'big_payoff_cycle': '10-20章一个阶段高潮',
        'foreshadow_cycle': '开篇即埋主线钩子，每 1-2 个单元推进一次关键线索。',
    },
    {
        'max_words': 300_000,
        'label': '轻长篇模式',
        'focus': '适合快速建立世界观并保持持续追读。',
        'volume_range': (2, 4),
        'volume_word_range': (60_000, 100_000),
        'chapter_per_volume_range': (20, 38),
        'unit_count_range': (3, 5),
        'unit_chapter_range': (3, 8),
        'chapter_cycle': '3-8章一个剧情单元，15-30章一个卷内高潮。',
        'small_payoff_cycle': '1-3章一个小回报',
        'mid_payoff_cycle': '6-12章一个中回报',
        'big_payoff_cycle': '15-30章一个卷内高潮',
        'foreshadow_cycle': '每卷至少有 2 条可见伏笔，卷末推进一次重要回收。',
    },
    {
        'max_words': 600_000,
        'label': '标准网文模式',
        'focus': '适合番茄式持续追读节奏，强调中段拉扯和卷末翻盘。',
        'volume_range': (4, 6),
        'volume_word_range': (80_000, 140_000),
        'chapter_per_volume_range': (28, 55),
        'unit_count_range': (4, 6),
        'unit_chapter_range': (5, 12),
        'chapter_cycle': '5-12章一个单元，25-45章一个卷级回报。',
        'small_payoff_cycle': '2-3章一个小爽点',
        'mid_payoff_cycle': '8-15章一个中爽点',
        'big_payoff_cycle': '25-45章一个卷级翻盘',
        'foreshadow_cycle': '每卷都要新埋线并回收旧线，卷末必须抬高一层真相。',
    },
    {
        'max_words': 1_000_000,
        'label': '长篇连载模式',
        'focus': '优先优化这一档，既能拉长线，又不至于失控。',
        'volume_range': (6, 8),
        'volume_word_range': (100_000, 180_000),
        'chapter_per_volume_range': (35, 65),
        'unit_count_range': (4, 7),
        'unit_chapter_range': (8, 18),
        'chapter_cycle': '8-18章一个单元，35-60章一个卷级高潮。',
        'small_payoff_cycle': '2-4章一个局部回报',
        'mid_payoff_cycle': '10-18章一个中段翻转',
        'big_payoff_cycle': '35-60章一个卷级高潮',
        'foreshadow_cycle': '前中后段都要保有伏笔流转，重要伏笔最好跨两卷回收。',
    },
    {
        'max_words': 3_000_000,
        'label': '超长篇扩展模式',
        'focus': '适合多地图、多势力、多阶段升级，但需要更强状态管理。',
        'volume_range': (8, 12),
        'volume_word_range': (140_000, 260_000),
        'chapter_per_volume_range': (45, 90),
        'unit_count_range': (5, 8),
        'unit_chapter_range': (10, 25),
        'chapter_cycle': '10-25章一个单元，50-90章一个卷级高潮。',
        'small_payoff_cycle': '3-5章一个局部收益',
        'mid_payoff_cycle': '12-25章一个中段回报',
        'big_payoff_cycle': '50-90章一个卷级高潮',
        'foreshadow_cycle': '用地图切换和势力升级承载伏笔，避免所有线索挤在同一卷。',
    },
    {
        'max_words': 10_000_000,
        'label': '超大型连载模式',
        'focus': '支持 1000 万字以内规划，但优先保证结构可拆分与可维护。',
        'volume_range': (12, 20),
        'volume_word_range': (180_000, 350_000),
        'chapter_per_volume_range': (60, 130),
        'unit_count_range': (6, 10),
        'unit_chapter_range': (15, 30),
        'chapter_cycle': '15-30章一个单元，80-150章一个大阶段。',
        'small_payoff_cycle': '3-6章一个小回报',
        'mid_payoff_cycle': '15-30章一个中段高潮',
        'big_payoff_cycle': '80-150章一个大阶段翻盘',
        'foreshadow_cycle': '必须用多层台账管理伏笔，单卷只解决局部，不要一次说透。',
    },
]

VOLUME_ROLE_TEMPLATES = {
    'opening': {
        'focus': '开篇立钩、建立压迫、完成第一次反打。',
        'goal': '先把主角困境和舞台规则写实，再给第一次上瘾回报。',
        'ending_hook': '卷末必须把问题抬到更大的规则层或更危险的新舞台。',
    },
    'expansion': {
        'focus': '切换更大舞台，扩大资源争夺和对手层级。',
        'goal': '让主角从局部求生转为主动争取位置与资源。',
        'ending_hook': '卷末让主角拿到资格，但代价是暴露更多价值。',
    },
    'middle': {
        'focus': '通过中段拉扯制造持续追读，保持局势升级。',
        'goal': '稳步推进关系洗牌、资源争夺和中段反噬。',
        'ending_hook': '卷末要回收一部分旧线，同时打开更深一层问题。',
    },
    'truth': {
        'focus': '让前文隐线反咬主线，逼近核心秘密。',
        'goal': '把主线矛盾和真相线逐渐合流，提高终局压力。',
        'ending_hook': '卷末必须让读者意识到真正的问题比之前理解的更大。',
    },
    'finale': {
        'focus': '集中清算旧账，完成终局翻盘与关键回收。',
        'goal': '用前文积累的选择和伏笔完成最终兑现，而不是临时外挂。',
        'ending_hook': '如果还有续作空间，只能留下代价或新秩序，不再用硬拖悬念。',
    },
}

UNIT_TEMPLATE_LIBRARY = {
    'opening': [
        {'title': '开场立钩', 'purpose': '用异常事件和不公平规则抓住读者。', 'payoff': '建立主角处境与第一层信息差。'},
        {'title': '规则压制', 'purpose': '把舞台规则和主角弱势写实。', 'payoff': '让读者知道主角为什么不得不冒险。'},
        {'title': '第一次反打', 'purpose': '给出第一次成瘾式回报。', 'payoff': '局部赢一次，但暴露更大的价值。'},
        {'title': '资源争夺', 'purpose': '把一次事件拉成多章连续拉扯。', 'payoff': '让更高层势力开始关注主角。'},
        {'title': '卷末翻盘', 'purpose': '完成首卷强回报并抬高下一卷风险。', 'payoff': '局部翻盘后强开更大舞台。'},
    ],
    'expansion': [
        {'title': '新地图落地', 'purpose': '让主角在更大舞台重新站稳。', 'payoff': '立足成本抬高，旧账不清零。'},
        {'title': '资源试探', 'purpose': '围绕资源和资格制造新竞争。', 'payoff': '拿到成长条件，但会被更多人盯上。'},
        {'title': '关系编织', 'purpose': '建立新同盟、新竞争和利用关系。', 'payoff': '让阵营关系开始复杂化。'},
        {'title': '中段抬压', 'purpose': '在回报后补足压迫，提升后续翻盘价值。', 'payoff': '读者知道要翻盘，但暂时还没到。'},
        {'title': '卷末升级', 'purpose': '完成更大舞台的第一次成功立足。', 'payoff': '升级身份同时引来更深的风险。'},
    ],
    'middle': [
        {'title': '资源争夺', 'purpose': '拉长一场资源或资格博弈。', 'payoff': '把卷内矛盾变成长期拉扯。'},
        {'title': '关系洗牌', 'purpose': '调整同盟、竞争和背刺关系。', 'payoff': '改变主角可调动的筹码。'},
        {'title': '中段反噬', 'purpose': '让旧胜利被规则或旧账反噬。', 'payoff': '提升卷内高潮的情绪回报。'},
        {'title': '隐藏推进', 'purpose': '轻推真相线，保留主线行动感。', 'payoff': '让读者知道还有更深层的结构。'},
        {'title': '卷末逆袭', 'purpose': '集中兑现本卷问题的阶段性答案。', 'payoff': '回收部分旧线并抬高下卷问题。'},
    ],
    'truth': [
        {'title': '真相撕口', 'purpose': '让前文隐线开始反咬主线。', 'payoff': '揭开一层真相但不彻底说透。'},
        {'title': '高层博弈', 'purpose': '把卷内斗争抬升到更大结构。', 'payoff': '让读者看到真正敌人不只一个。'},
        {'title': '旧账爆发', 'purpose': '让人物账和势力账开始集中兑现。', 'payoff': '迫使主角做高代价选择。'},
        {'title': '终局铺压', 'purpose': '为终局前的重压和牺牲做铺垫。', 'payoff': '建立最终翻盘的必要代价。'},
    ],
    'finale': [
        {'title': '真相外露', 'purpose': '把核心秘密从边缘拉到正中。', 'payoff': '确认终局真正要回答的问题。'},
        {'title': '旧账清算', 'purpose': '把前文埋下的人物账和因果账集中兑现。', 'payoff': '终局前资源与关系完成重排。'},
        {'title': '终局翻盘', 'purpose': '让前文长期积累的选择和伏笔一起结算。', 'payoff': '完成主线最大的情绪回报。'},
        {'title': '结局反证', 'purpose': '证明主角赢的不只是战斗结果。', 'payoff': '交代新秩序或结局代价。'},
    ],
}


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


def average_range(values: tuple[int, int]) -> float:
    return (values[0] + values[1]) / 2


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


def tapered_weights(count: int, *, head_bias: float = 0.92, tail_bias: float = 0.95) -> list[float]:
    if count <= 1:
        return [1.0]

    midpoint = (count - 1) / 2
    weights: list[float] = []
    for index in range(count):
        distance = abs(index - midpoint)
        normalized = 1 - (distance / max(midpoint, 1))
        weights.append(1.0 + normalized * 0.28)

    weights[0] *= head_bias
    weights[-1] *= tail_bias
    return weights


def weighted_distribute(total: int, weights: list[float], minimum: int = 1) -> list[int]:
    if not weights:
        return []
    if total <= 0:
        return [0] * len(weights)

    if total < minimum * len(weights):
        values = [0] * len(weights)
        for index in range(total):
            values[index % len(weights)] += 1
        return values

    total_weight = sum(weights) or len(weights)
    raw_values = [(total * weight) / total_weight for weight in weights]
    counts = [max(minimum, int(math.floor(value))) for value in raw_values]
    current = sum(counts)

    if current < total:
        remainders = sorted(
            ((raw_values[index] - counts[index], index) for index in range(len(weights))),
            reverse=True,
        )
        pointer = 0
        while current < total:
            _, index = remainders[pointer % len(remainders)]
            counts[index] += 1
            current += 1
            pointer += 1
    elif current > total:
        candidates = sorted(range(len(counts)), key=lambda index: counts[index], reverse=True)
        pointer = 0
        while current > total and candidates:
            index = candidates[pointer % len(candidates)]
            if counts[index] > minimum:
                counts[index] -= 1
                current -= 1
            pointer += 1
            if pointer > len(candidates) * 4:
                break

    return counts


def planning_profile(target_words: int) -> dict[str, Any]:
    for item in PROFILE_RULES:
        if target_words <= item['max_words']:
            return dict(item)
    return dict(PROFILE_RULES[-1])


def estimate_volume_count(target_words: int, chapter_count: int, profile: dict[str, Any]) -> int:
    word_based = round(target_words / average_range(profile['volume_word_range'])) if target_words > 0 else 1
    chapter_based = round(chapter_count / average_range(profile['chapter_per_volume_range'])) if chapter_count > 0 else 1
    suggested = round((word_based + chapter_based) / 2) if (word_based or chapter_based) else 1
    min_count, max_count = profile['volume_range']
    return clamp(max(1, suggested), min_count, max_count)


def estimate_unit_count(chapter_count: int, profile: dict[str, Any]) -> int:
    min_units, max_units = profile['unit_count_range']
    min_chapters_per_unit = max(profile['unit_chapter_range'][0], 1)
    max_reasonable = max(1, chapter_count // min_chapters_per_unit) if chapter_count else 1
    max_units = min(max_units, max_reasonable)
    avg_unit_chapters = average_range(profile['unit_chapter_range'])
    suggested = round(chapter_count / avg_unit_chapters) if chapter_count > 0 else 1
    lower_bound = min_units if chapter_count >= min_units * min_chapters_per_unit else 1
    upper_bound = max(1, max_units)
    return clamp(max(1, suggested), min(lower_bound, upper_bound), upper_bound)


def volume_title(index: int) -> str:
    if index <= len(VOLUME_TITLES):
        return VOLUME_TITLES[index - 1]
    return f'阶段推进 {index}'


def volume_role(index: int, total: int) -> str:
    if total <= 1:
        return 'finale'
    if index == 1:
        return 'opening'
    if index == total:
        return 'finale'
    if total >= 4 and index == total - 1:
        return 'truth'
    if total >= 5 and index == 2:
        return 'expansion'
    return 'middle'


def build_volume_plan(chapter_count: int, avg_chapter_words: int, volume_count: int, profile: dict[str, Any]) -> list[dict[str, Any]]:
    chapter_slices = weighted_distribute(chapter_count, tapered_weights(volume_count), minimum=1)
    volumes: list[dict[str, Any]] = []
    current_chapter = 1
    for index, current_count in enumerate(chapter_slices, start=1):
        chapter_start = current_chapter
        chapter_end = current_chapter + current_count - 1
        role = volume_role(index, volume_count)
        role_template = VOLUME_ROLE_TEMPLATES[role]
        unit_count = estimate_unit_count(current_count, profile)
        volumes.append(
            {
                'id': f'V{index:02d}',
                'title': f'第{index}卷：{volume_title(index)}',
                'role': role,
                'chapter_start': chapter_start,
                'chapter_end': chapter_end,
                'chapter_count': current_count,
                'suggested_words': current_count * avg_chapter_words,
                'suggested_unit_count': unit_count,
                'focus': role_template['focus'],
                'goal': role_template['goal'],
                'ending_hook': role_template['ending_hook'],
            }
        )
        current_chapter = chapter_end + 1
    return volumes


def build_plot_units(volumes: list[dict[str, Any]], profile: dict[str, Any]) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for volume in volumes:
        role = volume['role']
        templates = UNIT_TEMPLATE_LIBRARY[role]
        unit_count = volume['suggested_unit_count']
        slices = weighted_distribute(volume['chapter_count'], tapered_weights(unit_count, head_bias=0.9, tail_bias=1.0), minimum=1)
        current_chapter = volume['chapter_start']

        for index, current_count in enumerate(slices, start=1):
            template = templates[min(index - 1, len(templates) - 1)]
            chapter_start = current_chapter
            chapter_end = current_chapter + current_count - 1
            units.append(
                {
                    'id': f"{volume['id']}-U{index:02d}",
                    'volume_id': volume['id'],
                    'volume_title': volume['title'],
                    'role': role,
                    'title': template['title'],
                    'purpose': template['purpose'],
                    'payoff': template['payoff'],
                    'chapter_start': chapter_start,
                    'chapter_end': chapter_end,
                    'chapter_count': current_count,
                    'target_words': current_count * round(volume['suggested_words'] / max(volume['chapter_count'], 1)),
                }
            )
            current_chapter = chapter_end + 1
    return units


def build_story_state(data: ProjectInitData, project_dir: Path) -> dict[str, Any]:
    chapter_count = math.ceil(data.target_words / data.avg_chapter_words)
    profile = planning_profile(data.target_words)
    volume_count = estimate_volume_count(data.target_words, chapter_count, profile)
    volumes = build_volume_plan(chapter_count, data.avg_chapter_words, volume_count, profile)
    plot_units = build_plot_units(volumes, profile)
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
            'estimated_plot_units': len(plot_units),
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
        'volumes': volumes,
        'plot_units': plot_units,
    }


def state_file_path(project_dir: Path) -> Path:
    return project_dir / STATE_FILENAME


def load_project_state(project_dir: Path) -> dict[str, Any]:
    path = state_file_path(project_dir)
    if not path.exists():
        raise FileNotFoundError(f'未找到项目状态文件：{path}')

    state = json.loads(path.read_text(encoding='utf-8'))
    state.setdefault('meta', {})
    state.setdefault('planning_profile', {})
    state.setdefault('progress', {})
    state.setdefault('volumes', [])
    state.setdefault('plot_units', [])
    state['meta'].setdefault('project_dir', str(project_dir))
    state['progress'].setdefault('current_chapter', 1)
    state['progress'].setdefault('completed_chapters', 0)
    state['progress'].setdefault('completed_words', 0)
    state['meta'].setdefault('estimated_plot_units', len(state['plot_units']))
    return state


def project_file_shortcuts(project_dir: Path) -> dict[str, Path]:
    docs_dir = project_dir / 'docs'
    return {
        '项目目录': project_dir,
        '状态文件': state_file_path(project_dir),
        '项目总览': docs_dir / '00_项目总览.md',
        '总纲模板': docs_dir / '01_总纲模板.md',
        '人物圣经': docs_dir / '02_人物圣经.md',
        '伏笔账本': docs_dir / '03_伏笔账本.md',
        '卷纲建议': docs_dir / '04_卷纲建议.md',
        '剧情单元': docs_dir / '05_剧情单元模板.md',
        '章节卡模板': docs_dir / '06_章节卡模板.md',
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
        f"- 预估剧情单元：{meta.get('estimated_plot_units', len(state.get('plot_units', [])))} 个\n"
        f"- 规划档位：{profile['label']}\n"
        f"- 节奏说明：{profile['chapter_cycle']}\n"
        f"- 策略重点：{profile['focus']}\n\n"
        f"## 默认节奏\n"
        f"- 小回报：{profile['small_payoff_cycle']}\n"
        f"- 中回报：{profile['mid_payoff_cycle']}\n"
        f"- 大回报：{profile['big_payoff_cycle']}\n"
        f"- 伏笔节奏：{profile['foreshadow_cycle']}\n\n"
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
- 预估剧情单元：{meta.get('estimated_plot_units', len(state.get('plot_units', [])))}
- 节奏档位：{profile['label']}

## 一句话卖点

{meta['premise']}

## 默认节奏

- 小回报：{profile['small_payoff_cycle']}
- 中回报：{profile['mid_payoff_cycle']}
- 大回报：{profile['big_payoff_cycle']}
- 伏笔节奏：{profile['foreshadow_cycle']}

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
        '| 卷 | 角色 | 章节范围 | 单元数 | 建议字数 | 核心任务 | 卷末钩子 |',
        '| --- | --- | --- | --- | --- | --- | --- |',
    ]
    for volume in state['volumes']:
        lines.append(
            f"| {volume['title']} | {volume['role']} | {volume['chapter_start']}-{volume['chapter_end']} | {volume['suggested_unit_count']} | {volume['suggested_words']:,} | {volume['goal']} | {volume['ending_hook']} |"
        )
    return '\n'.join(lines) + '\n'


def render_plot_units(state: dict[str, Any]) -> str:
    lines = [
        '# 剧情单元规划',
        '',
        '| 单元 | 所属卷 | 章节范围 | 章节数 | 单元目的 | 阶段回报 |',
        '| --- | --- | --- | --- | --- | --- |',
        '',
    ]
    for unit in state.get('plot_units', []):
        lines.append(
            f"| {unit['id']} {unit['title']} | {unit['volume_title']} | {unit['chapter_start']}-{unit['chapter_end']} | {unit['chapter_count']} | {unit['purpose']} | {unit['payoff']} |"
        )
    return '\n'.join(lines) + '\n'


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


def build_dashboard_metrics(state: dict[str, Any]) -> dict[str, str]:
    meta = state['meta']
    profile = state['planning_profile']
    progress = state['progress']
    return {
        '书名': meta.get('title', '--'),
        '题材': meta.get('genre', '--'),
        '风格': meta.get('style', '--'),
        '目标规模': f"{meta.get('target_wan_words', '--')} 万字",
        '平均章字数': f"{meta.get('avg_chapter_words', '--')} 字",
        '预估章节': f"{meta.get('estimated_chapters', '--')} 章",
        '建议卷数': f"{meta.get('estimated_volumes', '--')} 卷",
        '剧情单元': f"{meta.get('estimated_plot_units', len(state.get('plot_units', [])))} 个",
        '当前进度': f"第{progress.get('current_chapter', 1)}章 / 已完成 {progress.get('completed_chapters', 0)} 章",
        '规划档位': profile.get('label', '--'),
    }


def dashboard_summary_text(state: dict[str, Any]) -> str:
    meta = state['meta']
    profile = state['planning_profile']
    progress = state['progress']
    lines = [
        f"# {meta.get('title', '未命名项目')} 项目仪表盘",
        '',
        "## 基础信息",
        f"- 题材：{meta.get('genre', '--')}",
        f"- 风格：{meta.get('style', '--')}",
        f"- 目标字数：{meta.get('target_words', 0):,} 字（{meta.get('target_wan_words', '--')} 万字）",
        f"- 平均章字数：{meta.get('avg_chapter_words', '--')} 字",
        f"- 预估章节：{meta.get('estimated_chapters', '--')} 章",
        f"- 建议卷数：{meta.get('estimated_volumes', '--')} 卷",
        f"- 预估剧情单元：{meta.get('estimated_plot_units', len(state.get('plot_units', [])))} 个",
        f"- 创建时间：{meta.get('created_at', '--')}",
        '',
        "## 当前进度",
        f"- 当前章节：第{progress.get('current_chapter', 1)}章",
        f"- 已完成章节：{progress.get('completed_chapters', 0)}章",
        f"- 已完成字数：{progress.get('completed_words', 0):,} 字",
        '',
        "## 规划档位",
        f"- 档位名称：{profile.get('label', '--')}",
        f"- 节奏建议：{profile.get('chapter_cycle', '--')}",
        f"- 策略重点：{profile.get('focus', '--')}",
        f"- 小回报：{profile.get('small_payoff_cycle', '--')}",
        f"- 中回报：{profile.get('mid_payoff_cycle', '--')}",
        f"- 大回报：{profile.get('big_payoff_cycle', '--')}",
        f"- 伏笔节奏：{profile.get('foreshadow_cycle', '--')}",
        '',
        "## 故事一句话",
        meta.get('premise', '待填写。'),
        '',
        "## 当前卷规划预览",
    ]
    for volume in state.get('volumes', [])[:6]:
        lines.append(
            f"- {volume['title']}：{volume['chapter_start']}-{volume['chapter_end']} 章，建议 {volume['suggested_words']:,} 字"
        )
    if len(state.get('volumes', [])) > 6:
        lines.append(f"- 其余 {len(state['volumes']) - 6} 卷可在卷规划表中继续查看。")
    return '\n'.join(lines) + '\n'


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
        state_file_path(project_dir): json.dumps(state, ensure_ascii=False, indent=2),
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
