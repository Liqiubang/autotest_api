import json


def _extract_body(content, start_idx):
    """从 start_idx 往后找 Body: 之后的 JSON 对象"""
    body_start = content.find('Body:', start_idx)
    if body_start < 0:
        return None
    brace_start = content.find('{', body_start)
    if brace_start < 0:
        return None
    depth = 0
    brace_end = -1
    for i in range(brace_start, len(content)):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                brace_end = i
                break
    if brace_end < 0:
        return None
    body_text = content[brace_start:brace_end + 1].replace('\t', '    ')
    return json.loads(body_text)


def parse_interface_data(file_path):
    """从接口数据文件中解析各接口的请求体，返回按模块分组的字典"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    base = 'http://172.16.42.128:8080/sms/v2'

    all_apis = {
        'qualification': {
            'list': '/qualification/list',
            'add': '/qualification/add',
            'update': '/qualification/update',
            'delete': '/qualification/delete',
            'change_log_list': '/qualification/change-log/list',
        },
        'signature': {
            'add': '/signature/add',
            'real_name_update': '/signature/real-name-update',
            'list': '/signature/list',
            'detail': '/signature/detail',
            'operator_reject_reason': '/signature/operator-reject-reason',
            'delete': '/signature/delete',
        },
        'template': {
            'add': '/template/add',
            'update': '/template/update',
            'detail': '/template/detail',
            'list': '/template/list',
            'query_type_enum': '/template/query-type-enum',
            'operator_reject_reason': '/template/operator-reject-reason',
            'delete': '/template/delete',
        },
    }

    result = {}
    for module, apis in all_apis.items():
        sections = {}
        for key, url_path in apis.items():
            idx = content.find(base + url_path)
            if idx < 0:
                continue
            body = _extract_body(content, idx)
            if body is not None:
                sections[key] = body
        result[module] = sections

    return result
