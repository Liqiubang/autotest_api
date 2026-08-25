# 接口自动化测试配置

# 环境变量（对应前置脚本中的配置）
APP_ID = "DEV_JDWQHYR9JHF"          # 替换为实际的 AppId
APP_SECRET = "xv4xi288m50p7nl0nr6s1a10h3m2ldga"  # 替换为实际的 AppSecret

# 服务地址
BASE_URL = "http://172.16.42.128:8080"

# 接口路径
API_QUALIFICATION_LIST = "/sms/v2/qualification/list"
API_QUALIFICATION_ADD = "/sms/v2/qualification/add"
API_QUALIFICATION_UPDATE = "/sms/v2/qualification/update"
API_QUALIFICATION_DELETE = "/sms/v2/qualification/delete"
API_QUALIFICATION_CHANGE_LOG_LIST = "/sms/v2/qualification/change-log/list"

API_SIGNATURE_ADD = "/sms/v2/signature/create"
API_SIGNATURE_REAL_NAME_UPDATE = "/sms/v2/signature/real-name-update"
API_SIGNATURE_LIST = "/sms/v2/signature/list"
API_SIGNATURE_DETAIL = "/sms/v2/signature/detail"
API_SIGNATURE_OPERATOR_REJECT_REASON = "/sms/v2/signature/operator-reject-reason"
API_SIGNATURE_DELETE = "/sms/v2/signature/delete"

API_TEMPLATE_ADD = "/sms/v2/template/add"
API_TEMPLATE_UPDATE = "/sms/v2/template/update"
API_TEMPLATE_DETAIL = "/sms/v2/template/detail"
API_TEMPLATE_LIST = "/sms/v2/template/list"
API_TEMPLATE_QUERY_TYPE_ENUM = "/sms/v2/template/query-type-enum"
API_TEMPLATE_OPERATOR_REJECT_REASON = "/sms/v2/template/operator-reject-reason"
API_TEMPLATE_DELETE = "/sms/v2/template/delete"

# 期望响应码
EXPECTED_CODE = "000000"

# 接口数据文件路径
INTERFACE_DATA_FILE = r"C:\Users\15274\OneDrive\自助通统一接口自动化.txt"
