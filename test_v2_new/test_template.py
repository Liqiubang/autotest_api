import pytest

from config import (
    API_TEMPLATE_ADD,
    API_TEMPLATE_DELETE,
    API_TEMPLATE_DETAIL,
    API_TEMPLATE_LIST,
    API_TEMPLATE_OPERATOR_REJECT_REASON,
    API_TEMPLATE_QUERY_TYPE_ENUM,
    API_TEMPLATE_UPDATE,
    EXPECTED_CODE,
    INTERFACE_DATA_FILE,
)
from conftest import run_case
from interface_parser import parse_interface_data
from sms_client import SmsClient


@pytest.fixture(scope="module")
def client():
    return SmsClient()


@pytest.fixture(scope="module")
def interface_data():
    return parse_interface_data(INTERFACE_DATA_FILE)


class TestTemplate:
    """模板管理接口自动化测试"""

    # 模块级变量，存储模板新增返回的 templateCode
    template_code = None

    # 收集所有测试请求/响应详情，用于生成报告
    test_results = []

    @pytest.mark.order(1)
    def test_template_add(self, client, interface_data):
        """测试模板新增接口，并提取 templateCode 供后续接口使用"""
        response = run_case(
            self.test_results, client, '模板新增',
            API_TEMPLATE_ADD, interface_data['template']['add'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板新增失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        assert "data" in response, "模板新增响应缺少 data 字段"

        data = response["data"]
        template_code = data.get("templateCode") if isinstance(data, dict) else None
        assert template_code is not None, f"模板新增未返回 templateCode, response={response}"

        TestTemplate.template_code = template_code

    @pytest.mark.order(2)
    def test_template_update(self, client, interface_data):
        """测试模板编辑接口，templateCode 优先取模板新增返回值，否则用文件中的值"""
        update_body = interface_data['template']['update'].copy()
        if TestTemplate.template_code is not None:
            update_body['templateCode'] = TestTemplate.template_code

        response = run_case(
            self.test_results, client, '模板编辑',
            API_TEMPLATE_UPDATE, update_body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板编辑失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(3)
    def test_template_detail(self, client, interface_data):
        """测试模板详情接口，templateCode 优先取模板新增返回值，否则用文件中的值"""
        body = interface_data['template']['detail'].copy()
        if TestTemplate.template_code is not None:
            body['templateCode'] = TestTemplate.template_code

        response = run_case(
            self.test_results, client, '模板详情',
            API_TEMPLATE_DETAIL, body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板详情失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(4)
    def test_template_list(self, client, interface_data):
        """测试分页查询模板接口"""
        response = run_case(
            self.test_results, client, '分页查询模板',
            API_TEMPLATE_LIST, interface_data['template']['list'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"分页查询模板失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(5)
    def test_template_query_type_enum(self, client, interface_data):
        """测试模板查询类型枚举接口"""
        response = run_case(
            self.test_results, client, '模板查询类型枚举',
            API_TEMPLATE_QUERY_TYPE_ENUM,
            interface_data['template']['query_type_enum'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板查询类型枚举接口失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(6)
    def test_template_operator_reject_reason(self, client, interface_data):
        """测试模板运营商驳回原因接口，templateCodes 优先取模板新增返回值，否则用文件中的值"""
        body = interface_data['template']['operator_reject_reason'].copy()
        if TestTemplate.template_code is not None:
            body['templateCodes'] = [TestTemplate.template_code]

        response = run_case(
            self.test_results, client, '模板运营商驳回原因',
            API_TEMPLATE_OPERATOR_REJECT_REASON, body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板运营商驳回原因接口失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(7)
    def test_template_delete(self, client, interface_data):
        """测试模板删除接口，templateCode 优先取模板新增返回值，否则用文件中的值"""
        delete_body = interface_data['template']['delete'].copy()
        if TestTemplate.template_code is not None:
            delete_body['templateCode'] = TestTemplate.template_code

        response = run_case(
            self.test_results, client, '模板删除',
            API_TEMPLATE_DELETE, delete_body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板删除失败: code={response.get('code')}, msg={response.get('msg')}"
        )


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
