# Generated by Django 3.2.20 on 2023-09-19 12:33

from django.db import migrations


def update_admin_role(apps, schema_editor):
    IastRoleV2 = apps.get_model("dongtai_common", "IastRoleV2")

    new_admin_permission = {
        "routes": [
            "dashboard",
            "Dashboard",
            "deployment",
            "deploy",
            "project",
            "projectManage",
            "vulnList",
            "scaList",
            "agentManage",
            "scanList",
            "integrationManagement",
            "strategyBox",
            "strategyManage",
            "templateManage",
            "hookRule",
            "sensitiveManage",
            "projectTemplate",
            "systemSettings",
            "search",
            "center",
            "reportCenter",
            "vulnSharing",
            "links",
            "authority",
            "roleSetting",
            "team",
            "account",
            "license",
            "changeLogo",
            "logManage",
            "about",
        ],
        "buttons": [
            {"id": 1, "label": "新增项目"},
            {"id": 2, "label": "删除项目"},
            {"id": 3, "label": "编辑项目"},
            {"id": 4, "label": "生成报告"},
            {"id": 5, "label": "删除漏洞"},
            {"id": 6, "label": "关联漏洞"},
            {"id": 7, "label": "漏洞分享"},
            {"id": 8, "label": "状态变更"},
            {"id": 9, "label": "集成同步"},
            {"id": 58, "label": "下载调用链"},
            {"id": 59, "label": "请求重放"},
            {"id": 10, "label": "组件分享"},
            {"id": 11, "label": "启用"},
            {"id": 12, "label": "暂停"},
            {"id": 13, "label": "导出日志"},
            {"id": 14, "label": "批量升级"},
            {"id": 15, "label": "主动验证"},
            {"id": 16, "label": "熔断配置"},
            {"id": 17, "label": "IDE 插件"},
            {"id": 18, "label": "CI/CD 集成"},
            {"id": 19, "label": "缺陷管理"},
            {"id": 20, "label": "消息通知"},
            {"id": 21, "label": "其他"},
            {"id": 22, "label": "新增策略"},
            {"id": 23, "label": "编辑策略"},
            {"id": 24, "label": "删除策略"},
            {"id": 25, "label": "修改状态"},
            {"id": 26, "label": "新增模版"},
            {"id": 27, "label": "编辑模版"},
            {"id": 28, "label": "删除模版"},
            {"id": 29, "label": "修改状态"},
            {"id": 30, "label": "添加规则类型"},
            {"id": 31, "label": "添加规则"},
            {"id": 32, "label": "删除规则"},
            {"id": 33, "label": "修改状态"},
            {"id": 34, "label": "全部启用"},
            {"id": 35, "label": "全部禁用"},
            {"id": 36, "label": "全部删除"},
            {"id": 37, "label": "新增规则"},
            {"id": 38, "label": "编辑规则"},
            {"id": 39, "label": "删除规则"},
            {"id": 40, "label": "修改状态"},
            {"id": 41, "label": "新增配置"},
            {"id": 42, "label": "编辑模版"},
            {"id": 57, "label": "删除模版"},
            {"id": 43, "label": "只读"},
            {"id": 44, "label": "修改"},
            {"id": 45, "label": "新增角色"},
            {"id": 46, "label": "删除角色"},
            {"id": 47, "label": "编辑角色"},
            {"id": 48, "label": "新增项目组"},
            {"id": 49, "label": "删除项目组"},
            {"id": 50, "label": "编辑项目组"},
            {"id": 51, "label": "查看详情"},
            {"id": 52, "label": "新增账号"},
            {"id": 53, "label": "删除账号"},
            {"id": 54, "label": "编辑账号"},
            {"id": 55, "label": "查看详情"},
            {"id": 56, "label": "消息通知"},
        ],
    }
    new_user_permission = {
        "routes": [
            "dashboard",
            "Dashboard",
            "deployment",
            "deploy",
            "project",
            "projectManage",
            "vulnList",
            "scaList",
            "agentManage",
            "scanList",
            "integrationManagement",
            "strategyBox",
            "strategyManage",
            "templateManage",
            "hookRule",
            "sensitiveManage",
            "projectTemplate",
            "systemSettings",
            "search",
            "center",
            "reportCenter",
            "vulnSharing",
            "links",
            "authority",
            "roleSetting",
            "team",
            "account",
            "license",
            "changeLogo",
            "logManage",
            "about",
        ],
        "buttons": [
            {"id": 1, "label": "新增项目"},
            {"id": 2, "label": "删除项目"},
            {"id": 3, "label": "编辑项目"},
            {"id": 4, "label": "生成报告"},
            {"id": 5, "label": "删除漏洞"},
            {"id": 6, "label": "关联漏洞"},
            {"id": 7, "label": "漏洞分享"},
            {"id": 8, "label": "状态变更"},
            {"id": 9, "label": "集成同步"},
            {"id": 58, "label": "下载调用链"},
            {"id": 10, "label": "组件分享"},
            {"id": 11, "label": "启用"},
            {"id": 12, "label": "暂停"},
            {"id": 13, "label": "导出日志"},
            {"id": 14, "label": "批量升级"},
            {"id": 15, "label": "主动验证"},
            {"id": 16, "label": "熔断配置"},
            {"id": 17, "label": "IDE 插件"},
            {"id": 18, "label": "CI/CD 集成"},
            {"id": 19, "label": "缺陷管理"},
            {"id": 20, "label": "消息通知"},
            {"id": 21, "label": "其他"},
            {"id": 22, "label": "新增策略"},
            {"id": 23, "label": "编辑策略"},
            {"id": 24, "label": "删除策略"},
            {"id": 25, "label": "修改状态"},
            {"id": 26, "label": "新增模版"},
            {"id": 27, "label": "编辑模版"},
            {"id": 28, "label": "删除模版"},
            {"id": 29, "label": "修改状态"},
            {"id": 30, "label": "添加规则类型"},
            {"id": 31, "label": "添加规则"},
            {"id": 32, "label": "删除规则"},
            {"id": 33, "label": "修改状态"},
            {"id": 34, "label": "全部启用"},
            {"id": 35, "label": "全部禁用"},
            {"id": 36, "label": "全部删除"},
            {"id": 37, "label": "新增规则"},
            {"id": 38, "label": "编辑规则"},
            {"id": 39, "label": "删除规则"},
            {"id": 40, "label": "修改状态"},
            {"id": 41, "label": "新增配置"},
            {"id": 42, "label": "编辑模版"},
            {"id": 57, "label": "删除模版"},
            {"id": 43, "label": "只读"},
            {"id": 44, "label": "修改"},
            {"id": 45, "label": "新增角色"},
            {"id": 46, "label": "删除角色"},
            {"id": 47, "label": "编辑角色"},
            {"id": 48, "label": "新增项目组"},
            {"id": 49, "label": "删除项目组"},
            {"id": 50, "label": "编辑项目组"},
            {"id": 51, "label": "查看详情"},
            {"id": 52, "label": "新增账号"},
            {"id": 53, "label": "删除账号"},
            {"id": 54, "label": "编辑账号"},
            {"id": 55, "label": "查看详情"},
            {"id": 56, "label": "消息通知"},
        ],
    }
    IastRoleV2.object.filter(name="管理员", is_admin=True).update(permission=new_admin_permission)
    IastRoleV2.object.filter(name="普通用户", is_admin=True).update(permission=new_user_permission)


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0035_alter_user_phone"),
    ]

    operations = [
        migrations.RunPython(update_admin_role),
    ]
