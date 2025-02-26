from typing import Any, Callable

import grpc


class StaticTokenValidationInterceptor(grpc.ServerInterceptor):
    HEADER_KEY = "authorization"

    def __init__(self, token: str) -> None:
        def abort(ignored_request: Any, context: grpc.ServicerContext) -> None:
            context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")

        self._abortion = grpc.unary_unary_rpc_method_handler(abort)
        self.token = token

    def intercept_service(
        self, continuation: Callable, handler_call_details: grpc.HandlerCallDetails
    ) -> grpc.RpcMethodHandler:
        for header, value in handler_call_details.invocation_metadata:  # type: ignore [reportAttributeAccessIssue]]
            if header == self.HEADER_KEY:
                token = value.decode("utf-8") if isinstance(value, bytes) else value
                if token.startswith("Bearer "):
                    token = token[7:]

                if self.token == token:
                    return continuation(handler_call_details)

        return self._abortion
