from xml.etree import ElementTree as et

from dataflowlauncher.custom_exceptions import PomParseError


def parse_pom(filename):
    """Parses pom to figure identify artifact and version"""
    xml_ns = "http://maven.apache.org/POM/4.0.0"
    tree = et.ElementTree()
    tree.parse(filename)
    artifact = version = ""

    artifact_id = tree.getroot().find("{%s}artifactId" % xml_ns)
    if artifact_id is not None:
        artifact = artifact_id.text
    else:
        raise PomParseError("Can't find artifactId in POM")

    proj_version = tree.getroot().find("{%s}version" % xml_ns)
    if proj_version is not None:
        version = proj_version.text
    else:
        parent = tree.getroot().find("{%s}parent" % xml_ns)
        if parent:
            proj_version = parent.find("{%s}version" % xml_ns)
            if proj_version is not None:
                version = proj_version.text
            else:
                raise PomParseError("Can't find version in POM")

    return artifact, version


def get_jar_filename(jar_path, artifact, version, jar_name_format):
    jar_name = jar_name_format.format(artifact=artifact, version=version)
    return "{0}/{1}".format(jar_path, jar_name)
