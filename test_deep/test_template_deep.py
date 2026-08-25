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


class TestTemplate:
    """深度接口-模板管理模块-7个接口"""

    # 模板新增v3 返回的 id
    template_id = None

    test_results_deep = []

    @pytest.mark.order(1)
    def test_01_template_add_v3(self, client, interfaces):
        """模板新增v3"""
        iface = interfaces[22]
        response = run_case(
            self.test_results_deep, client, '模板新增v3',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板新增v3失败: code={response.get('code')}, msg={response.get('msg')}"
        )
        data = response.get("data", {})
        tid = data.get("id") if isinstance(data, dict) else None
        assert tid is not None, f"模板新增v3未返回 id, response={response}"
        TestTemplate.template_id = tid

    @pytest.mark.order(2)
    def test_02_template_edit_v3(self, client, interfaces):
        """模板编辑v3，id 取模板新增v3返回的 id"""
        iface = interfaces[23]
        body = iface['body'].copy()
        if TestTemplate.template_id is not None:
            body['id'] = str(TestTemplate.template_id)

        response = run_case(
            self.test_results_deep, client, '模板编辑v3',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板编辑v3失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(3)
    def test_03_template_query_v1(self, client, interfaces):
        """模板查询v1，id 取模板新增v3返回的 id"""
        iface = interfaces[24]
        body = iface['body'].copy()
        if TestTemplate.template_id is not None:
            body['id'] = str(TestTemplate.template_id)

        response = run_case(
            self.test_results_deep, client, '模板查询v1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板查询v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(4)
    def test_04_template_list_v1(self, client, interfaces):
        """模板列表v1"""
        iface = interfaces[25]
        response = run_case(
            self.test_results_deep, client, '模板列表v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板列表v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(5)
    def test_05_template_query_type_enum_v1(self, client, interfaces):
        """模板枚举查询v1"""
        iface = interfaces[26]
        response = run_case(
            self.test_results_deep, client, '模板枚举查询v1',
            iface['url'], iface['body'],
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板枚举查询v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(6)
    def test_06_template_update_link_material_v1(self, client, interfaces):
        """模板更新引流材料v1，id 取模板新增v3返回的 id"""
        iface = interfaces[27]
        body = iface['body'].copy()
        if TestTemplate.template_id is not None:
            body['id'] = str(TestTemplate.template_id)

        response = run_case(
            self.test_results_deep, client, '模板更新引流材料v1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板更新引流材料v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )

    @pytest.mark.order(7)
    def test_07_template_delete_v1(self, client, interfaces):
        """模板删除v1，id 取模板新增v3返回的 id"""
        iface = interfaces[28]
        body = iface['body'].copy()
        if TestTemplate.template_id is not None:
            body['id'] = str(TestTemplate.template_id)

        response = run_case(
            self.test_results_deep, client, '模板删除v1',
            iface['url'], body,
        )
        assert response.get("code") == EXPECTED_CODE, (
            f"模板删除v1失败: code={response.get('code')}, msg={response.get('msg')}"
        )


if __name__ == '__main__':
    pytest.main(['-v', '-s', __file__])
