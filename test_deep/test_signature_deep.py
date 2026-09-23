import pytest

from test_deep.config_deep import EXPECTED_CODE
from test_deep.conftest import run_case
from test_deep.deep_client import DeepClient
from test_deep.deep_parser import parse_deep_interfaces


@pytest.fixture(scope="module")
def client():
    return DeepClient()


@pytest.fixture(scope="module")
def interfaces():
    return parse_deep_interfaces()


class TestSignature:
    """深度接口-签名管理模块-11个接口"""

    # 各版本签名新增返回的 id
    sig_v3_id = None
    sig_v4_id = None
    sig_v5_id = None
    sig_v6_id = None

    test_results_deep = []

    # =================== 签名新增/删除配对流程 ===================

    @pytest.mark.order(1)
    def test_01_signature_add_v3(self, client, interfaces):
        """签名新增v3"""
        iface = interfaces[11]
        response = run_case(
            self.test_results_deep, client, '签名新增v3',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名新增v3失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        sid = data.get("id") if isinstance(data, dict) else None
        assert sid is not None, f"签名新增v3未返回 id, response={response}"
        TestSignature.sig_v3_id = sid

    @pytest.mark.order(2)
    def test_02_signature_delete_v1_3(self, client, interfaces):
        """签名删除v1-3，id 取签名新增v3返回的 id"""
        iface = interfaces[12]
        body = iface['body'].copy()
        if TestSignature.sig_v3_id is not None:
            body['id'] = str(TestSignature.sig_v3_id)

        response = run_case(
            self.test_results_deep, client, '签名删除v1-3',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名删除v1-3失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(3)
    def test_03_signature_add_v4(self, client, interfaces):
        """签名新增v4"""
        iface = interfaces[13]
        response = run_case(
            self.test_results_deep, client, '签名新增v4',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名新增v4失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        sid = data.get("id") if isinstance(data, dict) else None
        assert sid is not None, f"签名新增v4未返回 id, response={response}"
        TestSignature.sig_v4_id = sid

    @pytest.mark.order(4)
    def test_04_signature_delete_v1_4(self, client, interfaces):
        """签名删除v1-4，id 取签名新增v4返回的 id"""
        iface = interfaces[14]
        body = iface['body'].copy()
        if TestSignature.sig_v4_id is not None:
            body['id'] = str(TestSignature.sig_v4_id)

        response = run_case(
            self.test_results_deep, client, '签名删除v1-4',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名删除v1-4失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(5)
    def test_05_signature_add_v5(self, client, interfaces):
        """签名新增v5"""
        iface = interfaces[15]
        response = run_case(
            self.test_results_deep, client, '签名新增v5',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名新增v5失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        sid = data.get("id") if isinstance(data, dict) else None
        assert sid is not None, f"签名新增v5未返回 id, response={response}"
        TestSignature.sig_v5_id = sid

    @pytest.mark.order(6)
    def test_06_signature_delete_v1_5(self, client, interfaces):
        """签名删除v1-5，id 取签名新增v5返回的 id"""
        iface = interfaces[16]
        body = iface['body'].copy()
        if TestSignature.sig_v5_id is not None:
            body['id'] = str(TestSignature.sig_v5_id)

        response = run_case(
            self.test_results_deep, client, '签名删除v1-5',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名删除v1-5失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(7)
    def test_07_signature_add_v6(self, client, interfaces):
        """签名新增v6"""
        iface = interfaces[17]
        response = run_case(
            self.test_results_deep, client, '签名新增v6',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名新增v6失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        sid = data.get("id") if isinstance(data, dict) else None
        assert sid is not None, f"签名新增v6未返回 id, response={response}"
        TestSignature.sig_v6_id = sid

    # =================== 签名实名修改 ===================

    @pytest.mark.order(8)
    def test_11_signature_real_name_modify_v3(self, client, interfaces):
        """签名实名修改v3，id 取签名新增v6返回的 id"""
        iface = interfaces[18]
        body = iface['body'].copy()
        if TestSignature.sig_v6_id is not None:
            body['id'] = str(TestSignature.sig_v6_id)

        response = run_case(
            self.test_results_deep, client, '签名实名修改v3',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名实名修改v3失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(9)
    def test_08_signature_delete_v1_6(self, client, interfaces):
        """签名删除v1-6，id 取签名新增v6返回的 id"""
        iface = interfaces[19]
        body = iface['body'].copy()
        if TestSignature.sig_v6_id is not None:
            body['id'] = str(TestSignature.sig_v6_id)

        response = run_case(
            self.test_results_deep, client, '签名删除v1-6',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名删除v1-6失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    # =================== 签名查询/列表 ===================

    @pytest.mark.order(10)
    def test_09_signature_query_v1(self, client, interfaces):
        """签名查询v1"""
        iface = interfaces[20]
        response = run_case(
            self.test_results_deep, client, '签名查询v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名查询v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(11)
    def test_10_signature_list_v1(self, client, interfaces):
        """签名列表v1"""
        iface = interfaces[21]
        response = run_case(
            self.test_results_deep, client, '签名列表v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"签名列表v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )




if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
