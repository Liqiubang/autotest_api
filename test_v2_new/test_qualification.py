import pytest

from config import (
    API_QUALIFICATION_ADD,
    API_QUALIFICATION_CHANGE_LOG_LIST,
    API_QUALIFICATION_DELETE,
    API_QUALIFICATION_LIST,
    API_QUALIFICATION_UPDATE,
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


class TestQualification:
    """资质管理接口自动化测试"""

    # 模块级变量，存储资质新增返回的 endCustomerId
    end_customer_id = None

    # 收集所有测试请求/响应详情，用于生成报告
    test_results = []

    @pytest.mark.order(1)
    def test_qualification_list(self, client, interface_data):
        """测试分页查询资质接口"""
        response = run_case(
            self.test_results, client, '分页查询资质',
            API_QUALIFICATION_LIST, interface_data['qualification']['list'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"分页查询资质失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(2)
    def test_qualification_add(self, client, interface_data):
        """测试资质新增接口，并提取 endCustomerId 供后续接口使用"""
        response = run_case(
            self.test_results, client, '资质新增',
            API_QUALIFICATION_ADD, interface_data['qualification']['add'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质新增失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        assert "data" in response, "资质新增响应缺少 data 字段"

        data = response["data"]
        end_customer_id = data.get("endCustomerId") if isinstance(data, dict) else None
        assert end_customer_id is not None, f"资质新增未返回 endCustomerId, response={response}"

        TestQualification.end_customer_id = end_customer_id

    @pytest.mark.order(3)
    def test_qualification_update(self, client, interface_data):
        """测试资质编辑接口，endCustomerId 优先取资质新增返回值，否则用文件中的值"""
        update_body = interface_data['qualification']['update'].copy()
        if TestQualification.end_customer_id is not None:
            update_body['endCustomerId'] = TestQualification.end_customer_id

        response = run_case(
            self.test_results, client, '资质编辑',
            API_QUALIFICATION_UPDATE, update_body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质编辑失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(4)
    def test_qualification_change_log_list(self, client, interface_data):
        """测试资质变更记录接口，endCustomerId 优先取资质新增返回值，否则用文件中的值"""
        body = interface_data['qualification']['change_log_list'].copy()
        if TestQualification.end_customer_id is not None:
            body['endCustomerId'] = TestQualification.end_customer_id

        response = run_case(
            self.test_results, client, '资质变更记录',
            API_QUALIFICATION_CHANGE_LOG_LIST, body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质变更记录查询失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(5)
    def test_qualification_delete(self, client, interface_data):
        """测试资质删除接口，endCustomerId 优先取资质新增返回值，否则用文件中的值"""
        delete_body = interface_data['qualification']['delete'].copy()
        if TestQualification.end_customer_id is not None:
            delete_body['endCustomerId'] = TestQualification.end_customer_id

        response = run_case(
            self.test_results, client, '资质删除',
            API_QUALIFICATION_DELETE, delete_body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质删除失败: code={response.get('code')}, msg={response.get('msg')}"
        )


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
