from pathlib import Path


def test_required_templates_exist():
    assert Path("wiki/_templates/factor.md").exists()
    assert Path("wiki/_templates/activation.md").exists()
    assert Path("AGENTS.md").exists()
