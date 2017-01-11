#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib,time,json,requests

app_key = '1234568'
app_secret = '0123456789abcdef0123456789abcdef'
user_id = 291234568


if type('') is not type(b''):
    bytes_type = bytes
    unicode_type = str
    basestring_type = str
else:
    bytes_type = str
    unicode_type = unicode
    basestring_type = basestring

_UTF8_TYPES = (bytes_type, type(None))


def utf8(text):
    """
        Converts a string argument to a byte string.

        If the argument is already a byte string or None, it is returned unchanged.
        Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(text, _UTF8_TYPES):
        return text
    assert isinstance(text, unicode_type), \
        "Expected bytes, unicode, or None; got %r" % type(text)
    return text.encode("utf-8")


def sign(secret, parameters):
    if hasattr(parameters, "items"):
        keys = parameters.keys()
        keys = sorted(keys, key=lambda x: x)

        body = str().join('%s%s' % (key, parameters[key]) for key in keys)
        parameters = "%s%s%s" % (secret, body, secret)
    else:
        print(" it's not a dictionary.")
    parameters = utf8(parameters)
    sign = hashlib.md5(parameters).hexdigest().upper()
    return sign

def api(tokendata):
    # 生成当前时间
    secret_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    tpwd_param = tokendata

    data = {
        'app_key': app_key,
        'format': 'json',
        'method': 'taobao.wireless.share.tpwd.create',
        'partner_id': 'top-apitools',
        'sign_method': 'md5',
        'timestamp': secret_time,
        'v': '2.0',
        'tpwd_param': json.dumps(tpwd_param),
    }

    data['sign'] = sign(app_secret, data)
    api_base = 'http://gw.api.taobao.com/router/rest'
    print(requests.post(api_base, headers=headers, data=data).json())


tokendata = {
    'text': '[优惠券内部专享]——汽车香水挂件车载精油挂饰品',
    'url': 'https://uland.taobao.com/coupon/edetail?activityId=0a537cb5a98a45c0bb5245825860659f&itemId=539341555442&pid=mm_118081706_19234461_67024748&scenes=3&channel=tk_qqhd',
    # 'ext': '{\"xx\":\"xx\"}',
    'logo': "http://img.alicdn.com/imgextra/i1/2351480332/TB2ZBD3b8PzQeBjSZFhXXbRpFXa_!!2351480332.jpg_400x400q70.jpg",
    'user_id': user_id
}
api(tokendata)
