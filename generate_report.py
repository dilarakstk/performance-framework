import json

with open("test_results.json") as f:
    results = json.load(f)

report = "# 🚀 Performance Test Report\n\n"

# Genel sonuç
overall_pass = all(item["result"] == "PASS" for item in results)

if overall_pass:
    report += "## ✅ Overall Result: PASS\n\n"
else:
    report += "## ❌ Overall Result: FAIL\n\n"

report += "| Scenario | Result | Exit Code |\n"
report += "|----------|--------|-----------|\n"

for item in results:
    scenario = item["scenario"]
    result = item["result"]
    exit_code = item["exit_code"]

    report += f"| {scenario} | {result} | {exit_code} |\n"

# yorum ekle
report += "\n## 🧠 Analysis\n\n"

if overall_pass:
    report += "- System handled all load scenarios successfully.\n"
    report += "- No critical performance degradation observed.\n"
else:
    report += "- Performance issues detected under certain load conditions.\n"
    report += "- Further optimization is required.\n"

# kaydet
with open("REPORT.md", "w") as f:
    f.write(report)

print("✅ REPORT.md güncellendi")