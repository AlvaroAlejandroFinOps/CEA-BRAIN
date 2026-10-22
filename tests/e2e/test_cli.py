import json
import subprocess
import os

def get_base_dir():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_cli_healthy_conversation():
    base_dir = get_base_dir()
    example_path = os.path.join(base_dir, "examples", "healthy-conversation.json")
    
    # Run CLI as a module
    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir
    
    result = subprocess.run(
        ["python", "-m", "src.context_auditor.cli", example_path, "--adapter", "gemini"],
        capture_output=True,
        text=True,
        env=env
    )
    
    # It should succeed
    assert result.returncode == 0
    
    # Output should be valid JSON
    output_json = json.loads(result.stdout)
    
    # Verify schema version and fields
    assert output_json["schema_version"] == "1.0.0"
    assert "audit_id" in output_json
    assert "risk_score" in output_json
    assert output_json["overall_status"] in ["stable", "moderate", "high", "critical"]

def test_cli_invalid_file():
    base_dir = get_base_dir()
    example_path = os.path.join(base_dir, "examples", "non_existent.json")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir
    
    result = subprocess.run(
        ["python", "-m", "src.context_auditor.cli", example_path],
        capture_output=True,
        text=True,
        env=env
    )
    
    # It should fail
    assert result.returncode == 1
    assert "Error during audit" in result.stderr

def test_cli_fast_gate_only():
    base_dir = get_base_dir()
    example_path = os.path.join(base_dir, "examples", "healthy-conversation.json")

    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir

    result = subprocess.run(
        ["python", "-m", "src.context_auditor.cli", example_path, "--fast-gate-only"],
        capture_output=True,
        text=True,
        env=env
    )

    assert result.returncode == 0
    output_json = json.loads(result.stdout)
    assert output_json["schema_version"] == "1.0.0"
    assert "l1_verdict" in output_json
    assert output_json["l1_verdict"]["route"] == "pass"
    assert "L1 Fast Gate" in output_json["limitations"][0]

def test_governance_files_exist():
    base_dir = get_base_dir()
    agents_md = os.path.join(base_dir, "AGENTS.md")
    run_audit_sh = os.path.join(base_dir, "run_audit.sh")
    ci_yml = os.path.join(base_dir, ".github", "workflows", "ci.yml")

    assert os.path.exists(agents_md), "AGENTS.md must exist in repository root"
    assert os.path.exists(run_audit_sh), "run_audit.sh must exist in repository root"
    assert os.path.exists(ci_yml), ".github/workflows/ci.yml must exist"
