# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpc.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\trpc.proto\x12\x11trabalho_sabatine\"9\n\x10SendDispoRequest\x12\x16\n\x0eid_dispositivo\x18\x01 \x01(\t\x12\r\n\x05marca\x18\x02 \x01(\t\"!\n\x0eSendDispoReply\x12\x0f\n\x07message\x18\x01 \x01(\t2\xc7\x01\n\nApiService\x12U\n\tSendDispo\x12#.trabalho_sabatine.SendDispoRequest\x1a!.trabalho_sabatine.SendDispoReply\"\x00\x12\x62\n\x14SendDispoStreamReply\x12#.trabalho_sabatine.SendDispoRequest\x1a!.trabalho_sabatine.SendDispoReply\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'rpc_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SENDDISPOREQUEST']._serialized_start=32
  _globals['_SENDDISPOREQUEST']._serialized_end=89
  _globals['_SENDDISPOREPLY']._serialized_start=91
  _globals['_SENDDISPOREPLY']._serialized_end=124
  _globals['_APISERVICE']._serialized_start=127
  _globals['_APISERVICE']._serialized_end=326
# @@protoc_insertion_point(module_scope)