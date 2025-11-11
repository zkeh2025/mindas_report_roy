# Job Manager 用户指南

## 📖 概述

Job Manager是一个基于Rust的分布式作业管理系统，支持Web API作业调度和执行。本指南将帮助您创建符合要求的Job执行器。

## 🚀 快速开始

### 1. 启动Job Manager服务器

```bash
(cd ../../.. && cargo run --bin zkeh-server)
```

服务器默认通过 `https://www.zkyhxl.cn:8443` 提供服务（本地调试可改为 `http://127.0.0.1:3001`）。

### 2. 验证服务状态

```bash
curl -X GET https://www.zkyhxl.cn:8443/api/v1/jobs/health \
  -H "X-Test-User-Id: 485c6921-974c-4fad-93fc-464c639db4ee" \
  -H "X-Test-User-Name: test_platform_admin" \
  -H "X-Test-User-Roles: platform_admin" \
  -H "X-Tenant-ID: 00000000-0000-0000-0000-000000000001"
```

预期响应：
```json
{
  "status": "healthy",
  "timestamp": "2025-10-25T11:10:23.820241428Z"
}
```

### 3. 测试身份配置

- 在当前目录下维护 `test_headers.json`，存放常用测试身份与请求头。
- 通过 `--headers-profile platform_admin` 或设置 `JOB_TEST_HEADERS_PROFILE=tenant_a_supervisor` 可切换身份。
- `simple_test.py` 与 `simple_job_executor.py` 支持 `--user-id`、`--roles`、`--tenant-id` 等参数直接覆盖请求头，便于临时调试。

## 🔧 创建Job执行器

### 执行器注册

首先，您需要向Job Manager注册您的执行器：

```bash
curl -X POST https://www.zkyhxl.cn:8443/api/v1/jobs/executors \
  -H "Content-Type: application/json" \
  -H "X-Test-User-Id: 485c6921-974c-4fad-93fc-464c639db4ee" \
  -H "X-Test-User-Name: test_platform_admin" \
  -H "X-Test-User-Roles: platform_admin" \
  -H "X-Tenant-ID: 00000000-0000-0000-0000-000000000001" \
  -d '{
    "id": "my-executor-001",
    "executor_type": "WebApi",
    "max_concurrent_jobs": 2,
    "supported_job_types": [
      {
        "WebApiJob": {
          "url": "https://example.com",
          "method": "GET",
          "headers": {},
          "body": null,
          "timeout": 30
        }
      }
    ]
  }'
```

### 执行器要求

您的执行器必须实现以下功能：

1. **注册到Job Manager**
2. **定期更新负载状态**
3. **处理作业请求**
4. **报告作业结果**

## 📝 执行器实现示例

### Python执行器示例

