from setuptools import setup

setup(
    name='qtile-widget-strava',
    packages=['stravawidget'],
    version='0.1.0',
    description='A qtile widget to show Strava stats.',
    author='elParaguayo',
    url='https://github.com/elparaguayo/qtile-widget-stats',
    license='MIT',
    install_requires=['qtile>0.14.2', 'dateutil', 'stravalib', 'units']
)
