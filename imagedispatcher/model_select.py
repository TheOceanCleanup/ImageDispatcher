import datetime


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
    if message["timestamp"].hour < 12:  # Morning only
        return ("testdeploy1", "yolo_v4", 2)
    else:
        return ("testdeploy1", "yolo_v4", 2)