```python
#!/usr/bin/env python3
"""
简化的Job执行器示例
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any

class JobExecutor:
    def __init__(self, executor_id: str, job_manager_url: str, max_jobs: int = 2):
        self.executor_id = executor_id
        self.job_manager_url = job_manager_url
        self.max_jobs = max_jobs
        self.current_jobs = 0
        self.running_jobs = {}
        
    async def register(self):
        """注册执行器到Job Manager"""
        executor_data = {
            "id": self.executor_id,
            "executor_type": "WebApi",
            "max_concurrent_jobs": self.max_jobs,
            "supported_job_types": [
                {
                    "WebApiJob": {
                        "url": "https://example.com",
                        "method": "GET",
                        "headers": {},
                        "body": None,
                        "timeout": 30
                    }
                }
            ]
        }
        
        test_headers = {
            "X-Test-User-Id": "485c6921-974c-4fad-93fc-464c639db4ee",
            "X-Test-User-Name": "test_platform_admin",
            "X-Test-User-Roles": "platform_admin",
            "X-Tenant-ID": "00000000-0000-0000-0000-000000000001"
        }
        
        async with aiohttp.ClientSession(headers=test_headers) as session:
            async with session.post(
                f"{self.job_manager_url}/api/v1/jobs/executors",
                json=executor_data
            ) as response:
                if response.status == 200:
                    print(f"✅ 执行器 {self.executor_id} 注册成功")
                    return True
                else:
                    print(f"❌ 执行器注册失败: {await response.text()}")
                    return False
    
    async def update_load(self, cpu_usage: float = 0.0, memory_usage: float = 0.0):
        """更新执行器负载状态"""
        load_data = {
            "current_jobs": self.current_jobs,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.job_manager_url}/api/v1/jobs/executors/{self.executor_id}",
                json=load_data
            ) as response:
                if response.status == 200:
                    print(f"📊 负载更新: {self.current_jobs}/{self.max_jobs} 作业")
                else:
                    print(f"❌ 负载更新失败: {await response.text()}")
    
    async def execute_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行作业"""
        job_type = job_data.get("job_type", {})
        
        if "WebApiJob" in job_type:
            web_job = job_type["WebApiJob"]
            url = web_job["url"]
            method = web_job["method"]
            headers = web_job.get("headers", {})
            body = web_job.get("body")
            timeout = web_job.get("timeout", 30)
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method=method,
                        url=url,
                        headers=headers,
                        data=body,
                        timeout=aiohttp.ClientTimeout(total=timeout)
                    ) as response:
                        result_text = await response.text()
                        
                        return {
                            "status": "completed",
                            "result": {
                                "status_code": response.status,
                                "headers": dict(response.headers),
                                "body": result_text
                            },
                            "error": None
                        }
            except Exception as e:
                return {
                    "status": "failed",
                    "result": None,
                    "error": str(e)
                }
        
        return {
            "status": "failed",
            "result": None,
            "error": "不支持的作业类型"
        }
    
    async def run(self):
        """运行执行器主循环"""
        # 注册执行器
        if not await self.register():
            return
        
        print(f"🚀 执行器 {self.executor_id} 开始运行...")
        
        while True:
            try:
                # 更新负载状态
                await self.update_load()
                
                # 这里可以添加获取待处理作业的逻辑
                # 目前Job Manager还没有实现作业分发机制
                
                await asyncio.sleep(5)  # 每5秒更新一次状态
                
            except KeyboardInterrupt:
                print(f"🛑 执行器 {self.executor_id} 停止")
                break
            except Exception as e:
                print(f"❌ 执行器错误: {e}")
                await asyncio.sleep(5)

# 使用示例
async def main():
    executor = JobExecutor(
        executor_id="my-executor-001",
        job_manager_url="https://www.zkyhxl.cn:8443",
        max_jobs=2
    )
    
    await executor.run()

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔄 Job Manager API

### 核心端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/v1/jobs/health` | 健康检查 |
| POST | `/api/v1/jobs/executors` | 注册执行器 |
| GET | `/api/v1/jobs/executors` | 获取执行器列表 |
| POST | `/api/v1/jobs/executors/{id}` | 更新执行器负载 |
| POST | `/api/v1/jobs/jobs` | 创建作业 |
| GET | `/api/v1/jobs/jobs/{id}` | 获取作业信息 |
| GET | `/api/v1/jobs/jobs/{id}/result` | 获取作业结果 |

### 作业类型

#### WebApiJob
```json
{
  "WebApiJob": {
    "url": "https://api.example.com/data",
    "method": "GET",
    "headers": {
      "Authorization": "Bearer token",
      "Content-Type": "application/json"
    },
    "body": "{\"key\": \"value\"}",
    "timeout": 30
  }
}
```

### 执行器类型

#### WebApi执行器
```json
{
  "id": "executor-001",
  "executor_type": "WebApi",
  "max_concurrent_jobs": 2,
  "supported_job_types": [
    {
      "WebApiJob": {
        "url": "https://example.com",
        "method": "GET",
        "headers": {},
        "body": null,
        "timeout": 30
      }
    }
  ]
}
```

## 🧪 测试工具

### 基本测试

运行基本功能测试：

```bash
cd crates/job-manager/test-python
python3 simple_test.py
```

### 执行器测试

启动示例执行器：

```bash
cd crates/job-manager/test-python
python3 simple_job_executor.py --executor-id "test-executor-001" --max-jobs 2
```

### 运行测试套件

```bash
cd crates/job-manager/test-python
bash run_test.sh quick
```

## 📋 最佳实践

### 1. 执行器设计
- 实现健康检查机制
- 定期更新负载状态
- 处理作业超时
- 实现错误重试

### 2. 作业设计
- 设置合理的超时时间
- 包含必要的认证信息
- 使用幂等操作
- 提供详细的错误信息

### 3. 监控和日志
- 记录作业执行状态
- 监控执行器性能
- 设置告警机制
- 保留执行历史

## 🔍 故障排除

### 常见问题

1. **执行器注册失败**
   - 检查Job Manager服务器是否运行
   - 验证网络连接
   - 检查JSON格式

2. **作业执行失败**
   - 检查目标URL是否可访问
   - 验证认证信息
   - 检查超时设置

3. **负载更新失败**
   - 确认执行器ID正确
   - 检查数据格式
   - 验证权限

### 调试技巧

1. 使用curl测试API端点
2. 查看Job Manager服务器日志
3. 检查数据库中的作业状态
4. 使用健康检查端点验证服务状态

## 📚 更多资源

- [Job Manager API文档](https://www.zkyhxl.cn:8443/swagger-ui/job-manager/)
- [测试报告](TEST_REPORT.md)
- [README文档](README.md)

---

**需要帮助？** 请查看测试文件或联系开发团队。
