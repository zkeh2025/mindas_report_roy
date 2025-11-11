#!/usr/bin/env python3
"""
简化的 Job Manager 测试（不依赖 aiohttp）。
支持通过命令行参数或环境变量注入测试用户权限头。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Dict, Optional, Tuple

DEFAULT_BASE_URL = "https://www.zkyhxl.cn:8443"
DEFAULT_HEADERS_PROFILE = "platform_admin"
DEFAULT_TIMEOUT = 20
HEADERS_FILE_NAME = "test_headers.json"


def load_headers(headers_file: Path, profile: str) -> Dict[str, str]:
    """从配置文件加载指定角色的默认测试头。"""
    if not headers_file.exists():
        return {}

    try:
        data = json.loads(headers_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"无法解析测试头文件 {headers_file}: {exc}") from exc

    profile_data = data.get(profile)
    if not profile_data:
        raise RuntimeError(
            f"测试头文件 {headers_file} 中不存在配置档案 '{profile}'，"
            "请检查 'headers' 字段或更换 --headers-profile 参数。"
        )

    headers = profile_data.get("headers")
    if not isinstance(headers, dict):
        raise RuntimeError(f"档案 '{profile}' 的 headers 字段不是对象。")

    return {str(k): str(v) for k, v in headers.items()}


def apply_header_overrides(headers: Dict[str, str], overrides: Dict[str, Optional[str]]) -> Dict[str, str]:
    """将命令行或环境变量提供的值覆盖到默认测试头。"""
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


class SimpleJobManagerTest:
    """简化的 Job Manager 测试器。"""

    def __init__(self, job_manager_url: str, headers: Dict[str, str], timeout: int):
        self.job_manager_url = job_manager_url.rstrip("/")
        self.headers = headers
        self.timeout = timeout

    def make_request(self, method: str, path: str, data: Optional[Dict] = None) -> Tuple[Optional[int], Optional[object]]:
        """发送 HTTP 请求并返回 (status, body)。"""
        url = f"{self.job_manager_url}{path}"
        request_data = None

        if data is not None:
            request_data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url, data=request_data, method=method)
        if data is not None:
            req.add_header("Content-Type", "application/json")

        for header_name, header_value in self.headers.items():
            req.add_header(header_name, header_value)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                try:
                    return response.status, json.loads(raw)
                except json.JSONDecodeError:
                    return response.status, raw
        except Exception as exc:
            print(f"请求失败: {exc}")
            return None, None

    def test_health(self) -> bool:
        """测试健康检查。"""
        print("1. 测试健康检查...")
        status, result = self.make_request("GET", "/api/v1/jobs/health")

        if status == 200:
            print("   ✅ 服务健康")
            print(f"   响应: {result}")
            return True

        print(f"   ❌ 服务异常: {status}")
        return False

    def test_executors(self) -> bool:
        """测试执行器列表。"""
        print("\n2. 测试执行器列表...")
        status, result = self.make_request("GET", "/api/v1/jobs/executors")

        if status == 200:
            executors = result if isinstance(result, list) else []
            print(f"   ✅ 找到 {len(executors)} 个执行器")
            for executor in executors[:3]:
                print(
                    "      - {id}: {running}/{max_jobs} 作业".format(
                        id=executor.get("id", "<unknown>"),
                        running=executor.get("current_jobs", 0),
                        max_jobs=executor.get("max_concurrent_jobs", 0),
                    )
                )
            return True

        print(f"   ❌ 查询失败: {status}")
        return False

    def test_create_job(self) -> Optional[str]:
        """测试创建作业。"""
        print("\n3. 测试创建作业...")
        job_payload = {
            "job_type": {
                "WebApiJob": {
                    "url": "https://httpbin.org/get",
                    "method": "GET",
                    "headers": {"User-Agent": "SimpleJobManagerTest"},
                    "body": None,
                    "timeout": 30,
                }
            },
            "priority": "High",
            "max_retries": 3,
        }

        status, result = self.make_request("POST", "/api/v1/jobs/jobs", job_payload)

        if status == 200 and isinstance(result, dict):
            job_id = result.get("job_id")
            print(f"   ✅ 作业创建成功: {job_id}")
            return job_id

        print(f"   ❌ 创建失败: {status} - {result}")
        return None

    def test_job_status(self, job_id: str) -> bool:
        """测试查询作业状态。"""
        print(f"\n4. 测试查询作业状态: {job_id}")
        status, result = self.make_request("GET", f"/api/v1/jobs/jobs/{job_id}")

        if status == 200 and isinstance(result, dict):
            print(f"   ✅ 作业状态: {result.get('status')}")
            print(f"   执行器: {result.get('executor_id')}")
            print(f"   优先级: {result.get('priority')}")
            return True

        print(f"   ❌ 查询失败: {status} - {result}")
        return False

    def run(self) -> bool:
        """按顺序执行所有测试。"""
        print("🚀 开始简化 Job Manager 测试")
        print("=" * 50)

        if not self.test_health():
            print("\n❌ 健康检查失败，无法继续测试")
            return False

        self.test_executors()
        job_id = self.test_create_job()

        if job_id:
            self.test_job_status(job_id)

        print("\n" + "=" * 50)
        print("✅ 简化测试完成！")
        return True


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""
    parser = argparse.ArgumentParser(description="Job Manager Python 集成测试")
    parser.add_argument(
        "--url",
        default=os.getenv("JOB_TEST_URL", DEFAULT_BASE_URL),
        help="Job Manager 服务地址（默认: %(default)s）",
    )
    parser.add_argument(
        "--headers-profile",
        default=os.getenv("JOB_TEST_HEADERS_PROFILE", DEFAULT_HEADERS_PROFILE),
        help="测试头配置档案名称（默认: %(default)s）",
    )
    parser.add_argument(
        "--headers-file",
        default=os.getenv("JOB_TEST_HEADERS_FILE"),
        help="测试头配置文件路径（默认: 当前目录下的 test_headers.json）",
    )
    parser.add_argument(
        "--user-id",
        default=os.getenv("JOB_TEST_USER_ID"),
        help="覆盖 X-Test-User-Id 的值",
    )
    parser.add_argument(
        "--user-name",
        default=os.getenv("JOB_TEST_USER_NAME"),
        help="覆盖 X-Test-User-Name 的值",
    )
    parser.add_argument(
        "--roles",
        default=os.getenv("JOB_TEST_USER_ROLES"),
        help="覆盖 X-Test-User-Roles 的值",
    )
    parser.add_argument(
        "--tenant-id",
        default=os.getenv("JOB_TEST_TENANT_ID"),
        help="覆盖 X-Tenant-ID 的值",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.getenv("JOB_TEST_TIMEOUT", DEFAULT_TIMEOUT)),
        help="请求超时时间（秒）",
    )
    parser.add_argument(
        "--print-headers",
        action="store_true",
        help="运行前打印最终使用的请求头",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    headers_file = Path(args.headers_file) if args.headers_file else Path(__file__).resolve().parent / HEADERS_FILE_NAME

    try:
        base_headers = load_headers(headers_file, args.headers_profile)
    except RuntimeError as exc:
        print(f"⚠️  {exc}")
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
        print("使用的测试头：")
        for name, value in headers.items():
            print(f"  {name}: {value}")

    test = SimpleJobManagerTest(job_manager_url=args.url, headers=headers, timeout=args.timeout)
    success = test.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
