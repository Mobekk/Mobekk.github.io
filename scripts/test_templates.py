"""Render adversarial author metadata through Jekyll and inspect the real output."""
from pathlib import Path
import shutil
import subprocess
import tempfile
from check_site import check

repo = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="blog-security-") as directory:
    source = Path(directory) / "source"
    output = Path(directory) / "output"
    source.mkdir()
    for name in ("_config.yml", "_layouts", "_posts", "index.html", "about.md", "assets", "CNAME", ".well-known"):
        origin, target = repo / name, source / name
        if origin.is_dir():
            shutil.copytree(origin, target)
        else:
            shutil.copy2(origin, target)
    payload = '\"><script>alert(1)</script><img src=x onerror=alert(1)>'
    # YAML single quotes preserve the HTML payload literally.
    (source / "_posts/2020-01-01-security-fixture.md").write_text(
        "---\nlayout: post\ntitle: '" + payload + "'\nread_time: '" + payload + "'\n"
        "tags: ['" + payload + "']\nexcerpt: '&lt;img src=x onerror=alert(1)&gt;'\n"
        "image: /assets/images/me.png\n---\nFixture body.\n"
    )
    bad_images = ['https://example.com/tracker.png', '//example.com/tracker.png',
                  '/assets/images/../../Gemfile', '/assets/images/%2e%2e/Gemfile',
                  '/assets/images/me.png" onerror="alert(1)']
    for index, image in enumerate(bad_images):
        (source / f"_posts/2020-01-02-invalid-image-{index}.md").write_text(
            "---\nlayout: post\ntitle: Invalid image\nimage: '" + image + "'\n---\nFixture.\n"
        )
    subprocess.run(["bundle", "exec", "jekyll", "build", "--safe", "--strict_front_matter",
                    "--source", str(source), "--destination", str(output)], check=True, cwd=repo)
    check(output)
    fixture = output / "2020/01/01/security-fixture.html"
    assert '&lt;script&gt;' in fixture.read_text()
    assert '<img src="/assets/images/me.png" alt="&quot;&gt;&lt;script&gt;' in fixture.read_text()
    for index in range(len(bad_images)):
        page = output / f"2020/01/02/invalid-image-{index}.html"
        assert 'post-cover-image' not in page.read_text(), "Invalid image metadata was accepted"
print("Malicious metadata stayed escaped; remote, missing and traversal image paths were omitted.")
