import pytest

from config import (
    API_SIGNATURE_ADD,
    API_SIGNATURE_DELETE,
    API_SIGNATURE_DETAIL,
    API_SIGNATURE_LIST,
    API_SIGNATURE_OPERATOR_REJECT_REASON,
    API_SIGNATURE_REAL_NAME_UPDATE,
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


class TestSignature:
    """签名管理接口自动化测试"""

    # 模块级变量，存储签名新增返回的 signId
    sign_id = None

    # 收集所有测试请求/响应详情，用于生成报告
    test_results = []

    @pytest.mark.order(1)
    def test_signature_add(self, client, interface_data):
        """测试签名新增接口，并提取 signId 供后续接口使用"""
        response = run_case(
            self.test_results, client, '签名新增',
            API_SIGNATURE_ADD, interface_data['signature']['add'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名新增失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        assert "data" in response, "签名新增响应缺少 data 字段"

        data = response["data"]
        sign_id = data.get("signId") if isinstance(data, dict) else None
        assert sign_id is not None, f"签名新增未返回 signId, response={response}"

        TestSignature.sign_id = sign_id

    @pytest.mark.order(2)
    def test_signature_real_name_update(self, client, interface_data):
        """测试签名实名更新接口，signId 固定使用 11950242"""
        body = interface_data['signature']['real_name_update'].copy()
        body['signId'] = 11950242

        response = run_case(
            self.test_results, client, '签名实名更新',
            API_SIGNATURE_REAL_NAME_UPDATE, body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名实名更新失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(3)
    def test_signature_list(self, client, interface_data):
        """测试分页查询签名接口"""
        response = run_case(
            self.test_results, client, '分页查询签名',
            API_SIGNATURE_LIST, interface_data['signature']['list'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"分页查询签名失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(4)
    def test_signature_detail(self, client, interface_data):
        """测试签名详情接口，signId 优先取签名新增返回值，否则用文件中的值"""
        body = interface_data['signature']['detail'].copy()
        if TestSignature.sign_id is not None:
            body['signId'] = TestSignature.sign_id

        response = run_case(
            self.test_results, client, '签名详情',
            API_SIGNATURE_DETAIL, body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名详情失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(5)
    def test_signature_operator_reject_reason(self, client, interface_data):
        """测试签名运营商驳回原因接口，signIds 优先取签名新增返回值，否则用文件中的值"""
        body = interface_data['signature']['operator_reject_reason'].copy()
        if TestSignature.sign_id is not None:
            body['signIds'] = [TestSignature.sign_id]

        response = run_case(
            self.test_results, client, '签名运营商驳回原因',
            API_SIGNATURE_OPERATOR_REJECT_REASON, body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名运营商驳回原因接口失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(6)
    def test_signature_delete(self, client, interface_data):
        """测试签名删除接口，signId 优先取签名新增返回值，否则用文件中的值"""
        delete_body = interface_data['signature']['delete'].copy()
        if TestSignature.sign_id is not None:
            delete_body['signId'] = TestSignature.sign_id

        response = run_case(
            self.test_results, client, '签名删除',
            API_SIGNATURE_DELETE, delete_body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名删除失败: code={response.get('code')}, msg={response.get('msg')}"
        )


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
