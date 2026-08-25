import pytest

from test_deep.config_deep import EXPECTED_CODE
from test_deep.conftest import run_case
from test_deep.deep_client import DeepClient
from test_deep.deep_parser import get_by_index, parse_deep_interfaces


@pytest.fixture(scope="module")
def client():
    return DeepClient()


@pytest.fixture(scope="module")
def interfaces():
    return parse_deep_interfaces()


class TestQualification:
    """深度接口-资质管理模块-11个接口"""

    # 资质新增v2 返回的 id
    qual_v2_id = None
    # 资质新增v1 返回的 id
    qual_v1_id = None

    test_results_deep = []

    # =================== V2 流程 ===================

    @pytest.mark.order(1)
    def test_01_qualification_add_v2(self, client, interfaces):
        """资质新增v2"""
        iface = interfaces[0]
        response = run_case(
            self.test_results_deep, client, '资质新增v2',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质新增v2失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        qid = data.get("id") or data.get("endCustomerId") if isinstance(data, dict) else None
        assert qid is not None, f"资质新增v2未返回 id, response={response}"
        TestQualification.qual_v2_id = qid

    @pytest.mark.order(2)
    def test_02_qualification_list_v1(self, client, interfaces):
        """资质列表v1"""
        iface = interfaces[1]
        response = run_case(
            self.test_results_deep, client, '资质列表v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质列表v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(3)
    def test_03_qualification_edit_v2(self, client, interfaces):
        """资质编辑v2，end_customer_id 取资质新增v2返回的 id"""
        iface = interfaces[2]
        body = iface['body'].copy()
        if TestQualification.qual_v2_id is not None:
            body['end_customer_id'] = str(TestQualification.qual_v2_id)

        response = run_case(
            self.test_results_deep, client, '资质编辑v2',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质编辑v2失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(4)
    def test_04_qualification_change_log_v1(self, client, interfaces):
        """资质变更查询v1"""
        iface = interfaces[3]
        body = iface['body'].copy()
        if TestQualification.qual_v2_id is not None:
            body['end_customer_id'] = str(TestQualification.qual_v2_id)

        response = run_case(
            self.test_results_deep, client, '资质变更查询v1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质变更查询v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(5)
    def test_05_qualification_delete_v1(self, client, interfaces):
        """资质删除v1，end_customer_id 取资质新增v2返回的 id"""
        iface = interfaces[4]
        body = iface['body'].copy()
        if TestQualification.qual_v2_id is not None:
            body['end_customer_id'] = str(TestQualification.qual_v2_id)

        response = run_case(
            self.test_results_deep, client, '资质删除v1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质删除v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    # =================== V1 流程 ===================

    @pytest.mark.order(6)
    def test_06_qualification_add_v1(self, client, interfaces):
        """资质新增v1"""
        iface = interfaces[5]
        response = run_case(
            self.test_results_deep, client, '资质新增v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质新增v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        qid = data.get("id") or data.get("endCustomerId") if isinstance(data, dict) else None
        assert qid is not None, f"资质新增v1未返回 id, response={response}"
        TestQualification.qual_v1_id = qid

    @pytest.mark.order(7)
    def test_07_qualification_edit_v1(self, client, interfaces):
        """资质编辑v1，end_customer_id 取资质新增v1返回的 id"""
        iface = interfaces[6]
        body = iface['body'].copy()
        if TestQualification.qual_v1_id is not None:
            body['end_customer_id'] = str(TestQualification.qual_v1_id)

        response = run_case(
            self.test_results_deep, client, '资质编辑v1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质编辑v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(8)
    def test_08_qualification_delete_v1_1(self, client, interfaces):
        """资质删除v1-1，end_customer_id 取资质新增v1返回的 id"""
        iface = interfaces[7]
        body = iface['body'].copy()
        if TestQualification.qual_v1_id is not None:
            body['end_customer_id'] = str(TestQualification.qual_v1_id)

        response = run_case(
            self.test_results_deep, client, '资质删除v1-1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"资质删除v1-1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    # =================== 老接口流程 ===================

    @pytest.mark.order(9)
    def test_09_old_qualification_add_v1(self, client, interfaces):
        """老接口-资质新增v1"""
        iface = interfaces[8]
        response = run_case(
            self.test_results_deep, client, '老接口-资质新增v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"老接口-资质新增v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(10)
    def test_10_old_qualification_add_v2(self, client, interfaces):
        """老接口-资质新增v2"""
        iface = interfaces[9]
        response = run_case(
            self.test_results_deep, client, '老接口-资质新增v2',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"老接口-资质新增v2失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(11)
    def test_11_old_qualification_list_v1(self, client, interfaces):
        """老接口-资质列表v1"""
        iface = interfaces[10]
        response = run_case(
            self.test_results_deep, client, '老接口-资质列表v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"老接口-资质列表v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
