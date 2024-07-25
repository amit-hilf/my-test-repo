class MockScheduler:
    def __init__(self):
        self.jobs = []

    def add_job(
        self, 
        job_name: str,
        schedule_expression: str, 
        target: str,
    ) -> None:
        self.jobs.append({
            'job_name': job_name,
            'schedule_expression': schedule_expression,
            'target': target
        })
        print(f"Job {job_name} added with schedule {schedule_expression}")

    def run_job(
        self,
    ) -> None:
        for job in self.jobs:
            print(f"Running job {job['job_name']}")
            job['target']()
