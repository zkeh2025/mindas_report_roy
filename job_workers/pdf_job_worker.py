import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict, Optional

import aiohttp


logger = logging.getLogger(__name__)


JobFetcher = Callable[["PdfJobWorker"], Awaitable[Optional[Dict[str, Any]]]]


@dataclass
class WorkerConfig:
    """Configuration payload used during worker registration."""

    pdf_api_url: str
    pdf_api_method: str = "POST"
    pdf_api_headers: Dict[str, str] = field(
        default_factory=lambda: {"Content-Type": "application/json"}
    )
    pdf_api_timeout: int = 120


class PdfJobWorker:
    """Job Manager worker dedicated to executing PDF generation Web API jobs."""

    def __init__(
        self,
        *,
        job_manager_url: str,
        worker_id: Optional[str] = None,
        max_concurrent_jobs: int = 2,
        worker_config: Optional[WorkerConfig] = None,
        job_manager_headers: Optional[Dict[str, str]] = None,
        job_fetcher: Optional[JobFetcher] = None,
        heartbeat_interval: int = 10,
        poll_interval: float = 2.0,
    ) -> None:
        """
        Args:
            job_manager_url: Base URL of the Job Manager (e.g. https://host/api/v1/jobs).
            worker_id: Optional worker identifier. If omitted a random value is generated.
            max_concurrent_jobs: Maximum number of jobs that can run simultaneously.
            worker_config: PDF API configuration describing the default WebApiJob payload.
            job_manager_headers: Optional HTTP headers required by the Job Manager (auth, tenant, etc.).
            job_fetcher: Coroutine returning the next job payload to execute. Defaults to no-op.
            heartbeat_interval: Interval (seconds) between heartbeat/load updates.
            poll_interval: Interval (seconds) used when no jobs are available.
        """
        self.worker_id = worker_id or f"pdf-worker-{uuid.uuid4().hex[:8]}"
        self.job_manager_url = job_manager_url.rstrip("/")
        self.max_concurrent_jobs = max_concurrent_jobs
        self.worker_config = worker_config
        self.job_manager_headers = job_manager_headers or {}
        self.job_fetcher = job_fetcher
        self.heartbeat_interval = heartbeat_interval
        self.poll_interval = poll_interval

        self._job_session: Optional[aiohttp.ClientSession] = None
        self._http_session: Optional[aiohttp.ClientSession] = None
        self._current_jobs: int = 0
        self._running: bool = False
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._job_loop_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the worker: register, open sessions, and launch background tasks."""
        if self._running:
            return

        await self._ensure_sessions()
        await self.register()

        self._running = True
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop(), name="pdf-worker-heartbeat")
        self._job_loop_task = asyncio.create_task(self._job_loop(), name="pdf-worker-jobs")
        logger.info("Worker %s started", self.worker_id)

    async def stop(self) -> None:
        """Stop worker execution and cleanup resources."""
        if not self._running:
            await self._close_sessions()
            return

        self._running = False

        for task in (self._heartbeat_task, self._job_loop_task):
            if task:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                except Exception as exc:
                    logger.debug("Background task raised during shutdown: %s", exc)

        await self._close_sessions()
        logger.info("Worker %s stopped", self.worker_id)

    async def _ensure_sessions(self) -> None:
        if self._job_session is None:
            timeout = aiohttp.ClientTimeout(total=60)
            self._job_session = aiohttp.ClientSession(
                headers=self.job_manager_headers, timeout=timeout
            )
        if self._http_session is None:
            self._http_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=300))

    async def _close_sessions(self) -> None:
        for session in (self._job_session, self._http_session):
            if session and not session.closed:
                await session.close()
        self._job_session = None
        self._http_session = None

    async def _heartbeat_loop(self) -> None:
        """Periodically publish heartbeat/load information."""
        try:
            while self._running:
                await self.update_load(
                    current_jobs=self._current_jobs,
                    cpu_usage=10.0 + self._current_jobs * 5.0,
                    memory_usage=20.0 + self._current_jobs * 8.0,
                )
                await asyncio.sleep(self.heartbeat_interval)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.error("Heartbeat loop encountered an error: %s", exc)

    async def _job_loop(self) -> None:
        """Continuously fetch and execute jobs."""
        try:
            while self._running:
                job_data = await self.fetch_next_job()
                if not job_data:
                    await asyncio.sleep(self.poll_interval)
                    continue

                await self._handle_job(job_data)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.error("Job loop encountered an error: %s", exc)

    async def fetch_next_job(self) -> Optional[Dict[str, Any]]:
        """Obtain the next job payload to execute."""
        if self.job_fetcher is None:
            return None
        return await self.job_fetcher(self)

    async def register(self) -> bool:
        """Register worker with the Job Manager."""
        if self._job_session is None:
            raise RuntimeError("Job session not initialised")

        payload = {
            "id": self.worker_id,
            "worker_type": "WebApi",
            "max_concurrent_jobs": self.max_concurrent_jobs,
            "supported_job_types": [],
        }

        if self.worker_config:
            payload["supported_job_types"].append(
                {
                    "WebApiJob": {
                        "url": self.worker_config.pdf_api_url,
                        "method": self.worker_config.pdf_api_method,
                        "headers": self.worker_config.pdf_api_headers,
                        "body": None,
                        "timeout": self.worker_config.pdf_api_timeout,
                    }
                }
            )

        url = f"{self.job_manager_url}/workers"

        try:
            async with self._job_session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("Worker %s registered successfully", self.worker_id)
                    return True
                text = await response.text()
                logger.error(
                    "Worker registration failed (%s): %s", response.status, text
                )
        except Exception as exc:
            logger.error("Worker registration error: %s", exc)
        return False

    async def update_load(
        self, *, current_jobs: int, cpu_usage: float, memory_usage: float
    ) -> None:
        """Send current load metrics to the Job Manager."""
        if self._job_session is None:
            return

        url = f"{self.job_manager_url}/workers/{self.worker_id}"
        payload = {
            "current_jobs": current_jobs,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
        }

        try:
            async with self._job_session.post(url, json=payload) as response:
                if response.status != 200:
                    text = await response.text()
                    logger.debug(
                        "Load update not accepted (%s): %s", response.status, text
                    )
        except Exception as exc:
            logger.warning("Failed to update load: %s", exc)

    async def submit_result(
        self,
        job_id: str,
        *,
        result: Optional[Dict[str, Any]],
        error: Optional[str],
        execution_time_ms: Optional[int] = None,
    ) -> None:
        """Submit job execution result back to Job Manager."""
        if self._job_session is None:
            return

        url = f"{self.job_manager_url}/jobs/{job_id}/result"
        payload: Dict[str, Any] = {
            "job_id": job_id,
            "status": "Completed" if error is None else "Failed",
            "result": json.dumps(result) if result is not None else None,
            "error": error,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        if execution_time_ms is not None:
            payload["execution_time_ms"] = execution_time_ms

        try:
            async with self._job_session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("Submitted result for job %s", job_id)
                else:
                    text = await response.text()
                    logger.error(
                        "Failed to submit result for job %s (%s): %s",
                        job_id,
                        response.status,
                        text,
                    )
        except Exception as exc:
            logger.error("Result submission error for job %s: %s", job_id, exc)

    async def execute_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatch execution based on the job type definition."""
        job_type = job_data.get("job_type") or {}

        if "WebApiJob" in job_type:
            return await self._execute_web_api_job(job_data, job_type["WebApiJob"])

        raise ValueError(f"Unsupported job type in payload: {job_type!r}")

    async def _handle_job(self, job_data: Dict[str, Any]) -> None:
        """Execute a single job and submit its result."""
        job_id = job_data.get("id") or uuid.uuid4().hex
        start_time = time.perf_counter()
        self._current_jobs += 1
        await self.update_load(
            current_jobs=self._current_jobs,
            cpu_usage=10.0 + self._current_jobs * 5.0,
            memory_usage=20.0 + self._current_jobs * 8.0,
        )

        try:
            execution_payload = await self.execute_job(job_data)
            duration_ms = int((time.perf_counter() - start_time) * 1000)
            await self.submit_result(
                job_id,
                result={
                    "worker_id": self.worker_id,
                    "web_api_response": execution_payload,
                },
                error=None,
                execution_time_ms=duration_ms,
            )
        except Exception as exc:
            logger.exception("Job %s failed: %s", job_id, exc)
            await self.submit_result(job_id, result=None, error=str(exc))
        finally:
            self._current_jobs = max(self._current_jobs - 1, 0)
            await self.update_load(
                current_jobs=self._current_jobs,
                cpu_usage=10.0 + self._current_jobs * 5.0,
                memory_usage=20.0 + self._current_jobs * 8.0,
            )

    async def _execute_web_api_job(
        self, job_data: Dict[str, Any], web_api_job: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute PDF generation through the configured Web API."""
        if self._http_session is None:
            raise RuntimeError("HTTP session not initialised")

        url = web_api_job.get("url") or (self.worker_config.pdf_api_url if self.worker_config else None)
        if not url:
            raise ValueError("WebApiJob url is not provided")

        method = web_api_job.get("method", "POST").upper()
        headers = web_api_job.get("headers") or {}
        body = web_api_job.get("body")
        timeout_seconds = web_api_job.get(
            "timeout",
            self.worker_config.pdf_api_timeout if self.worker_config else 120,
        )

        data: Optional[bytes] = None
        json_payload: Optional[Any] = None

        if isinstance(body, (dict, list)):
            json_payload = body
        elif isinstance(body, str):
            data = body.encode("utf-8")
        elif body is not None:
            json_payload = body

        timeout = aiohttp.ClientTimeout(total=timeout_seconds)

        async with self._http_session.request(
            method,
            url,
            headers=headers,
            json=json_payload,
            data=data,
            timeout=timeout,
        ) as response:
            raw_body = await response.text()
            parsed_body: Any
            try:
                parsed_body = json.loads(raw_body)
            except json.JSONDecodeError:
                parsed_body = raw_body

            result = {
                "status_code": response.status,
                "headers": dict(response.headers),
                "body": parsed_body,
            }

            # Promote commonly used fields from JSON response
            if isinstance(parsed_body, dict):
                for key in ("pdf_url", "download_url", "file_url"):
                    if key in parsed_body:
                        result[key] = parsed_body[key]

            return result


