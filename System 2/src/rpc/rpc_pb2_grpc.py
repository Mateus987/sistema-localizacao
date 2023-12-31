# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import src.rpc.rpc_pb2 as rpc__pb2


class ApiServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendDispo = channel.unary_unary(
                '/trabalho_sabatine.ApiService/SendDispo',
                request_serializer=rpc__pb2.SendDispoRequest.SerializeToString,
                response_deserializer=rpc__pb2.SendDispoReply.FromString,
                )
        self.SendDispoStreamReply = channel.unary_stream(
                '/trabalho_sabatine.ApiService/SendDispoStreamReply',
                request_serializer=rpc__pb2.SendDispoRequest.SerializeToString,
                response_deserializer=rpc__pb2.SendDispoReply.FromString,
                )


class ApiServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SendDispo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendDispoStreamReply(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ApiServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendDispo': grpc.unary_unary_rpc_method_handler(
                    servicer.SendDispo,
                    request_deserializer=rpc__pb2.SendDispoRequest.FromString,
                    response_serializer=rpc__pb2.SendDispoReply.SerializeToString,
            ),
            'SendDispoStreamReply': grpc.unary_stream_rpc_method_handler(
                    servicer.SendDispoStreamReply,
                    request_deserializer=rpc__pb2.SendDispoRequest.FromString,
                    response_serializer=rpc__pb2.SendDispoReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'trabalho_sabatine.ApiService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ApiService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SendDispo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/trabalho_sabatine.ApiService/SendDispo',
            rpc__pb2.SendDispoRequest.SerializeToString,
            rpc__pb2.SendDispoReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendDispoStreamReply(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/trabalho_sabatine.ApiService/SendDispoStreamReply',
            rpc__pb2.SendDispoRequest.SerializeToString,
            rpc__pb2.SendDispoReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
