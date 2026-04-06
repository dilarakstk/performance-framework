import json
import subprocess
import time


with open("config/config.json") as f:
    config = json.load(f)

scenarios = config["scenarios"]
host = config["host"]


def run_scenario(name, users, spawn_rate, run_time):
    print(f"\n=== {name.upper()} SENARYOSU BAŞLIYOR ===")
    print(f"Users: {users}")
    print(f"Spawn rate: {spawn_rate}")
    print(f"Run time: {run_time}")
    print(f"Host: {host}")

    command = [
        "python3",
        "-m",
        "locust",
        "-f",
        "locustfile.py",
        "--headless",
        "-u",
        str(users),
        "-r",
        str(spawn_rate),
        "--run-time",
        run_time,
        "--host",
        host,
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)

    if result.returncode == 0:
        print(f"=== {name.upper()} SONUÇ: PASS ===")
    else:
        print(f"=== {name.upper()} SONUÇ: FAIL ===")

    return {
        "scenario": name,
        "users": users,
        "spawn_rate": spawn_rate,
        "run_time": run_time,
        "exit_code": result.returncode,
        "result": "PASS" if result.returncode == 0 else "FAIL",
        "output": result.stdout,
    }


def main():
    all_results = []

    for scenario_name, scenario_data in scenarios.items():
        result = run_scenario(
            scenario_name,
            scenario_data["users"],
            scenario_data["spawn_rate"],
            scenario_data["run_time"],
        )
        all_results.append(result)
        time.sleep(2)

    with open("test_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print("\n=== TÜM SENARYOLAR TAMAMLANDI ===")
    print("Sonuçlar test_results.json dosyasına kaydedildi.")


if __name__ == "__main__":
    main()