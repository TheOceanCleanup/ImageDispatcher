# ImageDispatcher - ServiceBus listeners that calls Image Recognition model to detect plastic objects in queued images
# Copyright (C) 2020-2021 The Ocean Cleanup™
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime


def select_service(message):
    """
    Select the webservice / endpoint to offer the image to. Should return the
    endpoint name, model used and the version. The latter two are for
    administration purposes only.

    # TODO: Check if we want to detect model and version automatically instead.
    #       Requires integration with AzureML, and we need to think if the
    #       overhead of making calls to Azure API is worth it.

    :param message:     The message, use this to determine the model
    :returns:           A tuple of the form
                        (<service name>, <model name>, <model_version>)
    """
    # TODO make actual differentation here
    timestamp = datetime.strptime(message['timestamp'], "%Y-%m-%dT%H:%M:%S")
    if timestamp.hour < 12:  # Morning only
        return ("yolov5", "yolov5", 3)
    else:
        return ("yolov5", "yolov5", 3)
