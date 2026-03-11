import shutil
import unittest
import uuid
from pathlib import Path

from novel_writer.state import (
    ProjectInitData,
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
            self.assertEqual(result.state['meta']['target_wan_words'], 48)
            self.assertGreaterEqual(result.state['meta']['estimated_chapters'], 1)
            self.assertGreaterEqual(result.state['meta']['estimated_volumes'], 1)

            loaded_state = load_project_state(result.project_dir)
            self.assertEqual(loaded_state['meta']['title'], title)

            summary = dashboard_summary_text(loaded_state)
            self.assertIn(title, summary)
            self.assertIn('项目仪表盘', summary)

            shortcuts = project_file_shortcuts(result.project_dir)
            self.assertEqual(shortcuts['项目目录'], result.project_dir)
            self.assertTrue(shortcuts['总纲模板'].exists())
        finally:
            if project_dir.exists():
                shutil.rmtree(project_dir)


if __name__ == '__main__':
    unittest.main()
