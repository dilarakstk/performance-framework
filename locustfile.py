import json
from locust import HttpUser, task, between, events

with open("config/thresholds.json") as f:
    THRESHOLDS = json.load(f)

with open("config/config.json") as f:
    config = json.load(f)

HOST = config["host"]
ENDPOINT = config["endpoint"]


class PerformanceUser(HttpUser):
    wait_time = between(1, 2)
    host = HOST

    @task
    def test_endpoint(self):
        self.client.get(ENDPOINT)


@events.quitting.add_listener
def evaluate_performance(environment, **kwargs):
    print("BURAYA GİRDİ")
    stats = environment.stats.total

    avg = stats.avg_response_time
    p95 = stats.get_response_time_percentile(0.95)
    fail_rate = stats.fail_ratio * 100

    print("\n--- TEST SONUCU ---")
    print(f"Average Response Time: {avg} ms")
    print(f"95th Percentile: {p95} ms")
    print(f"Failure Rate: {fail_rate} %")

    failed = False

    if avg > THRESHOLDS["avg_response_time_ms"]:
        print("FAIL: Average response time çok yüksek")
        failed = True

    if p95 > THRESHOLDS["p95_response_time_ms"]:
        print("FAIL: 95th percentile çok yüksek")
        failed = True

    if fail_rate > THRESHOLDS["failure_rate_percent"]:
        print("FAIL: Failure rate çok yüksek")
        failed = True

    if failed:
        print("SONUÇ: TEST BAŞARISIZ")
        environment.process_exit_code = 1
    else:
        print("SONUÇ: TEST BAŞARILI")
        environment.process_exit_code = 0