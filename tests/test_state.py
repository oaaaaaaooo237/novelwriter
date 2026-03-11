import shutil
import unittest
import uuid
from pathlib import Path

from novel_writer.state import (
    ProjectInitData,
    build_story_state,
    dashboard_summary_text,
    initialize_project,
    load_project_state,
    project_file_shortcuts,
)


class ProjectInitTests(unittest.TestCase):
    def test_initialize_project_creates_files_and_state(self) -> None:
        projects_root = Path('projects').resolve()
        projects_root.mkdir(parents=True, exist_ok=True)
        title = f"测试项目_{uuid.uuid4().hex[:8]}"
        project_dir = projects_root / title

        try:
            payload = ProjectInitData(
                title=title,
                premise='一个少年在高压宗门里翻盘并逐步接近大秘密。',
                genre='玄幻',
                style='番茄系强钩子爽文',
                root_dir=projects_root,
                target_wan_words=48,
                avg_chapter_words=1800,
            )

            result = initialize_project(payload)

            self.assertTrue((result.project_dir / 'story_state.json').exists())
            self.assertTrue((result.project_dir / 'docs' / '01_总纲模板.md').exists())
            self.assertTrue((result.project_dir / 'docs' / '04_卷纲建议.md').exists())
            self.assertTrue((result.project_dir / 'prompts' / '01_总导演提示.md').exists())
            self.assertTrue((result.project_dir / 'prompts' / '05_审校提示.md').exists())
            self.assertEqual(result.state['meta']['target_wan_words'], 48)
            self.assertGreaterEqual(result.state['meta']['estimated_chapters'], 1)
            self.assertGreaterEqual(result.state['meta']['estimated_volumes'], 1)
            self.assertGreaterEqual(result.state['meta']['estimated_plot_units'], 1)

            loaded_state = load_project_state(result.project_dir)
            self.assertEqual(loaded_state['meta']['title'], title)

            summary = dashboard_summary_text(loaded_state)
            self.assertIn(title, summary)
            self.assertIn('项目仪表盘', summary)

            shortcuts = project_file_shortcuts(result.project_dir)
            self.assertEqual(shortcuts['项目目录'], result.project_dir)
            self.assertTrue(shortcuts['总纲模板'].exists())
            self.assertTrue(shortcuts['总导演提示'].exists())
            self.assertTrue(shortcuts['单元规划提示'].exists())
            self.assertTrue(shortcuts['章节卡提示'].exists())
            self.assertTrue(shortcuts['正文写作提示'].exists())
            self.assertTrue(shortcuts['审校提示'].exists())

            plot_units = loaded_state['plot_units']
            self.assertEqual(plot_units[0]['chapter_start'], 1)
            self.assertEqual(plot_units[-1]['chapter_end'], loaded_state['meta']['estimated_chapters'])
            for previous, current in zip(plot_units, plot_units[1:]):
                self.assertEqual(previous['chapter_end'] + 1, current['chapter_start'])

            director_prompt = shortcuts['总导演提示'].read_text(encoding='utf-8')
            self.assertIn(title, director_prompt)
            self.assertIn('总导演提示', director_prompt)
        finally:
            if project_dir.exists():
                shutil.rmtree(project_dir)

    def test_planning_scales_with_target_words(self) -> None:
        projects_root = Path('projects').resolve()
        small = build_story_state(
            ProjectInitData(
                title='短篇测试',
                premise='短中篇测试。',
                genre='玄幻',
                style='番茄系强钩子爽文',
                root_dir=projects_root,
                target_wan_words=8,
                avg_chapter_words=1800,
            ),
            projects_root / '短篇测试',
        )
        large = build_story_state(
            ProjectInitData(
                title='长篇测试',
                premise='长篇测试。',
                genre='玄幻',
                style='番茄系强钩子爽文',
                root_dir=projects_root,
                target_wan_words=90,
                avg_chapter_words=1800,
            ),
            projects_root / '长篇测试',
        )

        self.assertLess(small['meta']['estimated_volumes'], large['meta']['estimated_volumes'])
        self.assertLess(small['meta']['estimated_plot_units'], large['meta']['estimated_plot_units'])
        self.assertEqual(small['planning_profile']['label'], '短中篇模式')
        self.assertEqual(large['planning_profile']['label'], '长篇连载模式')


if __name__ == '__main__':
    unittest.main()
