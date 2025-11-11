# Job Manager 测试套件

这个目录包含了Job Manager模块的测试工具和示例。

## 📁 文件说明

### 核心文件
- `simple_test.py` - 基本功能测试脚本
- `simple_job_executor.py` - 简化的Job执行器示例
- `run_test.sh` - 测试运行器

### 文档
- `USER_GUIDE.md` - 用户指南（推荐阅读）
- `README.md` - 本文件
- `TEST_REPORT.md` - 测试报告

## 🚀 快速开始

### 1. 启动Job Manager服务器
```bash
(cd ../../.. && cargo run --bin zkeh-server)
```

### 2. 运行基本测试
```bash
python3 simple_test.py --print-headers
```

### 3. 启动示例执行器
```bash
python3 simple_job_executor.py --executor-id "test-executor-001" --max-jobs 2 --print-headers
```

### 4. 运行测试套件
```bash
bash run_test.sh quick https://www.zkyhxl.cn:8443 platform_admin
```

### 5. 指定测试身份
- 通过 `test_headers.json` 维护常用测试身份与请求头。
- 使用 `JOB_TEST_HEADERS_PROFILE` 环境变量或命令行参数（如 `--headers-profile tenant_a_supervisor`）切换身份。
- 直接传入 `--user-id`、`--roles`、`--tenant-id` 可覆盖默认值。

## 📖 用户指南

详细的使用说明请参考 [USER_GUIDE.md](USER_GUIDE.md)，包含：

- 如何创建Job执行器
- API使用说明
- 最佳实践
- 故障排除

## 🧪 测试功能

### 基本测试 (`simple_test.py`)
- ✅ 健康检查
- ✅ 执行器列表
- ✅ 作业创建
- ✅ 作业状态查询

### 执行器示例 (`simple_job_executor.py`)
- 支持并行执行2个任务
- 自动注册到Job Manager
- 模拟任务执行延迟
- 实时上报任务状态

## 🔧 依赖

```bash
pip3 install aiohttp
```

## 📊 测试结果

最新的测试结果请查看 [TEST_REPORT.md](TEST_REPORT.md)。

---

**开始使用**: 请先阅读 [USER_GUIDE.md](USER_GUIDE.md) 了解如何创建符合要求的Job执行器。