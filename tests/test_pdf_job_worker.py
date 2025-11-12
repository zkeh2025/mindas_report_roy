import asyncio
import json
from typing import Any, Dict, List, Optional

from aiohttp import web

from job_workers import PdfJobWorker, WorkerConfig


class StubPdfJobWorker(PdfJobWorker):
    """PdfJobWorker subclass that records interactions for testing."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.load_updates: List[Dict[str, Any]] = []
        self.submitted_results: List[Dict[str, Any]] = []
        self.register_called: bool = False

    async def register(self) -> bool:  # type: ignore[override]
        self.register_called = True
        return True

    async def update_load(  # type: ignore[override]
        self, *, current_jobs: int, cpu_usage: float, memory_usage: float
    ) -> None:
        self.load_updates.append(
            {
                "current_jobs": current_jobs,
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
            }
        )

    async def submit_result(  # type: ignore[override]
        self,
        job_id: str,
        *,
        result: Optional[Dict[str, Any]],
        error: Optional[str],
        execution_time_ms: Optional[int] = None,
    ) -> None:
        self.submitted_results.append(
            {
                "job_id": job_id,
                "result": result,
                "error": error,
                "execution_time_ms": execution_time_ms,
            }
        )


async def _start_mock_pdf_api() -> web.AppRunner:
    async def handle_generate(request: web.Request) -> web.Response:
        payload = await request.json()
        report_id = payload.get("report_id", "unknown")
        return web.json_response(
            {
                "pdf_url": f"http://files.local/{report_id}.pdf",
                "received_payload": payload,
            }
        )

    app = web.Application()
    app.router.add_post("/generate", handle_generate)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    return runner


async def _get_runner_port(runner: web.AppRunner) -> int:
    sites = list(runner.sites)
    if not sites:
        raise RuntimeError("No site bound to runner")
    sockets = getattr(sites[0], "_server", None).sockets
    if not sockets:
        raise RuntimeError("No sockets available on runner site")
    return sockets[0].getsockname()[1]


async def main() -> None:
    runner = await _start_mock_pdf_api()
    worker: Optional[StubPdfJobWorker] = None
    try:
        port = await _get_runner_port(runner)
        pdf_url = f"http://127.0.0.1:{port}/generate"

        worker = StubPdfJobWorker(
            job_manager_url="http://job-manager.local/api/v1/jobs",
            worker_config=WorkerConfig(pdf_api_url=pdf_url),
        )

        await worker._ensure_sessions()

        job_payload = {
            "id": "0c6a8f7e-8d42-4aab-8c60-03f96d7b93a2",
            "job_type": {
                "WebApiJob": {
                    "url": pdf_url,
                    "method": "POST",
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps(
                        {
                            "report_id": "demo_report",
                            "student": {"name": "Alice", "grade": "11"},
                        }
                    ),
                    "timeout": 10,
                }
            },
        }

        await worker._handle_job(job_payload)

        assert worker.submitted_results, "Expected job result to be submitted"
        result_payload = worker.submitted_results[0]
        assert result_payload["error"] is None
        assert result_payload["result"] is not None
        web_api_response = result_payload["result"]["web_api_response"]
        assert web_api_response["status_code"] == 200
        assert web_api_response["pdf_url"] == "http://files.local/demo_report.pdf"

        print("PDF Job Worker integration test passed.")
    finally:
        if worker:
            await worker.stop()
        await runner.cleanup()


if __name__ == "__main__":
    asyncio.run(main())


