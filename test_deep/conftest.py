import json
import os
from datetime import datetime

from test_deep.config_deep import EXPECTED_CODE


def run_case(results, client, name, url, body):
    """执行单个深度接口用例并记录结果。返回响应 JSON。"""
    start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    record = {
        'name': name,
        'time': start_time,
        'end_time': '',
        'url': url,
        'headers': {},
        'body': body,
        'response': {},
        'passed': False,
    }
    try:
        response, req_url, headers, req_body = client.post(url, body)
        record['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record['url'] = req_url
        record['headers'] = headers
        record['body'] = req_body
        record['response'] = response
        record['passed'] = response.get('code') == EXPECTED_CODE
        results.append(record)
        return response
    except Exception as e:
        record['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record['response'] = {'error': f'{type(e).__name__}: {e}'}
        results.append(record)
        raise


def pytest_sessionfinish(session, exitstatus):
    """测试结束后生成深度接口 HTML 报告"""
    all_results = []
    seen_classes = set()
    for item in session.items:
        cls = getattr(item, 'cls', None)
        if cls and hasattr(cls, 'test_results_deep') and cls not in seen_classes:
            seen_classes.add(cls)
            all_results.extend(cls.test_results_deep)

    if not all_results:
        return

    report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    total = len(all_results)
    passed = sum(1 for r in all_results if r['passed'])
    failed = total - passed

    rows_html = ''
    for i, r in enumerate(all_results, 1):
        status = 'PASS' if r['passed'] else 'FAIL'
        status_color = '#28a745' if r['passed'] else '#dc3545'
        status_icon = '&#10004;' if r['passed'] else '&#10008;'

        req_headers = _format_json(r['headers'])
        req_body = _format_json(r['body'])
        resp_body = _format_json(r['response'])

        rows_html += f'''
        <tr class="result-row">
            <td>{i}</td>
            <td><strong>{r['name']}</strong></td>
            <td><span class="status-badge" style="background:{status_color}">{status_icon} {status}</span></td>
            <td><code>{r['time']}</code><br><code>{r['end_time']}</code></td>
            <td><code class="url">{r['url']}</code></td>
            <td>
                <details>
                    <summary class="toggle">Headers</summary>
                    <pre class="json-block">{req_headers}</pre>
                </details>
            </td>
            <td>
                <details>
                    <summary class="toggle">Body</summary>
                    <pre class="json-block">{req_body}</pre>
                </details>
            </td>
            <td>
                <details>
                    <summary class="toggle">Response</summary>
                    <pre class="json-block">{resp_body}</pre>
                </details>
            </td>
        </tr>'''

    env_url = all_results[0]['url'].split('/apis')[0] if all_results else 'N/A'
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>深度接口自动化测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
               background: #f4f6f9; color: #333; padding: 24px; }}
        .header {{ background: linear-gradient(135deg, #6c5ce7, #a29bfe); color: #fff;
                   padding: 28px 32px; border-radius: 10px; margin-bottom: 24px; }}
        .header h1 {{ font-size: 22px; margin-bottom: 8px; }}
        .header .meta {{ font-size: 13px; opacity: 0.85; }}
        .summary {{ display: flex; gap: 16px; margin-bottom: 24px; }}
        .summary .card {{ background: #fff; border-radius: 8px; padding: 18px 24px;
                          flex: 1; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
                          text-align: center; }}
        .card .num {{ font-size: 32px; font-weight: 700; }}
        .card .label {{ font-size: 13px; color: #666; margin-top: 4px; }}
        .card.total .num {{ color: #6c5ce7; }}
        .card.pass .num {{ color: #28a745; }}
        .card.fail .num {{ color: #dc3545; }}
        table {{ width: 100%; border-collapse: collapse; background: #fff;
                 border-radius: 8px; overflow: hidden;
                 box-shadow: 0 1px 4px rgba(0,0,0,0.08); }}
        th {{ background: #f0f3f7; padding: 12px 14px; text-align: left;
              font-size: 13px; color: #555; border-bottom: 2px solid #e0e4ea; }}
        td {{ padding: 12px 14px; border-bottom: 1px solid #eee; font-size: 13px;
              vertical-align: top; }}
        .result-row:hover {{ background: #f8fafd; }}
        .url {{ word-break: break-all; font-size: 12px; color: #6c5ce7; }}
        .status-badge {{ display: inline-block; padding: 3px 10px; border-radius: 12px;
                         color: #fff; font-size: 12px; font-weight: 600; }}
        .toggle {{ cursor: pointer; color: #6c5ce7; font-size: 12px; font-weight: 600;
                   user-select: none; }}
        .toggle:hover {{ text-decoration: underline; }}
        .json-block {{ background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px;
                       padding: 10px; font-size: 11px; line-height: 1.5;
                       max-height: 300px; overflow: auto; white-space: pre-wrap;
                       word-break: break-all; margin-top: 6px; display: none; }}
        details[open] .json-block {{ display: block; }}
        .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 24px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>深度接口自动化测试报告</h1>
        <div class="meta">报告生成时间：{report_time} &nbsp;|&nbsp; 测试环境：{env_url}</div>
    </div>

    <div class="summary">
        <div class="card total"><div class="num">{total}</div><div class="label">总计用例</div></div>
        <div class="card pass"><div class="num">{passed}</div><div class="label">通过</div></div>
        <div class="card fail"><div class="num">{failed}</div><div class="label">失败</div></div>
    </div>

    <table>
        <thead>
            <tr>
                <th style="width:36px">#</th>
                <th>接口名称</th>
                <th>结果</th>
                <th>执行时间</th>
                <th>请求 URL</th>
                <th>Headers</th>
                <th>Body</th>
                <th>响应内容</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <div class="footer">深度接口自动化测试报告 &copy; {datetime.now().year}</div>
</body>
</html>'''

    report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    os.makedirs(report_dir, exist_ok=True)
    report_file = os.path.join(report_dir, 'report_deep.html')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'\n{"="*60}')
    print(f' 深度接口测试报告已生成: {report_file}')
    print(f'{"="*60}')


def _json_safe(obj):
    """将对象安全转为可 JSON 序列化的格式，base64 图片数据截断"""
    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            if isinstance(v, str) and len(v) > 200 and (
                v.startswith('data:image') or v.startswith('base64,') or v.startswith('/9j')
            ):
                result[k] = v[:50] + '...[base64已截断]'
            else:
                result[k] = _json_safe(v)
        return result
    elif isinstance(obj, list):
        return [_json_safe(item) for item in obj]
    return obj


def _format_json(obj):
    """格式化 JSON，截断 base64 数据"""
    return json.dumps(_json_safe(obj), ensure_ascii=False, indent=4)
