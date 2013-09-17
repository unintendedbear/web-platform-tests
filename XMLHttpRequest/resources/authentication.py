def main(request, response):
    if "logout" in request.GET:
        return ((401, "Unauthorized"),
                [("WWW-Authenticate", 'Basic realm="test"')],
                "Logged out, hopefully")

    session_user = request.auth.username
    session_pass = request.auth.password
    expected_user_name = request.headers.get("X-User", None)
    expected_user_password = request.headers.get("X-Pass", None)

    token = expected_user_name
    if session_user is None and session_pass is None:
        if token is not None and request.server.stash.take(token) is not None:
            return 'FAIL (did not challenge)'
        else:
            if token is not None:
                request.server.stash.put(token, "1")
            status = (401, 'Unauthorized')
            headers = [('WWW-Authenticate', 'Basic realm="test"'),
                       ('XHR-USER', expected_user_name),
                       ('SES-USER', session_user)]
            return status, headers, 'FAIL (should be transparent)'
    else:
        headers = [('XHR-USER', expected_user_name),
                   ('SES-USER', session_user),
                   ("X-challenge", "DID" if token is not None and request.server.stash.take(token) is None
                    else "DID-NOT")]
        return headers, session_user + "\n" + session_pass;

