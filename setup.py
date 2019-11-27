from setuptools import setup

setup(
    name = 'xtremeAPI',
    version = '2.1',
    packages = ['xtremeAPI','xtremeAPI.lib'],
    entry_points = {
        'console_scripts': [
            'xtremeCreate = xtremeAPI.__main__:create',
            'xtremeUpdate = xtremeAPI.__main__:update',
        ]
    })

