# Copyright 2018 GoDaddy
# Copyright (c) 2015 Rackspace
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from octavia.controller.healthmanager.health_drivers import update_base
from octavia.tests.unit import base


class TestHealthUpdateBase(base.TestCase):

    def setUp(self):
        super(TestHealthUpdateBase, self).setUp()
        self.logger = update_base.HealthUpdateBase()

    def test_update_health(self):
        self.assertRaises(NotImplementedError,
                          self.logger.update_health, {'id': 1}, '192.0.2.1')


class TestStatsUpdateBase(base.TestCase):
    def setUp(self):
        super(TestStatsUpdateBase, self).setUp()
        self.logger = update_base.StatsUpdateBase()

    def test_update_stats(self):
        self.assertRaises(NotImplementedError,
                          self.logger.update_stats, {'id': 1}, '192.0.2.1')
