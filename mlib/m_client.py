# encoding: utf-8

import re
import time

import requests
import urllib3
from mlib.logger import myLog
from mlib.m_expection import ParamsError
from requests import Request, Response
from requests.exceptions import (InvalidSchema, InvalidURL, MissingSchema,
                                 RequestException)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

absolute_http_url_regexp = re.compile(r"^https?://", re.I)

logger = myLog.getLog()

class ApiResponse(Response):

    def raise_for_status(self):
        if hasattr(self, 'error') and self.error:
            raise self.error
        Response.raise_for_status(self)


class HttpSession(requests.Session):
    """
    Class for performing HTTP requests and holding (session-) cookies between requests (in order
    to be able to log in and out of websites). Each request is logged so that HttpRunner can
    display statistics.

    This is a slightly extended version of `python-request <http://python-requests.org>`_'s
    :py:class:`requests.Session` class and mostly this class works exactly the same. However
    the methods for making requests (get, post, delete, put, head, options, patch, request)
    can now take a *url* argument that's only the path part of the URL, in which case the host
    part of the URL will be prepended with the HttpSession.base_url which is normally inherited
    from a HttpRunner class' host property.
    """
    def __init__(self, base_url=None, *args, **kwargs):
        super(HttpSession, self).__init__(*args, **kwargs)
        self.base_url = base_url if base_url else ""
        self.init_meta_data()

    def _build_url(self, path):
        """ prepend url with hostname unless it's already an absolute URL """
        if absolute_http_url_regexp.match(path):
            return path
        elif self.base_url:
            return "{}/{}".format(self.base_url.rstrip("/"), path.lstrip("/"))
        else:
            raise ParamsError("base url missed!")

    def init_meta_data(self):
        """ initialize meta_data, it will store detail data of request and response
        """
        self.meta_data = {
            "url": "N/A",
            "method": "N/A",
            "request_time": "N/A",
            "request_headers": {},
            "request_body": "N/A",
            "status_code": "N/A",
            "response_headers": {},
            "response_body": "N/A",
            "content_size": "N/A",
            "response_time_ms": "N/A",
            "elapsed_ms": "N/A"
        }

    def request(self, method, url, name=None, **kwargs):
        """
        Constructs and sends a :py:class:`requests.Request`.
        Returns :py:class:`requests.Response` object.

        :param method:
            method for the new :class:`Request` object.
        :param url:
            URL for the new :class:`Request` object.
        :param name: (optional)
            Placeholder, make compatible with Locust's HttpSession
        :param params: (optional)
            Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional)
            Dictionary or bytes to send in the body of the :class:`Request`.
        :param headers: (optional)
            Dictionary of HTTP Headers to send with the :class:`Request`.
        :param cookies: (optional)
            Dict or CookieJar object to send with the :class:`Request`.
        :param files: (optional)
            Dictionary of ``'filename': file-like-objects`` for multipart encoding upload.
        :param auth: (optional)
            Auth tuple or callable to enable Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional)
            How long to wait for the server to send data before giving up, as a float, or \
            a (`connect timeout, read timeout <user/advanced.html#timeouts>`_) tuple.
            :type timeout: float or tuple
        :param allow_redirects: (optional)
            Set to True by default.
        :type allow_redirects: bool
        :param proxies: (optional)
            Dictionary mapping protocol to the URL of the proxy.
        :param stream: (optional)
            whether to immediately download the response content. Defaults to ``False``.
        :param verify: (optional)
            if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
        :param cert: (optional)
            if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.
        """
        # record original request info
        self.meta_data["method"] = method
        self.meta_data["url"] = url
        self.meta_data["request_time"] = time.time()

        # prepend url with hostname unless it's already an absolute URL
        url = self._build_url(url)
        print(url)
        kwargs.setdefault("timeout", 120)
        response = self._send_request_safe_mode(method, url, **kwargs)

        # record the consumed time
        self.meta_data["response_time_ms"] = round((time.time() - self.meta_data["request_time"]) * 1000, 2)
        self.meta_data["elapsed_ms"] = response.elapsed.microseconds / 1000.0

        # record actual request info
        self.meta_data["url"] = (response.history and response.history[0] or response).request.url
        self.meta_data["request_headers"] = response.request.headers
        self.meta_data["request_body"] = response.request.body

        # record response info
        self.meta_data["status_code"] = response.status_code
        self.meta_data["response_headers"] = response.headers
        try:
            self.meta_data["response_body"] = response.json()
        except ValueError:
            self.meta_data["response_body"] = response.content

        # log response details in debug mode
        msg = "response details:\n"
        msg += "> status_code: {}\n".format(self.meta_data["status_code"])
        msg += "> headers: {}\n".format(self.meta_data["response_headers"])
        msg += "> body: {}".format(self.meta_data["response_body"])
        logger.m_debug(msg)

        # get the length of the content, but if the argument stream is set to True, we take
        # the size from the content-length header, in order to not trigger fetching of the body
        if kwargs.get("stream", False):
            self.meta_data["content_size"] = int(self.meta_data["response_headers"].get("content-length") or 0)
        else:
            self.meta_data["content_size"] = len(response.content or "")

        try:
            response.raise_for_status()
        except RequestException as e:
            logger.m_error(u"{exception}".format(exception=str(e)))
        else:
            logger.m_info(
                """status_code: {}, response_time(ms): {} ms, response_length: {} bytes""".format(
                    self.meta_data["status_code"],
                    self.meta_data["response_time_ms"],
                    self.meta_data["content_size"]
                )
            )

        return response

    def _send_request_safe_mode(self, method, url, **kwargs):
        """
        Send a HTTP request, and catch any exception that might occur due to connection problems.
        Safe mode has been removed from requests 1.x.
        """
        try:
            msg = "processed request:\n"
            msg += "> {method} {url}\n".format(method=method, url=url)
            msg += "> kwargs: {kwargs}".format(kwargs=kwargs)
            logger.m_debug(msg)
            return requests.Session.request(self, method, url, **kwargs)
        except (MissingSchema, InvalidSchema, InvalidURL):
            raise
        except RequestException as ex:
            resp = ApiResponse()
            resp.error = ex
            resp.status_code = 0  # with this status_code, content returns None
            resp.request = Request(method, url).prepare()
            return resp
