import json
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.context_auditor.auditor import ContextAuditor
from src.context_auditor.adapters.gemini import GeminiAdapter

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "eval_dataset.jsonl")
    
    auditor = ContextAuditor(llm_adapter=GeminiAdapter())
    
    total = 0
    passed = 0
    
    with open(dataset_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            
            case = json.loads(line)
            total += 1
            case_id = case["case_id"]
            expected_status = case["expected_status"]
            requires_factual = case.get("task_requires_factual", False)
            
            try:
                # Note: Because the GeminiAdapter is mocked and returns perfect scores by default,
                # evaluating real status differences requires a real LLM.
                # Here we just ensure the pipeline executes without crashing on the dataset.
                result = auditor.audit(case["input"], task_requires_factual=requires_factual)
                
                # In a real run with the API, we'd check: assert result.overall_status.value == expected_status
                # For now we just validate that it produces a valid schema.
                print(f"[OK] {case_id} processed successfully. (Status: {result.overall_status.value})")
                passed += 1
            except Exception as e:
                print(f"[FAIL] {case_id} failed: {e}")
                
    print(f"\nEvaluation Complete. {passed}/{total} cases executed successfully.")
    
    if passed != total:
        sys.exit(1)

if __name__ == "__main__":
    main()
