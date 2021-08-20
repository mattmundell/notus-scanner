# Copyright (C) 2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from uuid import UUID

from unittest import TestCase, mock

from notus.scanner.messages.message import Message
from notus.scanner.messaging.mqtt import MQTTPublisher


class MQTTPublisherTestCase(TestCase):
    def test_publish(self):
        client = mock.MagicMock()
        publisher = MQTTPublisher(client)

        created = datetime.fromtimestamp(1628512774)
        message_id = UUID('63026767-029d-417e-9148-77f4da49f49a')
        group_id = UUID('866350e8-1492-497e-b12b-c079287d51dd')
        message = Message(
            message_id=message_id, group_id=group_id, created=created
        )

        publisher.publish(message)

        client.publish.assert_called_with(
            None,
            '{"message_id": "63026767-029d-417e-9148-77f4da49f49a", '
            '"message_type": null, '
            '"group_id": "866350e8-1492-497e-b12b-c079287d51dd", '
            '"created": 1628512774.0}',
            qos=1,
        )
