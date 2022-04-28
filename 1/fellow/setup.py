from setuptools import setup, find_namespace_packages

setup(
    name='fellow',
    version='0.1',
    description='«Fellow» is your personal friend and assistant with a contact book, notes and some additional features.',
    url='https://github.com/maxdetsyk/goit_group_project.git',
    author='Essence Team',
    author_email='flyingcircus@example.com',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    entry_points={'console_scripts': ['fellow = fellow.main:main']}
)