"""深度接口数据文件解析器 - 解析 x-www-form-urlencoded 格式的接口数据"""

import re

from test_deep.config_deep import (
    DEEP_API_NAME,
    DEEP_INTERFACE_DATA_FILE,
    DEEP_SIGNATURE,
    DEEP_TIMESTAMP,
    DEEP_USERNAME,
)

# 模板变量映射
FIXED_VARS = {
    'username': DEEP_USERNAME,
    'timestamp': DEEP_TIMESTAMP,
    'signature': DEEP_SIGNATURE,
    'api_name': DEEP_API_NAME,
}

# 匹配 body 字段名（小写字母/下划线开头，可含 [数字]）
_FIELD_RE = re.compile(r'^([\w][\w\[\]]*)\s*:(.*)')


def _resolve(value):
    """替换 {{variable}} 模板变量"""
    for k, v in FIXED_VARS.items():
        value = value.replace('{{' + k + '}}', v)
    return value


def parse_deep_interfaces(file_path=None):
    """解析深度接口数据文件，返回接口列表：
    [{'name': str, 'url': str, 'body': {key: value}}, ...]
    """
    if file_path is None:
        file_path = DEEP_INTERFACE_DATA_FILE

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    interfaces = []
    current = None
    in_body = False

    for raw_line in lines:
        line = raw_line.rstrip('\n\r')

        # 新的编号接口节：n、名称
        m = re.match(r'^(\d+)、(.+)', line)
        if m:
            if current and current['url']:
                interfaces.append(current)
            current = {'name': m.group(2).strip(), 'url': '', 'body': {}}
            in_body = False
            continue

        if current is None:
            continue

        # URL 行
        if line.strip() == 'URL:':
            in_body = False
            continue

        # Body 行
        if line.strip() == 'Body:':
            in_body = True
            continue

        # http 行 = URL 值
        if line.startswith('http'):
            current['url'] = line.strip()
            in_body = False
            continue

        # Body 字段
        if in_body:
            m2 = _FIELD_RE.match(line)
            if m2:
                key = m2.group(1).strip()
                value = _resolve(m2.group(2).strip())
                current['body'][key] = value

    # 添加最后一个
    if current and current['url']:
        interfaces.append(current)

    return interfaces


def get_by_name(interfaces, name):
    """按名称查找接口（模糊匹配），返回 body dict"""
    for iface in interfaces:
        if name in iface['name']:
            return iface['body']
    raise ValueError(f"未找到接口: {name}")


def get_by_index(interfaces, idx):
    """按序号获取接口（0-based），返回 body dict"""
    return interfaces[idx]['body']
