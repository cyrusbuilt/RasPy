"""Image capture utility methods."""


from raspy.devices.picamera import image_encoding


def get_encoding_file_extension(encoding):
    """Get the encoding file extension.

    :param int encoding: The image encoding format.
    :returns: The file extension associated with the specified format.
    :rtype: str
    """
    if encoding == image_encoding.BITMAP:
        ext = "bmp"
    elif encoding == image_encoding.GIF:
        ext = "gif"
    elif encoding == image_encoding.JPEG:
        ext = "jpg"
    elif encoding == image_encoding.PNG:
        ext = "png"
    else:
        ext = ""
    return ext
