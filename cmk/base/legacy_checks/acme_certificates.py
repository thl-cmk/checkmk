#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


import time

from cmk.base.check_api import get_age_human_readable, LegacyCheckDefinition
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.agent_based_api.v1 import SNMPTree
from cmk.base.plugins.agent_based.utils.acme import DETECT_ACME

# .1.3.6.1.4.1.9148.3.9.1.10.1.3.65.1 rootca
# .1.3.6.1.4.1.9148.3.9.1.10.1.5.65.1 Jul 25 00:33:17 2003 GMT
# .1.3.6.1.4.1.9148.3.9.1.10.1.6.65.1 Aug 17 05:19:39 2027 GMT
# .1.3.6.1.4.1.9148.3.9.1.10.1.7.65.1 /C=US/O=Avaya Inc./OU=SIP Product Certificate Authority/CN=SIP Product Certificate Authority


def inventory_acme_certificates(info):
    return [(name, {}) for name, _start, _expire, _issuer in info]


def check_acme_certificates(item, params, info):
    for name, start, expire, issuer in info:
        if item == name:
            expire_date, _expire_tz = expire.rsplit(" ", 1)
            expire_time = time.mktime(time.strptime(expire_date, "%b %d %H:%M:%S %Y"))

            now = time.time()
            warn, crit = params["expire_lower"]
            state = 0

            time_diff = expire_time - now
            if expire_time <= now:
                age_info = "%s ago" % get_age_human_readable(abs(time_diff))
            else:
                age_info = "%s to go" % get_age_human_readable(time_diff)

            infotext = "Expire: %s (%s)" % (expire, age_info)

            if time_diff >= 0:
                if time_diff < crit:
                    state = 2
                elif time_diff < warn:
                    state = 1
                if state:
                    infotext += " (warn/crit below %s/%s)" % (
                        get_age_human_readable(warn),
                        get_age_human_readable(crit),
                    )
            else:
                state = 2
                infotext += " (expire date in the past)"

            yield state, infotext
            yield 0, "Start: %s, Issuer: %s" % (start, issuer)


check_info["acme_certificates"] = LegacyCheckDefinition(
    detect=DETECT_ACME,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.9148.3.9.1.10.1",
        oids=["3", "5", "6", "7"],
    ),
    service_name="Certificate %s",
    discovery_function=inventory_acme_certificates,
    check_function=check_acme_certificates,
    check_ruleset_name="acme_certificates",
    check_default_parameters={
        "expire_lower": (604800, 2592000),  # 1 week, 30 days, suggested by customer
    },
)
