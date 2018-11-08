# Copyright 2014 OpenStack Foundation
# All Rights Reserved.
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

from octavia.common import constants
from octavia.common.jinja.haproxy import jinja_cfg
from octavia.tests.unit import base
from octavia.tests.unit.common.sample_configs import sample_configs


class TestHaproxyCfg(base.TestCase):
    def setUp(self):
        super(TestHaproxyCfg, self).setUp()
        self.jinja_cfg = jinja_cfg.JinjaTemplater(
            base_amp_path='/var/lib/octavia',
            base_crt_dir='/var/lib/octavia/certs')

    def test_get_template(self):
        template = self.jinja_cfg._get_template()
        self.assertEqual('haproxy.cfg.j2', template.name)

    def test_render_template_tls(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option httplog\n"
              "    maxconn {maxconn}\n"
              "    redirect scheme https if !{{ ssl_fc }}\n"
              "    bind 10.0.0.2:443 "
              "ssl crt /var/lib/octavia/certs/"
              "sample_listener_id_1/tls_container_id.pem "
              "crt /var/lib/octavia/certs/sample_listener_id_1\n"
              "    mode http\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 cookie "
              "sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        tls_tupe = sample_configs.sample_tls_container_tuple(
            id='tls_container_id',
            certificate='imaCert1', private_key='imaPrivateKey1',
            primary_cn='FakeCN')
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='TERMINATED_HTTPS',
                                                 tls=True, sni=True),
            tls_tupe)
        self.assertEqual(
            sample_configs.sample_base_expected_config(
                frontend=fe, backend=be),
            rendered_obj)

    def test_render_template_tls_no_sni(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option httplog\n"
              "    maxconn {maxconn}\n"
              "    redirect scheme https if !{{ ssl_fc }}\n"
              "    bind 10.0.0.2:443 "
              "ssl crt /var/lib/octavia/certs/"
              "sample_listener_id_1/tls_container_id.pem\n"
              "    mode http\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                proto='TERMINATED_HTTPS', tls=True),
            tls_cert=sample_configs.sample_tls_container_tuple(
                id='tls_container_id',
                certificate='ImAalsdkfjCert',
                private_key='ImAsdlfksdjPrivateKey',
                primary_cn="FakeCN"))
        self.assertEqual(
            sample_configs.sample_base_expected_config(
                frontend=fe, backend=be),
            rendered_obj)

    def test_render_template_http(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple())
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_member_backup(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "addr 192.168.1.1 port 9000 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "addr 192.168.1.1 port 9000 "
              "cookie sample_member_id_2 backup\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(monitor_ip_port=True,
                                                 backup_member=True))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_custom_timeouts(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option httplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:80\n"
              "    mode http\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 1\n"
              "    timeout server 3\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "check inter 30s fall 3 rise 2 cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "check inter 30s fall 3 rise 2 cookie "
              "sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(timeout_member_connect=1,
                                                 timeout_client_data=2,
                                                 timeout_member_data=3))
        self.assertEqual(
            sample_configs.sample_base_expected_config(frontend=fe,
                                                       backend=be),
            rendered_obj)

    def test_render_template_null_timeouts(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option httplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:80\n"
              "    mode http\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "check inter 30s fall 3 rise 2 cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "check inter 30s fall 3 rise 2 cookie "
              "sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(timeout_member_connect=None,
                                                 timeout_client_data=None,
                                                 timeout_member_data=None))
        self.assertEqual(
            sample_configs.sample_base_expected_config(frontend=fe,
                                                       backend=be),
            rendered_obj)

    def test_render_template_member_monitor_addr_port(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "addr 192.168.1.1 port 9000 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "addr 192.168.1.1 port 9000 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(monitor_ip_port=True))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_https_real_monitor(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option tcplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:443\n"
              "    mode tcp\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode tcp\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check check-ssl verify none inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check check-ssl verify none inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTPS'))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be), rendered_obj)

    def test_render_template_https_hello_monitor(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option tcplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:443\n"
              "    mode tcp\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode tcp\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option ssl-hello-chk\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                proto='HTTPS', monitor_proto='TLS-HELLO'))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be), rendered_obj)

    def test_render_template_no_monitor_http(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTP', monitor=False))
        self.assertEqual(sample_configs.sample_base_expected_config(
            backend=be), rendered_obj)

    def test_render_template_disabled_member(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "cookie sample_member_id_2 disabled\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTP', monitor=False,
                                                 disabled_member=True))
        self.assertEqual(sample_configs.sample_base_expected_config(
            backend=be), rendered_obj)

    def test_render_template_ping_monitor_http(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option external-check\n"
              "    external-check command /var/lib/octavia/ping-wrapper.sh\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        go = "    maxconn {maxconn}\n    external-check\n\n".format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTP',
                                                 monitor_proto='PING'))
        self.assertEqual(sample_configs.sample_base_expected_config(
            backend=be, global_opts=go), rendered_obj)

    def test_render_template_no_monitor_https(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option tcplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:443\n"
              "    mode tcp\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode tcp\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTPS', monitor=False))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be), rendered_obj)

    def test_render_template_no_persistence_https(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option tcplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:443\n"
              "    mode tcp\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode tcp\n"
              "    balance roundrobin\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13\n\n").format(maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTPS', monitor=False,
                                                 persistence=False))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be), rendered_obj)

    def test_render_template_no_persistence_http(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13\n\n").format(maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTP', monitor=False,
                                                 persistence=False))
        self.assertEqual(sample_configs.sample_base_expected_config(
            backend=be), rendered_obj)

    def test_render_template_sourceip_persistence(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    stick-table type ip size 10k\n"
              "    stick on src\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                persistence_type='SOURCE_IP'))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_appcookie_persistence(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    stick-table type string len 64 size 10k\n"
              "    stick store-response res.cook(JSESSIONID)\n"
              "    stick match req.cook(JSESSIONID)\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                persistence_type='APP_COOKIE',
                persistence_cookie='JSESSIONID'))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_unlimited_connections(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option tcplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:443\n"
              "    mode tcp\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode tcp\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTPS', monitor=False))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be), rendered_obj)

    def test_render_template_limited_connections(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option tcplog\n"
              "    maxconn 2014\n"
              "    bind 10.0.0.2:443\n"
              "    mode tcp\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n")
        be = ("backend sample_pool_id_1\n"
              "    mode tcp\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    fullconn 2014\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 "
              "cookie sample_member_id_2\n\n")
        g_opts = "    maxconn 2014\n\n"
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(proto='HTTPS', monitor=False,
                                                 connection_limit=2014))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be, global_opts=g_opts), rendered_obj)

    def test_render_template_l7policies(self):
        fe = ("frontend sample_listener_id_1\n"
              "    option httplog\n"
              "    maxconn {maxconn}\n"
              "    bind 10.0.0.2:80\n"
              "    mode http\n"
              "        acl sample_l7rule_id_1 path -m beg /api\n"
              "    use_backend sample_pool_id_2 if sample_l7rule_id_1\n"
              "        acl sample_l7rule_id_2 req.hdr(Some-header) -m sub "
              "This\\ string\\\\\\ with\\ stuff\n"
              "        acl sample_l7rule_id_3 req.cook(some-cookie) -m reg "
              "this.*|that\n"
              "    redirect location http://www.example.com if "
              "!sample_l7rule_id_2 sample_l7rule_id_3\n"
              "        acl sample_l7rule_id_4 path_end -m str jpg\n"
              "        acl sample_l7rule_id_5 req.hdr(host) -i -m end "
              ".example.com\n"
              "    http-request deny if sample_l7rule_id_4 "
              "sample_l7rule_id_5\n"
              "        acl sample_l7rule_id_2 req.hdr(Some-header) -m sub "
              "This\\ string\\\\\\ with\\ stuff\n"
              "        acl sample_l7rule_id_3 req.cook(some-cookie) -m reg "
              "this.*|that\n"
              "    redirect prefix https://example.com if "
              "!sample_l7rule_id_2 sample_l7rule_id_3\n"
              "    default_backend sample_pool_id_1\n"
              "    timeout client 50000\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 weight 13 check "
              "inter 30s fall 3 rise 2 cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 weight 13 check "
              "inter 30s fall 3 rise 2 cookie sample_member_id_2\n"
              "\n"
              "backend sample_pool_id_2\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /healthmon.html\n"
              "    http-check expect rstatus 418\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_3 10.0.0.97:82 weight 13 check "
              "inter 30s fall 3 rise 2 cookie sample_member_id_3\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(l7=True))
        self.assertEqual(sample_configs.sample_base_expected_config(
            frontend=fe, backend=be), rendered_obj)

    def test_render_template_http_xff(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    option forwardfor\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                insert_headers={'X-Forwarded-For': 'true'}))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_http_xff_xfport(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    option httpchk GET /index.html\n"
              "    http-check expect rstatus 418\n"
              "    option forwardfor\n"
              "    http-request set-header X-Forwarded-Port %[dst_port]\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                insert_headers={'X-Forwarded-For': 'true',
                                'X-Forwarded-Port': 'true'}))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_render_template_pool_proxy_protocol(self):
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1 send-proxy\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2 send-proxy\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = self.jinja_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(
                be_proto='PROXY'))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

    def test_transform_session_persistence(self):
        in_persistence = sample_configs.sample_session_persistence_tuple()
        ret = self.jinja_cfg._transform_session_persistence(in_persistence, {})
        self.assertEqual(sample_configs.RET_PERSISTENCE, ret)

    def test_transform_health_monitor(self):
        in_persistence = sample_configs.sample_health_monitor_tuple()
        ret = self.jinja_cfg._transform_health_monitor(in_persistence, {})
        self.assertEqual(sample_configs.RET_MONITOR_1, ret)

    def test_transform_member(self):
        in_member = sample_configs.sample_member_tuple('sample_member_id_1',
                                                       '10.0.0.99')
        ret = self.jinja_cfg._transform_member(in_member, {})
        self.assertEqual(sample_configs.RET_MEMBER_1, ret)

    def test_transform_pool(self):
        in_pool = sample_configs.sample_pool_tuple()
        ret = self.jinja_cfg._transform_pool(in_pool, {})
        self.assertEqual(sample_configs.RET_POOL_1, ret)

    def test_transform_pool_2(self):
        in_pool = sample_configs.sample_pool_tuple(sample_pool=2)
        ret = self.jinja_cfg._transform_pool(in_pool, {})
        self.assertEqual(sample_configs.RET_POOL_2, ret)

    def test_transform_pool_http_reuse(self):
        in_pool = sample_configs.sample_pool_tuple(sample_pool=2)
        ret = self.jinja_cfg._transform_pool(
            in_pool, {constants.HTTP_REUSE: True})
        import copy
        expected_config = copy.copy(sample_configs.RET_POOL_2)
        expected_config[constants.HTTP_REUSE] = True
        self.assertEqual(expected_config, ret)

    def test_transform_listener(self):
        in_listener = sample_configs.sample_listener_tuple()
        ret = self.jinja_cfg._transform_listener(in_listener, None, {})
        self.assertEqual(sample_configs.RET_LISTENER, ret)

    def test_transform_listener_with_l7(self):
        in_listener = sample_configs.sample_listener_tuple(l7=True)
        ret = self.jinja_cfg._transform_listener(in_listener, None, {})
        self.assertEqual(sample_configs.RET_LISTENER_L7, ret)

    def test_transform_loadbalancer(self):
        in_amphora = sample_configs.sample_amphora_tuple()
        in_listener = sample_configs.sample_listener_tuple()
        ret = self.jinja_cfg._transform_loadbalancer(
            in_amphora, in_listener.load_balancer, in_listener, None, {})
        self.assertEqual(sample_configs.RET_LB, ret)

    def test_transform_amphora(self):
        in_amphora = sample_configs.sample_amphora_tuple()
        ret = self.jinja_cfg._transform_amphora(in_amphora, {})
        self.assertEqual(sample_configs.RET_AMPHORA, ret)

    def test_transform_loadbalancer_with_l7(self):
        in_amphora = sample_configs.sample_amphora_tuple()
        in_listener = sample_configs.sample_listener_tuple(l7=True)
        ret = self.jinja_cfg._transform_loadbalancer(
            in_amphora, in_listener.load_balancer, in_listener, None, {})
        self.assertEqual(sample_configs.RET_LB_L7, ret)

    def test_transform_l7policy(self):
        in_l7policy = sample_configs.sample_l7policy_tuple(
            'sample_l7policy_id_1')
        ret = self.jinja_cfg._transform_l7policy(in_l7policy, {})
        self.assertEqual(sample_configs.RET_L7POLICY_1, ret)

    def test_transform_l7policy_2(self):
        in_l7policy = sample_configs.sample_l7policy_tuple(
            'sample_l7policy_id_2', sample_policy=2)
        ret = self.jinja_cfg._transform_l7policy(in_l7policy, {})
        self.assertEqual(sample_configs.RET_L7POLICY_2, ret)

    def test_transform_l7policy_disabled_rule(self):
        in_l7policy = sample_configs.sample_l7policy_tuple(
            'sample_l7policy_id_6', sample_policy=6)
        ret = self.jinja_cfg._transform_l7policy(in_l7policy, {})
        self.assertEqual(sample_configs.RET_L7POLICY_6, ret)

    def test_escape_haproxy_config_string(self):
        self.assertEqual(self.jinja_cfg._escape_haproxy_config_string(
            'string_with_none'), 'string_with_none')
        self.assertEqual(self.jinja_cfg._escape_haproxy_config_string(
            'string with spaces'), 'string\\ with\\ spaces')
        self.assertEqual(self.jinja_cfg._escape_haproxy_config_string(
            'string\\with\\backslashes'), 'string\\\\with\\\\backslashes')
        self.assertEqual(self.jinja_cfg._escape_haproxy_config_string(
            'string\\ with\\ all'), 'string\\\\\\ with\\\\\\ all')

    def test_expand_expected_codes(self):
        exp_codes = ''
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set([]))
        exp_codes = '200'
        self.assertEqual(
            self.jinja_cfg._expand_expected_codes(exp_codes), set(['200']))
        exp_codes = '200, 201'
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set(['200', '201']))
        exp_codes = '200, 201,202'
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set(['200', '201', '202']))
        exp_codes = '200-202'
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set(['200', '201', '202']))
        exp_codes = '200-202, 205'
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set(['200', '201', '202', '205']))
        exp_codes = '200, 201-203'
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set(['200', '201', '202', '203']))
        exp_codes = '200, 201-203, 205'
        self.assertEqual(self.jinja_cfg._expand_expected_codes(exp_codes),
                         set(['200', '201', '202', '203', '205']))
        exp_codes = '201-200, 205'
        self.assertEqual(
            self.jinja_cfg._expand_expected_codes(exp_codes), set(['205']))

    def test_render_template_no_log(self):
        j_cfg = jinja_cfg.JinjaTemplater(
            base_amp_path='/var/lib/octavia',
            base_crt_dir='/var/lib/octavia/certs',
            connection_logging=False)
        defaults = ("defaults\n"
                    "    no log\n"
                    "    retries 3\n"
                    "    option redispatch\n"
                    "    option splice-request\n"
                    "    option splice-response\n"
                    "    option http-keep-alive\n\n")
        rendered_obj = j_cfg.render_loadbalancer_obj(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple()
        )
        self.assertEqual(
            sample_configs.sample_base_expected_config(defaults=defaults),
            rendered_obj)

    def test_http_reuse(self):
        j_cfg = jinja_cfg.JinjaTemplater(
            base_amp_path='/var/lib/octavia',
            base_crt_dir='/var/lib/octavia/certs')

        # With http-reuse
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    http-reuse safe\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1 send-proxy\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2 send-proxy\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = j_cfg.build_config(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(be_proto='PROXY'),
            tls_cert=None,
            haproxy_versions=("1", "8", "1"))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)

        # Without http-reuse
        be = ("backend sample_pool_id_1\n"
              "    mode http\n"
              "    balance roundrobin\n"
              "    cookie SRV insert indirect nocache\n"
              "    timeout check 31s\n"
              "    fullconn {maxconn}\n"
              "    option allbackups\n"
              "    timeout connect 5000\n"
              "    timeout server 50000\n"
              "    server sample_member_id_1 10.0.0.99:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_1 send-proxy\n"
              "    server sample_member_id_2 10.0.0.98:82 "
              "weight 13 check inter 30s fall 3 rise 2 "
              "cookie sample_member_id_2 send-proxy\n\n").format(
            maxconn=constants.HAPROXY_MAX_MAXCONN)
        rendered_obj = j_cfg.build_config(
            sample_configs.sample_amphora_tuple(),
            sample_configs.sample_listener_tuple(be_proto='PROXY'),
            tls_cert=None,
            haproxy_versions=("1", "5", "18"))
        self.assertEqual(
            sample_configs.sample_base_expected_config(backend=be),
            rendered_obj)
