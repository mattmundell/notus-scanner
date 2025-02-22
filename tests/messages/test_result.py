# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2021-2023 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from datetime import datetime, timezone
from unittest import TestCase
from uuid import UUID

from notus.scanner.errors import MessageParsingError
from notus.scanner.messages.message import MessageType
from notus.scanner.messages.result import ResultMessage, ResultType


class ResultMessageTestCase(TestCase):
    def test_constructor(self):
        message = ResultMessage(
            scan_id="scan_1",
            host_ip="1.1.1.1",
            host_name="foo",
            oid="1.2.3.4.5",
            value="A Vulnerability has been found",
            uri="file://foo/bar",
        )

        self.assertIsInstance(message.message_id, UUID)
        self.assertIsInstance(message.group_id, str)
        self.assertIsInstance(message.created, datetime)

        self.assertEqual(message.message_type, MessageType.RESULT)
        self.assertEqual(message.topic, "scanner/scan/info")

        self.assertEqual(message.scan_id, "scan_1")
        self.assertEqual(message.host_ip, "1.1.1.1")
        self.assertEqual(message.host_name, "foo")
        self.assertEqual(message.oid, "1.2.3.4.5")
        self.assertEqual(message.value, "A Vulnerability has been found")

        self.assertEqual(message.result_type, ResultType.ALARM)
        self.assertEqual(message.port, "package")
        self.assertEqual(message.uri, "file://foo/bar")

    def test_serialize(self):
        created = datetime.fromtimestamp(1628512774)
        message_id = UUID("63026767-029d-417e-9148-77f4da49f49a")
        group_id = "866350e8-1492-497e-b12b-c079287d51dd"

        message = ResultMessage(
            created=created,
            message_id=message_id,
            group_id=group_id,
            scan_id="scan_1",
            host_ip="1.1.1.1",
            host_name="foo",
            oid="1.2.3.4.5",
            value="A Vulnerability has been found",
            uri="file://foo/bar",
        )

        serialized = message.serialize()
        self.assertEqual(serialized["created"], 1628512774.0)
        self.assertEqual(
            serialized["message_id"], "63026767-029d-417e-9148-77f4da49f49a"
        )
        self.assertEqual(
            serialized["group_id"], "866350e8-1492-497e-b12b-c079287d51dd"
        )
        self.assertEqual(serialized["message_type"], "result.scan")
        self.assertEqual(serialized["scan_id"], "scan_1")
        self.assertEqual(serialized["host_ip"], "1.1.1.1")
        self.assertEqual(serialized["host_name"], "foo")
        self.assertEqual(serialized["oid"], "1.2.3.4.5")
        self.assertEqual(serialized["value"], "A Vulnerability has been found")
        self.assertEqual(serialized["uri"], "file://foo/bar")
        self.assertEqual(serialized["port"], "package")
        self.assertEqual(serialized["result_type"], "ALARM")

    def test_deserialize(self):
        data = {
            "message_id": "63026767-029d-417e-9148-77f4da49f49a",
            "group_id": "866350e8-1492-497e-b12b-c079287d51dd",
            "created": 1628512774.0,
            "message_type": "result.scan",
            "scan_id": "scan_1",
            "host_ip": "1.1.1.1",
            "host_name": "foo",
            "oid": "1.2.3.4.5",
            "value": "A Vulnerability has been found",
            "uri": "file://foo/bar",
            "port": "package",
            "result_type": "ALARM",
        }

        message = ResultMessage.deserialize(data)
        self.assertEqual(
            message.message_id, UUID("63026767-029d-417e-9148-77f4da49f49a")
        )
        self.assertEqual(
            message.group_id, "866350e8-1492-497e-b12b-c079287d51dd"
        )
        self.assertEqual(
            message.created,
            datetime.fromtimestamp(1628512774.0, tz=timezone.utc),
        )
        self.assertEqual(message.message_type, MessageType.RESULT)

        self.assertEqual(message.scan_id, "scan_1")
        self.assertEqual(message.host_ip, "1.1.1.1")
        self.assertEqual(message.host_name, "foo")
        self.assertEqual(message.oid, "1.2.3.4.5")
        self.assertEqual(message.value, "A Vulnerability has been found")
        self.assertEqual(message.uri, "file://foo/bar")
        self.assertEqual(message.port, "package")
        self.assertEqual(message.result_type, ResultType.ALARM)

    def test_deserialize_invalid_message_type(self):
        data = {
            "message_id": "63026767-029d-417e-9148-77f4da49f49a",
            "group_id": "866350e8-1492-497e-b12b-c079287d51dd",
            "created": 1628512774.0,
            "message_type": "scan.status",
            "scan_id": "scan_1",
            "host_ip": "1.1.1.1",
            "host_name": "foo",
            "oid": "1.2.3.4.5",
            "value": "A Vulnerability has been found",
            "uri": "file://foo/bar",
            "port": "package",
            "result_type": "ALARM",
        }
        with self.assertRaisesRegex(
            MessageParsingError,
            "Invalid message type MessageType.SCAN_STATUS for "
            "ResultMessage. Must be MessageType.RESULT.",
        ):
            ResultMessage.deserialize(data)

    def test_deserialize_invalid_result_type(self):
        data = {
            "message_id": "63026767-029d-417e-9148-77f4da49f49a",
            "group_id": "866350e8-1492-497e-b12b-c079287d51dd",
            "created": 1628512774.0,
            "message_type": "result.scan",
            "scan_id": "scan_1",
            "host_ip": "1.1.1.1",
            "host_name": "foo",
            "oid": "1.2.3.4.5",
            "value": "A Vulnerability has been found",
            "uri": "file://foo/bar",
            "port": "package",
            "result_type": "foo",
        }

        with self.assertRaisesRegex(
            MessageParsingError,
            "error while parsing 'result_type', 'foo' is not a valid"
            " ResultType",
        ):
            ResultMessage.deserialize(data)
