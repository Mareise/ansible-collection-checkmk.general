#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Copyright: (c) 2023, Marcel Arentz <gdspd_you@open-one.de>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Ensure compatibility to Python2
from __future__ import absolute_import, division, print_function

__metaclass__ = type


def result_as_dict(result):
    return {
        "changed": result.changed,
        "failed": result.failed,
        "msg": result.msg,
    }


GENERIC_HTTP_CODES = {
    204: (True, False, "Successfully executed"),
    400: (False, True, "Bad request: Parameter or validation failure"),
    403: (False, True, "Forbidden: Configuration via Setup is disabled"),
    404: (False, True, "Not found"),
    406: (False, True, "Required headers are not satisfied"),
    412: (False, True, "If-Match does not match ETag"),
    415: (False, True, "Wrong content-type in header"),
    428: (False, True, "If-Match header is missing"),
}

def construct_error_message_for_failed_fetch_call(info, error_origin):
    if  error_origin:
        error_template = "Error calling API. Origin: {%s}." % error_origin
    else:
        error_template = "Error calling API."
    
    status_code = info.get("status")
    if status_code:
        error_template += " HTTP code: %d." % status_code

    body = info.get("body")
    msg = info.get("msg")

    error_details = "Body: %s." % body if body else ("Msg: %s." % msg if msg else "N/A")

    error_message = error_template + " Details: {%s}." % error_details
    return error_message