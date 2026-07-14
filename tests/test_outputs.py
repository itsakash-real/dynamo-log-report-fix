import json
import re
from collections import Counter
from pathlib import Path


def test_report_file_is_valid_json():
    """Verify the report file exists and contains valid JSON."""
    path = Path("/app/report.json")
    assert path.exists(), "report.json was not created"
    data = json.loads(path.read_text())
    assert isinstance(data, dict), "report.json must contain a JSON object"
    assert "total_requests" in data, "missing total_requests key"
    assert "unique_ips" in data, "missing unique_ips key"
    assert "top_path" in data, "missing top_path key"


def test_total_requests_matches_log():
    """Verify total_requests equals the number of non-empty lines in access.log."""
    path = Path("/app/report.json")
    data = json.loads(path.read_text())
    log_lines = [l for l in Path("/app/access.log").read_text().splitlines() if l.strip()]
    assert data["total_requests"] == len(log_lines), \
        f"expected {len(log_lines)} requests, got {data['total_requests']}"


def test_unique_ips_matches_log():
    """Verify unique_ips is the count of distinct client IPs in access.log."""
    path = Path("/app/report.json")
    data = json.loads(path.read_text())
    ips = {l.split()[0] for l in Path("/app/access.log").read_text().splitlines() if l.strip()}
    assert data["unique_ips"] == len(ips), \
        f"expected {len(ips)} unique IPs, got {data['unique_ips']}"


def test_top_path_is_most_common():
    """Verify top_path is the most frequently requested path in the log."""
    path = Path("/app/report.json")
    data = json.loads(path.read_text())
    paths = []
    for line in Path("/app/access.log").read_text().splitlines():
        m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
        if m:
            paths.append(m.group(1))
    expected_top = Counter(paths).most_common(1)[0][0]
    assert data["top_path"] == expected_top, \
        f"expected top_path '{expected_top}', got '{data['top_path']}'"
