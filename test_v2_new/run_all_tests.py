"""一键运行 test_v2_new 目录下所有测试文件"""
import os
import pytest


if __name__ == '__main__':
    # 获取项目根目录（test_v2_new 的父目录）
    test_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(test_dir)

    # 切换到项目根目录，确保 conftest.py 能被加载
    os.chdir(project_root)

    pytest.main(['-v', '-s', '--order-scope=class', test_dir])
