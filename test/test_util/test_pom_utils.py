from unittest import TestCase, main

from dataflowlauncher.custom_exceptions import PomParseError
from dataflowlauncher.utils.pom_utils import get_jar_filename, parse_pom
from rootpath import get_absolute_path


class TestPomUtils(TestCase):
    def test_get_jar_filename(self):
        self.assertEqual(get_jar_filename('target',
                                          'test-project',
                                          '1.0.0'),
                         'target/test-project-1.0.0.jar')

    def test_get_custom_jar_filename(self):
        self.assertEqual(get_jar_filename('root_project/target',
                                          'test-project',
                                          '1.0.0'),
                         'root_project/target/test-project-1.0.0.jar')

    def test_project_with_version(self):
        file = "_testing/pom_with_version.xml"
        self.assertEqual(parse_pom(get_absolute_path(file)),
                         ('pom_artifact', '1.0.1-SNAPSHOT'))

    def test_project_with_parent_version(self):
        file = "_testing/pom_with_parent_version.xml"
        self.assertEqual(parse_pom(get_absolute_path(file)),
                         ('pom_artifact', '1.0.3-SNAPSHOT'))

    def test_project_with_no_version(self):
        with self.assertRaises(PomParseError):
            file = "_testing/pom_with_no_version.xml"
            self.assertEqual(parse_pom(get_absolute_path(file)),
                             ('pom_artifact', ''))


if __name__ == '__main__':
    main()
