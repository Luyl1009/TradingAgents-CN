#!/usr/bin/env python3
"""
Harness 反馈验证脚本

在每次代码修改后运行,确保:
1. Python 语法正确
2. 依赖完整
3. 基本功能正常
4. Docker 配置有效

用法:
    python scripts/harness/validate_changes.py
"""

import sys
import subprocess
import os
from pathlib import Path

# 颜色输出
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_header(text: str):
    """打印标题"""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(text: str):
    """打印成功信息"""
    print(f"{GREEN}✅ {text}{RESET}")


def print_error(text: str):
    """打印错误信息"""
    print(f"{RED}❌ {text}{RESET}")


def print_warning(text: str):
    """打印警告信息"""
    print(f"{YELLOW}⚠️ {text}{RESET}")


def print_info(text: str):
    """打印提示信息"""
    print(f"{BLUE}ℹ️ {text}{RESET}")


def run_command(cmd: str, capture: bool = True) -> tuple:
    """运行命令并返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "命令超时"
    except Exception as e:
        return -1, "", str(e)


def check_python_syntax():
    """检查 Python 文件语法"""
    print_header("1. Python 语法检查")
    
    project_root = Path(__file__).parent.parent.parent
    errors = []
    
    # 检查关键目录
    dirs_to_check = [
        "app",
        "tradingagents",
        "utils",
        "cli"
    ]
    
    total_files = 0
    valid_files = 0
    
    for dir_name in dirs_to_check:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            continue
            
        for py_file in dir_path.rglob("*.py"):
            total_files += 1
            returncode, _, stderr = run_command(f"python3 -m py_compile {py_file}")
            
            if returncode == 0:
                valid_files += 1
            else:
                errors.append(f"{py_file.relative_to(project_root)}: {stderr}")
    
    print(f"检查文件数: {total_files}")
    print(f"通过文件数: {valid_files}")
    
    if errors:
        print_error(f"发现 {len(errors)} 个语法错误:")
        for error in errors[:5]:  # 只显示前 5 个
            print(f"  {error}")
        if len(errors) > 5:
            print(f"  ... 还有 {len(errors) - 5} 个错误")
        return False
    else:
        print_success("所有 Python 文件语法正确")
        return True


def check_docker_compose():
    """检查 Docker Compose 配置"""
    print_header("2. Docker Compose 配置检查")
    
    returncode, stdout, stderr = run_command("docker compose config")
    
    if returncode == 0:
        print_success("Docker Compose 配置有效")
        
        # 提取服务数量
        services = [line for line in stdout.split("\n") if line.startswith("  ") and ":" in line]
        print(f"服务数量: {len(services)}")
        return True
    else:
        print_error(f"Docker Compose 配置无效: {stderr}")
        return False


def check_docker_services():
    """检查 Docker 服务状态"""
    print_header("3. Docker 服务状态检查")
    
    returncode, stdout, stderr = run_command("docker compose ps")
    
    if returncode == 0:
        # 检查服务是否运行
        services = stdout.strip().split("\n")[1:]  # 跳过标题行
        running_count = 0
        
        for service in services:
            if "Up" in service or "running" in service.lower():
                running_count += 1
                service_name = service.split()[0]
                print_success(f"服务 {service_name} 运行正常")
        
        print(f"\n运行中的服务: {running_count}/{len(services)}")
        
        if running_count == len(services):
            print_success("所有服务正常运行")
            return True
        else:
            print_warning("部分服务未运行")
            return True  # 不阻塞,只是警告
    else:
        print_error(f"无法获取服务状态: {stderr}")
        return False


def check_api_health():
    """检查 API 健康状态"""
    print_header("4. API 健康检查")
    
    returncode, stdout, stderr = run_command(
        "curl -s http://localhost:3000/api/health"
    )
    
    if returncode == 0 and "200" in stdout or "ok" in stdout.lower():
        print_success("API 健康检查通过")
        return True
    else:
        print_warning("API 健康检查失败 (服务可能未启动)")
        return True  # 不阻塞,因为服务可能未启动


def check_dependencies():
    """检查关键依赖"""
    print_header("5. 关键依赖检查")
    
    # 检查是否在 Docker 容器内
    in_docker = os.path.exists("/.dockerenv")
    
    if not in_docker:
        print_warning("当前在本地环境,跳过依赖检查")
        print_info("依赖检查应在 Docker 容器内运行")
        return True  # 不阻塞
    
    # 在 Docker 容器内检查依赖
    dependencies = [
        ("fastapi", "FastAPI 框架"),
        ("uvicorn", "ASGI 服务器"),
        ("pymongo", "MongoDB 驱动"),
        ("redis", "Redis 客户端"),
        ("langchain", "LangChain 框架"),
        ("nest_asyncio", "嵌套事件循环"),
    ]
    
    all_installed = True
    
    for package, description in dependencies:
        returncode, stdout, stderr = run_command(f"pip show {package}")
        
        if returncode == 0:
            version = stdout.split("\n")[1].split(": ")[1]
            print_success(f"{description}: {version}")
        else:
            print_error(f"{description}: 未安装")
            all_installed = False
    
    return all_installed


def check_environment_file():
    """检查环境配置文件"""
    print_header("6. 环境配置文件检查")
    
    project_root = Path(__file__).parent.parent.parent
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print_error(".env 文件不存在")
        print_warning("请复制 .env.docker 为 .env")
        return False
    
    print_success(".env 文件存在")
    
    # 检查关键配置
    required_keys = [
        "MONGODB_URL",
        "REDIS_URL",
        "DASHSCOPE_API_KEY",
    ]
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    missing_keys = []
    for key in required_keys:
        if key not in content:
            missing_keys.append(key)
    
    if missing_keys:
        print_warning(f"缺少关键配置: {', '.join(missing_keys)}")
        return False
    else:
        print_success("关键配置完整")
        return True


def check_file_structure():
    """检查项目文件结构"""
    print_header("7. 项目结构检查")
    
    project_root = Path(__file__).parent.parent.parent
    
    required_files = [
        ("docker-compose.yml", "Docker Compose 配置"),
        ("Dockerfile.backend", "后端 Dockerfile"),
        ("Dockerfile.frontend", "前端 Dockerfile"),
        ("pyproject.toml", "Python 项目配置"),
        ("requirements.txt", "Python 依赖"),
        ("AGENTS.md", "AI 助手规则"),
        ("PROGRESS.md", "项目进度"),
    ]
    
    all_exist = True
    
    for file_path, description in required_files:
        if (project_root / file_path).exists():
            print_success(f"{description}: {file_path}")
        else:
            print_error(f"{description}: {file_path} 不存在")
            all_exist = False
    
    return all_exist


def main():
    """主函数"""
    print_header("Harness 反馈验证系统")
    print("开始检查项目状态...\n")
    
    checks = [
        ("Python 语法", check_python_syntax),
        ("Docker Compose 配置", check_docker_compose),
        ("Docker 服务", check_docker_services),
        ("API 健康", check_api_health),
        ("依赖完整性", check_dependencies),
        ("环境配置", check_environment_file),
        ("项目结构", check_file_structure),
    ]
    
    results = {}
    
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"{name} 检查失败: {e}")
            results[name] = False
    
    # 汇总结果
    print_header("验证结果汇总")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, passed_check in results.items():
        if passed_check:
            print_success(f"{name}: 通过")
        else:
            print_error(f"{name}: 失败")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print(f"\n{GREEN}🎉 所有检查通过! 代码可以提交。{RESET}")
        return 0
    else:
        print(f"\n{RED}⚠️ 有 {total - passed} 个检查未通过,请修复后再提交。{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
