#!/bin/bash

echo "=== Job Manager 测试运行器 ==="

# 获取脚本所在目录与仓库根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRATE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$CRATE_ROOT/../.." && pwd)"

# 检查参数
TEST_TYPE=${1:-"quick"}
JOB_MANAGER_URL=${2:-"https://www.zkyhxl.cn:8443"}
HEADERS_PROFILE=${JOB_HEADERS_PROFILE:-"platform_admin"}
HEADERS_FILE=${JOB_HEADERS_FILE:-"$SCRIPT_DIR/test_headers.json"}

echo "脚本目录: $SCRIPT_DIR"
echo "测试类型: $TEST_TYPE"
echo "Job Manager URL: $JOB_MANAGER_URL"

# 检查Python环境
echo ""
echo "1. 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# 检查依赖
echo ""
echo "2. 检查Python依赖..."
if ! python3 -c "import aiohttp" 2>/dev/null; then
    echo "⚠️  aiohttp 未安装，正在安装..."
    if command -v pip3 &> /dev/null; then
        pip3 install aiohttp
    else
        echo "❌ pip3 未安装，请手动安装 aiohttp"
        exit 1
    fi
fi
echo "✅ Python依赖检查完成"

# 检查Job Manager服务器
echo ""
echo "3. 检查Job Manager服务器..."
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$JOB_MANAGER_URL/api/v1/jobs/health")
case "$HEALTH_STATUS" in
    200)
        echo "✅ Job Manager服务器响应正常"
        ;;
    401|403)
        echo "⚠️  Job Manager健康检查返回 $HEALTH_STATUS（可能需要测试头），继续执行 Python 测试验证..."
        ;;
    *)
        echo "❌ Job Manager服务器未正常响应 (HTTP $HEALTH_STATUS)"
        echo "请检查服务是否已启动: (cd $REPO_ROOT && cargo run --bin zkeh-server)"
        ;;
esac

# 根据测试类型运行不同的测试
echo ""
echo "4. 运行测试..."

case $TEST_TYPE in
    "quick")
        PROFILE_OVERRIDE=${3:-"$HEADERS_PROFILE"}
        echo "🚀 运行快速测试 (headers profile: $PROFILE_OVERRIDE)..."
        JOB_TEST_URL="$JOB_MANAGER_URL" \
        JOB_TEST_HEADERS_PROFILE="$PROFILE_OVERRIDE" \
        JOB_TEST_HEADERS_FILE="$HEADERS_FILE" \
        python3 "$SCRIPT_DIR/simple_test.py" --print-headers
        ;;
    
    "executor")
        echo "⚙️  启动任务执行器..."
        EXECUTOR_ID=${3:-"test-executor-$(date +%s)"}
        MAX_JOBS=${4:-2}
        PROFILE_OVERRIDE=${5:-"$HEADERS_PROFILE"}
        echo "执行器ID: $EXECUTOR_ID"
        echo "最大并发任务: $MAX_JOBS"
        echo "Headers profile: $PROFILE_OVERRIDE"
        python3 "$SCRIPT_DIR/simple_job_executor.py" \
            --executor-id "$EXECUTOR_ID" \
            --job-manager-url "$JOB_MANAGER_URL" \
            --max-jobs "$MAX_JOBS" \
            --headers-profile "$PROFILE_OVERRIDE" \
            --headers-file "$HEADERS_FILE"
        ;;
    
    "help")
        echo "📖 使用方法:"
        echo "  $0 [测试类型] [Job Manager URL] [执行器ID] [最大任务数]"
        echo ""
        echo "可用的测试类型:"
        echo "  quick     - 快速测试 (默认)"
        echo "  executor  - 启动任务执行器"
        echo "  help      - 显示帮助"
        echo ""
        echo "示例:"
        echo "  $0 quick"
        echo "  $0 executor https://www.zkyhxl.cn:8443 my-executor 3"
        ;;
    
    *)
        echo "❌ 未知的测试类型: $TEST_TYPE"
        echo "运行 '$0 help' 查看帮助"
        exit 1
        ;;
esac

echo ""
echo "=== 测试运行器完成 ==="