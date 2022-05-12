# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/internal/more_extensions.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.google/protobuf/internal/more_extensions.proto\x12\x18google.protobuf.internal\"\x99\x01\n\x0fTopLevelMessage\x12\x41\n\nsubmessage\x18\x01 \x01(\x0b\x32).google.protobuf.internal.ExtendedMessageB\x02(\x01\x12\x43\n\x0enested_message\x18\x02 \x01(\x0b\x32\'.google.protobuf.internal.NestedMessageB\x02(\x01\"R\n\rNestedMessage\x12\x41\n\nsubmessage\x18\x01 \x01(\x0b\x32).google.protobuf.internal.ExtendedMessageB\x02(\x01\"K\n\x0f\x45xtendedMessage\x12\x17\n\x0eoptional_int32\x18\xe9\x07 \x01(\x05\x12\x18\n\x0frepeated_string\x18\xea\x07 \x03(\t*\x05\x08\x01\x10\xe8\x07\"-\n\x0e\x46oreignMessage\x12\x1b\n\x13\x66oreign_message_int\x18\x01 \x01(\x05:I\n\x16optional_int_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x01 \x01(\x05:w\n\x1aoptional_message_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x02 \x01(\x0b\x32(.google.protobuf.internal.ForeignMessage:I\n\x16repeated_int_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x03 \x03(\x05:w\n\x1arepeated_message_extension\x12).google.protobuf.internal.ExtendedMessage\x18\x04 \x03(\x0b\x32(.google.protobuf.internal.ForeignMessage')


OPTIONAL_INT_EXTENSION_FIELD_NUMBER = 1
optional_int_extension = DESCRIPTOR.extensions_by_name['optional_int_extension']
OPTIONAL_MESSAGE_EXTENSION_FIELD_NUMBER = 2
optional_message_extension = DESCRIPTOR.extensions_by_name['optional_message_extension']
REPEATED_INT_EXTENSION_FIELD_NUMBER = 3
repeated_int_extension = DESCRIPTOR.extensions_by_name['repeated_int_extension']
REPEATED_MESSAGE_EXTENSION_FIELD_NUMBER = 4
repeated_message_extension = DESCRIPTOR.extensions_by_name['repeated_message_extension']

_TOPLEVELMESSAGE = DESCRIPTOR.message_types_by_name['TopLevelMessage']
_NESTEDMESSAGE = DESCRIPTOR.message_types_by_name['NestedMessage']
_EXTENDEDMESSAGE = DESCRIPTOR.message_types_by_name['ExtendedMessage']
_FOREIGNMESSAGE = DESCRIPTOR.message_types_by_name['ForeignMessage']
TopLevelMessage = _reflection.GeneratedProtocolMessageType('TopLevelMessage', (_message.Message,), {
  'DESCRIPTOR' : _TOPLEVELMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.TopLevelMessage)
  })
_sym_db.RegisterMessage(TopLevelMessage)

NestedMessage = _reflection.GeneratedProtocolMessageType('NestedMessage', (_message.Message,), {
  'DESCRIPTOR' : _NESTEDMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.NestedMessage)
  })
_sym_db.RegisterMessage(NestedMessage)

ExtendedMessage = _reflection.GeneratedProtocolMessageType('ExtendedMessage', (_message.Message,), {
  'DESCRIPTOR' : _EXTENDEDMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.ExtendedMessage)
  })
_sym_db.RegisterMessage(ExtendedMessage)

ForeignMessage = _reflection.GeneratedProtocolMessageType('ForeignMessage', (_message.Message,), {
  'DESCRIPTOR' : _FOREIGNMESSAGE,
  '__module__' : 'google.protobuf.internal.more_extensions_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.internal.ForeignMessage)
  })
_sym_db.RegisterMessage(ForeignMessage)

if _descriptor._USE_C_DESCRIPTORS == False:
  ExtendedMessage.RegisterExtension(optional_int_extension)
  ExtendedMessage.RegisterExtension(optional_message_extension)
  ExtendedMessage.RegisterExtension(repeated_int_extension)
  ExtendedMessage.RegisterExtension(repeated_message_extension)

  DESCRIPTOR._options = None
  _TOPLEVELMESSAGE.fields_by_name['submessage']._options = None
  _TOPLEVELMESSAGE.fields_by_name['submessage']._serialized_options = b'(\001'
  _TOPLEVELMESSAGE.fields_by_name['nested_message']._options = None
  _TOPLEVELMESSAGE.fields_by_name['nested_message']._serialized_options = b'(\001'
  _NESTEDMESSAGE.fields_by_name['submessage']._options = None
  _NESTEDMESSAGE.fields_by_name['submessage']._serialized_options = b'(\001'
  _TOPLEVELMESSAGE._serialized_start=77
  _TOPLEVELMESSAGE._serialized_end=230
  _NESTEDMESSAGE._serialized_start=232
  _NESTEDMESSAGE._serialized_end=314
  _EXTENDEDMESSAGE._serialized_start=316
  _EXTENDEDMESSAGE._serialized_end=391
  _FOREIGNMESSAGE._serialized_start=393
  _FOREIGNMESSAGE._serialized_end=438
# @@protoc_insertion_point(module_scope)