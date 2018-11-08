#    Copyright 2014 Rackspace
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from wsme import types as wtypes

from octavia.api.common import types
from octavia.common import constants


class BaseHealthMonitorType(types.BaseType):
    _type_to_model_map = {'admin_state_up': 'enabled',
                          'max_retries': 'rise_threshold',
                          'max_retries_down': 'fall_threshold'}
    _child_map = {}


class HealthMonitorResponse(BaseHealthMonitorType):
    """Defines which attributes are to be shown on any response."""
    id = wtypes.wsattr(wtypes.UuidType())
    name = wtypes.wsattr(wtypes.StringType())
    type = wtypes.wsattr(wtypes.text)
    delay = wtypes.wsattr(wtypes.IntegerType())
    timeout = wtypes.wsattr(wtypes.IntegerType())
    max_retries = wtypes.wsattr(wtypes.IntegerType())
    max_retries_down = wtypes.wsattr(wtypes.IntegerType())
    http_method = wtypes.wsattr(wtypes.text)
    url_path = wtypes.wsattr(wtypes.text)
    expected_codes = wtypes.wsattr(wtypes.text)
    admin_state_up = wtypes.wsattr(bool)
    project_id = wtypes.wsattr(wtypes.StringType())
    pools = wtypes.wsattr([types.IdOnlyType])
    provisioning_status = wtypes.wsattr(wtypes.StringType())
    operating_status = wtypes.wsattr(wtypes.StringType())
    created_at = wtypes.wsattr(wtypes.datetime.datetime)
    updated_at = wtypes.wsattr(wtypes.datetime.datetime)

    @classmethod
    def from_data_model(cls, data_model, children=False):
        healthmonitor = super(HealthMonitorResponse, cls).from_data_model(
            data_model, children=children)

        if cls._full_response():
            del healthmonitor.pools
        else:
            healthmonitor.pools = [
                types.IdOnlyType.from_data_model(data_model.pool)]
        return healthmonitor


class HealthMonitorFullResponse(HealthMonitorResponse):
    @classmethod
    def _full_response(cls):
        return True


class HealthMonitorRootResponse(types.BaseType):
    healthmonitor = wtypes.wsattr(HealthMonitorResponse)


class HealthMonitorsRootResponse(types.BaseType):
    healthmonitors = wtypes.wsattr([HealthMonitorResponse])
    healthmonitors_links = wtypes.wsattr([types.PageType])


class HealthMonitorPOST(BaseHealthMonitorType):
    """Defines mandatory and optional attributes of a POST request."""
    name = wtypes.wsattr(wtypes.StringType(max_length=255))
    type = wtypes.wsattr(
        wtypes.Enum(str, *constants.SUPPORTED_HEALTH_MONITOR_TYPES),
        mandatory=True)
    delay = wtypes.wsattr(wtypes.IntegerType(minimum=0), mandatory=True)
    timeout = wtypes.wsattr(wtypes.IntegerType(minimum=0), mandatory=True)
    max_retries_down = wtypes.wsattr(
        wtypes.IntegerType(minimum=constants.MIN_HM_RETRIES,
                           maximum=constants.MAX_HM_RETRIES), default=3)
    max_retries = wtypes.wsattr(
        wtypes.IntegerType(minimum=constants.MIN_HM_RETRIES,
                           maximum=constants.MAX_HM_RETRIES),
        mandatory=True)
    http_method = wtypes.wsattr(
        wtypes.Enum(str, *constants.SUPPORTED_HEALTH_MONITOR_HTTP_METHODS))
    url_path = wtypes.wsattr(
        types.URLPathType())
    expected_codes = wtypes.wsattr(
        wtypes.StringType(pattern=r'^(\d{3}(\s*,\s*\d{3})*)$|^(\d{3}-\d{3})$'))
    admin_state_up = wtypes.wsattr(bool, default=True)
    # TODO(johnsom) Remove after deprecation (R series)
    project_id = wtypes.wsattr(wtypes.StringType(max_length=36))
    pool_id = wtypes.wsattr(wtypes.UuidType(), mandatory=True)


class HealthMonitorRootPOST(types.BaseType):
    healthmonitor = wtypes.wsattr(HealthMonitorPOST)


class HealthMonitorPUT(BaseHealthMonitorType):
    """Defines attributes that are acceptable of a PUT request."""
    name = wtypes.wsattr(wtypes.StringType(max_length=255))
    delay = wtypes.wsattr(wtypes.IntegerType(minimum=0))
    timeout = wtypes.wsattr(wtypes.IntegerType(minimum=0))
    max_retries_down = wtypes.wsattr(
        wtypes.IntegerType(minimum=constants.MIN_HM_RETRIES,
                           maximum=constants.MAX_HM_RETRIES))
    max_retries = wtypes.wsattr(
        wtypes.IntegerType(minimum=constants.MIN_HM_RETRIES,
                           maximum=constants.MAX_HM_RETRIES))
    http_method = wtypes.wsattr(
        wtypes.Enum(str, *constants.SUPPORTED_HEALTH_MONITOR_HTTP_METHODS))
    url_path = wtypes.wsattr(types.URLPathType())
    expected_codes = wtypes.wsattr(
        wtypes.StringType(pattern=r'^(\d{3}(\s*,\s*\d{3})*)$|^(\d{3}-\d{3})$'))
    admin_state_up = wtypes.wsattr(bool)


class HealthMonitorRootPUT(types.BaseType):
    healthmonitor = wtypes.wsattr(HealthMonitorPUT)


class HealthMonitorSingleCreate(BaseHealthMonitorType):
    """Defines mandatory and optional attributes of a POST request."""
    name = wtypes.wsattr(wtypes.StringType(max_length=255))
    type = wtypes.wsattr(
        wtypes.Enum(str, *constants.SUPPORTED_HEALTH_MONITOR_TYPES),
        mandatory=True)
    delay = wtypes.wsattr(wtypes.IntegerType(minimum=0), mandatory=True)
    timeout = wtypes.wsattr(wtypes.IntegerType(minimum=0), mandatory=True)
    max_retries_down = wtypes.wsattr(
        wtypes.IntegerType(minimum=constants.MIN_HM_RETRIES,
                           maximum=constants.MAX_HM_RETRIES), default=3)
    max_retries = wtypes.wsattr(
        wtypes.IntegerType(minimum=constants.MIN_HM_RETRIES,
                           maximum=constants.MAX_HM_RETRIES),
        mandatory=True)
    http_method = wtypes.wsattr(
        wtypes.Enum(str, *constants.SUPPORTED_HEALTH_MONITOR_HTTP_METHODS))
    url_path = wtypes.wsattr(types.URLPathType())
    expected_codes = wtypes.wsattr(
        wtypes.StringType(pattern=r'^(\d{3}(\s*,\s*\d{3})*)$|^(\d{3}-\d{3})$'))
    admin_state_up = wtypes.wsattr(bool, default=True)


class HealthMonitorStatusResponse(BaseHealthMonitorType):
    """Defines which attributes are to be shown on status response."""
    id = wtypes.wsattr(wtypes.UuidType())
    name = wtypes.wsattr(wtypes.StringType())
    type = wtypes.wsattr(wtypes.text)
    provisioning_status = wtypes.wsattr(wtypes.StringType())
    operating_status = wtypes.wsattr(wtypes.StringType())
