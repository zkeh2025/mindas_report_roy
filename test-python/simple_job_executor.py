#!/usr/bin/env python3
"""
简化的 Job Manager 任务执行器，支持在测试环境中注入权限头。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import aiohttp

DEFAULT_BASE_URL = "https://www.zkyhxl.cn:8443"
DEFAULT_HEADERS_PROFILE = "platform_admin"
HEADERS_FILE_NAME = "test_headers.json"

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_headers(headers_file: Path, profile: str) -> Dict[str, str]:
    if not headers_file.exists():
        return {}

    try:
        data = json.loads(headers_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"无法解析测试头文件 {headers_file}: {exc}") from exc

    profile_data = data.get(profile)
    if not profile_data:
        raise RuntimeError(f"测试头文件 {headers_file} 中不存在配置档案 '{profile}'。")

    headers = profile_data.get("headers")
    if not isinstance(headers, dict):
        raise RuntimeError(f"档案 '{profile}' 的 headers 字段不是对象。")

    return {str(k): str(v) for k, v in headers.items()}


def apply_header_overrides(headers: Dict[str, str], overrides: Dict[str, Optional[str]]) -> Dict[str, str]:
    mapping = {
        "user_id": "X-Test-User-Id",
        "user_name": "X-Test-User-Name",
        "roles": "X-Test-User-Roles",
        "tenant_id": "X-Tenant-ID",
    }

    result = dict(headers)
    for key, header_name in mapping.items():
        value = overrides.get(key)
        if value:
            result[header_name] = value

    return result


class SimpleJobExecutor:
    """简化的任务执行器"""

    def __init__(self, executor_id: str, job_manager_url: str, max_jobs: int, headers: Dict[str, str]):
        self.executor_id = executor_id
        self.job_manager_url = job_manager_url.rstrip("/")
        self.max_jobs = max_jobs
        self.headers = headers
        self.session: Optional[aiohttp.ClientSession] = None
        self.running_jobs: Dict[str, asyncio.Task] = {}
        self.is_running = False

    async def start(self) -> None:
        """启动执行器"""
        logger.info("启动执行器 %s", self.executor_id)

        self.session = aiohttp.ClientSession(headers=self.headers)
        self.is_running = True

        await self.register()
        await self.main_loop()

    async def stop(self) -> None:
        """停止执行器"""
        logger.info("停止执行器...")
        self.is_running = False
        if self.session:
            await self.session.close()

    async def register(self) -> None:
        """注册执行器"""
        url = f"{self.job_manager_url}/api/v1/executors"
        payload = {
            "id": self.executor_id,
            "executor_type": "WebApi",
            "max_concurrent_jobs": self.max_jobs,
            "supported_job_types": ["WebApiJob"],
        }

        try:
            assert self.session is not None
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("执行器 %s 注册成功", self.executor_id)
                else:
                    text = await response.text()
                    logger.error("注册失败: %s - %s", response.status, text)
        except Exception as exc:
            logger.error("注册错误: %s", exc)

    async def main_loop(self) -> None:
        """主循环"""
        while self.is_running:
            try:
                await self.send_heartbeat()
                await self.check_running_jobs()
                await asyncio.sleep(5)
            except Exception as exc:
                logger.error("主循环错误: %s", exc)
                await asyncio.sleep(5)

    async def send_heartbeat(self) -> None:
        """发送心跳"""
        url = f"{self.job_manager_url}/api/v1/executors/{self.executor_id}"
        payload = {
            "current_jobs": len(self.running_jobs),
            "cpu_usage": 50.0 + len(self.running_jobs) * 20.0,
            "memory_usage": 60.0 + len(self.running_jobs) * 15.0,
        }

        try:
            assert self.session is not None
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.debug("心跳发送成功")
                else:
                    text = await response.text()
                    logger.warning("心跳发送失败: %s - %s", response.status, text)
        except Exception as exc:
            logger.error("心跳错误: %s", exc)

    async def check_running_jobs(self) -> None:
        """检查运行中的作业"""
        completed_jobs = []

        for job_id, task in list(self.running_jobs.items()):
            if task.done():
                completed_jobs.append(job_id)
                try:
                    result = await task
                    logger.info("作业 %s 完成: %s", job_id, result)
                except Exception as exc:
                    logger.error("作业 %s 失败: %s", job_id, exc)

        for job_id in completed_jobs:
            self.running_jobs.pop(job_id, None)

    async def execute_job(self, job_data: Dict) -> bool:
        """执行作业"""
        job_id = job_data["id"]

        logger.info("开始执行作业 %s", job_id)

        try:
            execution_time = 2.0 + (hash(job_id) % 30) / 10.0
            await asyncio.sleep(execution_time)

            result = {
                "status": "success",
                "executor_id": self.executor_id,
                "execution_time": execution_time,
                "timestamp": datetime.now().isoformat(),
                "data": f"Job {job_id} completed by {self.executor_id}",
            }

            await self.submit_result(job_id, result, None)
            logger.info("作业 %s 执行完成", job_id)
            return True

        except Exception as exc:
            logger.error("作业 %s 执行失败: %s", job_id, exc)
            await self.submit_result(job_id, None, str(exc))
            return False

    async def submit_result(self, job_id: str, result: Optional[Dict], error: Optional[str]) -> None:
        """提交作业结果"""
        url = f"{self.job_manager_url}/api/v1/jobs/{job_id}/result"
        payload = {
            "job_id": job_id,
            "status": "Completed" if result else "Failed",
            "result": json.dumps(result) if result else None,
            "error": error,
            "completed_at": datetime.now().isoformat(),
        }

        try:
            assert self.session is not None
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("作业 %s 结果提交成功", job_id)
                else:
                    text = await response.text()
                    logger.error("作业 %s 结果提交失败: %s - %s", job_id, response.status, text)
        except Exception as exc:
            logger.error("提交结果错误: %s", exc)

    async def assign_job(self, job_data: Dict) -> bool:
        """分配作业"""
        job_id = job_data["id"]

        if len(self.running_jobs) >= self.max_jobs:
            logger.warning("执行器容量已满，无法执行作业 %s", job_id)
            return False

        task = asyncio.create_task(self.execute_job(job_data))
        self.running_jobs[job_id] = task

        logger.info("作业 %s 已分配给执行器 %s", job_id, self.executor_id)
        return True


async def main() -> None:
    parser = argparse.ArgumentParser(description="简化的 Job Manager 任务执行器")
    parser.add_argument("--executor-id", default=f"executor-{uuid.uuid4().hex[:8]}", help="执行器 ID")
    parser.add_argument(
        "--job-manager-url",
        default=DEFAULT_BASE_URL,
        help="Job Manager 服务器 URL",
    )
    parser.add_argument("--max-jobs", type=int, default=2, help="最大并发任务数")
    parser.add_argument("--headers-profile", default=DEFAULT_HEADERS_PROFILE, help="测试头配置档案名称")
    parser.add_argument("--headers-file", help="测试头配置文件路径（默认: 当前目录下的 test_headers.json）")
    parser.add_argument("--user-id", help="覆盖 X-Test-User-Id 的值")
    parser.add_argument("--user-name", help="覆盖 X-Test-User-Name 的值")
    parser.add_argument("--roles", help="覆盖 X-Test-User-Roles 的值")
    parser.add_argument("--tenant-id", help="覆盖 X-Tenant-ID 的值")
    parser.add_argument("--print-headers", action="store_true", help="启动前打印请求头")

    args = parser.parse_args()

    headers_file = Path(args.headers_file) if args.headers_file else Path(__file__).resolve().parent / HEADERS_FILE_NAME

    try:
        base_headers = load_headers(headers_file, args.headers_profile)
    except RuntimeError as exc:
        logger.warning("%s", exc)
        base_headers = {}

    headers = apply_header_overrides(
        base_headers,
        {
            "user_id": args.user_id,
            "user_name": args.user_name,
            "roles": args.roles,
            "tenant_id": args.tenant_id,
        },
    )

    if args.print_headers:
        logger.info("使用的测试头: %s", headers)

    executor = SimpleJobExecutor(
        executor_id=args.executor_id,
        job_manager_url=args.job_manager_url,
        max_jobs=args.max_jobs,
        headers=headers,
    )

    try:
        await executor.start()
    except KeyboardInterrupt:
        logger.info("收到停止信号...")
    finally:
        await executor.stop()


if __name__ == "__main__":
    asyncio.run(main())
