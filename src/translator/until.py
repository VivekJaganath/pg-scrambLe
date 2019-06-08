import os
import yaml
import logging
import event

log = logging.getLogger(__name__)
evtlog = event.get_logger('validator.events')


def read_descriptor_files(files):
    """
    Loads the VNF descriptors provided in the file list. It builds a
    dictionary of the loaded descriptor files. Each entry has the
    key of the VNF combo ID, in the format 'vendor.name.version'.
    :param files: filename list of descriptors
    :return: Dictionary of descriptors. None if unsuccessful.
    """

    descriptors = {}
    for file in files:
        content = read_descriptor_file(file)
        if not content:
            continue
        did = descriptor_id(content)
        if did in descriptors.keys():
            log.error("Duplicate descriptor in files: '{0}' <==> '{1}'"
                      .format(file , descriptors[did]))
            continue
        descriptors[did] = file
    return descriptors


def read_descriptor_file(file):
    """
    Reads a SONATA descriptor from a file.
    :param file: descriptor filename
    :return: descriptor dictionary
    """

    descriptor = file

    if not descriptor:
        evtlog.log("Invalid descriptor",
                   "Couldn't read descriptor file: '{0}'".format(file),
                   file,
                   'evt_invalid_descriptor')
        return

    if 'vendor' not in descriptor or \
            'name' not in descriptor or \
            'version' not in descriptor:
        log.warning("Invalid SONATA descriptor file: '{0}'. Missing "
                    "'vendor', 'name' or 'version'. Ignoring."
                    .format(file))
        return

    return descriptor


def descriptor_id(descriptor):
    """
    Provides the descriptor id of the specified descriptor content
    :param descriptor: descriptor content dict
    :return: descriptor id
    """
    return build_descriptor_id(descriptor['vendor'],
                               descriptor['name'],
                               descriptor['version'])


def build_descriptor_id(vendor, name, version):
    """
    Assemble the descriptor id based on its vendor, name and version.
    :param vendor: descriptor vendor
    :param name: descriptor name
    :param version: descriptor version
    :return: descriptor id
    """
    return vendor + '.' + name + '.' + version


def list_files(path, extension):
    """
    Retrieves a list of files with the specified extension in a given
    directory path.
    :param path: directory to search for files
    :param extension: extension of files
    :return: list of files
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                file_list.append(os.path.join(root, file))
    return file_list


def strip_root(path):
    """
    Remove leading slash of a path
    """
    if type(path) is not str:
        return path
    return path[1:] if path[0] == '/' else path


class CountCalls(object):
    """Decorator to determine number of calls for a method"""

    def __init__(self, method):
        self.method = method
        self.counter = 0

    def __call__(self, *args, **kwargs):
        self.counter += 1
        return self.method(*args, **kwargs)

