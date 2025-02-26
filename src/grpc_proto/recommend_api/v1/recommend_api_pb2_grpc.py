# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from recommend_api.v1 import recommend_api_pb2 as recommend__api_dot_v1_dot_recommend__api__pb2


class RecommenderServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Recommend = channel.unary_unary(
                '/recommend_api.v1.RecommenderService/Recommend',
                request_serializer=recommend__api_dot_v1_dot_recommend__api__pb2.RecommendRequest.SerializeToString,
                response_deserializer=recommend__api_dot_v1_dot_recommend__api__pb2.RecommendResponse.FromString,
                _registered_method=True)


class RecommenderServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Recommend(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RecommenderServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Recommend': grpc.unary_unary_rpc_method_handler(
                    servicer.Recommend,
                    request_deserializer=recommend__api_dot_v1_dot_recommend__api__pb2.RecommendRequest.FromString,
                    response_serializer=recommend__api_dot_v1_dot_recommend__api__pb2.RecommendResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'recommend_api.v1.RecommenderService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('recommend_api.v1.RecommenderService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RecommenderService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Recommend(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/recommend_api.v1.RecommenderService/Recommend',
            recommend__api_dot_v1_dot_recommend__api__pb2.RecommendRequest.SerializeToString,
            recommend__api_dot_v1_dot_recommend__api__pb2.RecommendResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
