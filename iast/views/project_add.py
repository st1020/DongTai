#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging
import time

from django.db.models import Q

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.project import (IastProject, VulValidation)
from dongtai.models.strategy_user import IastStrategyUser
from iast.base.project_version import version_modify, ProjectsVersionDataSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from django.db import transaction

logger = logging.getLogger("django")


class _ProjectsAddBodyArgsSerializer(serializers.Serializer):
    name = serializers.CharField(help_text=_('The name of project'))
    agent_ids = serializers.CharField(help_text=_(
        'The id corresponding to the agent, use, for segmentation.'))
    scan_id = serializers.IntegerField(
        help_text=_("The id corresponding to the scanning strategy."))
    version_name = serializers.CharField(
        help_text=_("The version name of the project"))
    pid = serializers.IntegerField(help_text=_("The id of the project"))
    description = serializers.CharField(
        help_text=_("Description of the project"))
    vul_validation = serializers.IntegerField(
        help_text="vul validation switch")
    base_url = serializers.CharField()
    test_req_header_key = serializers.CharField()
    test_req_header_value = serializers.CharField()



_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((202, _('Parameter error')), ''),
    ((201, _('Created success')), ''),
    ((202, _('Agent has been bound by other application')), ''),
    ((203, _('Failed to create, the application name already exists')), ''),
))


class ProjectAdd(UserEndPoint):
    name = "api-v1-project-add"
    description = _("New application")

    @extend_schema_with_envcheck(
        request=_ProjectsAddBodyArgsSerializer,
        tags=[_('Project')],
        summary=_('Projects Add'),
        description=_(
            """Create a new project according to the given conditions;
            when specifying the project id, update the item corresponding to the id according to the given condition."""
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        with transaction.atomic():
            try:
                name = request.data.get("name")
                mode = "插桩模式"
                scan_id = request.data.get("scan_id")

                auth_users = self.get_auth_users(request.user)
                scan = IastStrategyUser.objects.filter(id=scan_id, user=request.user).first()
                agent_ids = request.data.get("agent_ids", None)
                base_url = request.data.get('base_url', None)
                test_req_header_key = request.data.get('test_req_header_key',
                                                       None)
                test_req_header_value = request.data.get(
                    'test_req_header_value', None)
                if agent_ids:
                    try:
                        agents = [int(i) for i in agent_ids.split(',')]
                    except Exception as e:
                        print(e)
                        return R.failure(status=202, msg=_('Parameter error'))
                else:
                    agents = []
                if not scan_id or not name or not mode:
                    return R.failure(status=202, msg=_('Parameter error'))

                version_name = request.data.get("version_name", "")
                if not version_name:
                    version_name = "V1.0"
                pid = request.data.get("pid", 0)
                vul_validation = request.data.get("vul_validation", None)
                #vul_validation = vul_validation if vul_validation is None else (
                #    VulValidation.ENABLE
                #    if vul_validation == True else VulValidation.DISABLE)
                if pid:
                    project = IastProject.objects.filter(id=pid, user=request.user).first()
                    project.name = name
                else:

                    project = IastProject.objects.filter(name=name, user=request.user).first()
                    if not project:
                        project = IastProject.objects.create(name=name, user=request.user)
                    else:
                        return R.failure(status=203, msg=_('Failed to create, the application name already exists'))
                versionInfo = IastProjectVersion.objects.filter(project_id=project.id, user=request.user, current_version=1, status=1).first()
                if versionInfo:
                    project_version_id = versionInfo.id
                else:
                    project_version_id = 0
                current_project_version = {
                    "project_id": project.id,
                    "version_id": project_version_id,
                    "version_name": version_name,
                    "description": request.data.get("description", ""),
                    "current_version": 1
                }
                result = version_modify(request.user, current_project_version)
                if result.get("status", "202") == "202":
                    return R.failure(status=202, msg=_("Parameter error"))
                else:
                    project_version_id = result.get("data", {}).get("version_id", 0)

                if agent_ids:
                    haveBind = IastAgent.objects.filter(
                        ~Q(bind_project_id=project.id),
                        id__in=agents,
                        bind_project_id__gt=0,
                        user__in=auth_users).exists()
                    if haveBind:
                        return R.failure(status=202, msg=_('Agent has been bound by other application'))

                project.scan = scan
                project.mode = mode
                project.agent_count = len(agents)
                project.user = request.user
                project.latest_time = int(time.time())
                if vul_validation is not None:
                    project.vul_validation = vul_validation
                if agents:
                    project.agent_count = IastAgent.objects.filter(
                        Q(id__in=agents) | Q(project_name=name),
                        user__in=auth_users,
                        bind_project_id=0,
                        project_version_id=0
                    ).update(bind_project_id=project.id, project_version_id=project_version_id, online=1)
                else:
                    project.agent_count = IastAgent.objects.filter(
                        project_name=name, user__in=auth_users).update(
                            bind_project_id=project.id,
                            project_version_id=project_version_id)
                if base_url:
                    project.base_url = base_url
                if test_req_header_key:
                    project.test_req_header_key = test_req_header_key
                if test_req_header_value:
                    project.test_req_header_value = test_req_header_value
                project.save(update_fields=[
                    'name', 'scan_id', 'mode', 'agent_count', 'user_id',
                    'latest_time', 'vul_validation', 'base_url',
                    'test_req_header_key', 'test_req_header_value'
                ])

                return R.success(
                    msg=_('Updated success')) if pid else R.success(
                        msg=_('Created success'))
            except Exception as e:
                logger.error(e)
                return R.failure(status=202, msg=_("Parameter error"))
