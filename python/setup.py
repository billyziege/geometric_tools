from setuptools import setup

setup(
    name='geometric_tools',
    version='0.0.0',
    description='A package for describing and manipulating geometric objects.',
    url='https://github.com/billyziege/geometric_tools',
    author='BRandon Zerbe',
    author_email='zerbe@lanl.gov',
    license='Creative commons',
    packages=['geometric_tools'],
    install_requires=['numpy'],

    classifiers=[
        'Development Status :: 1-Remedial',
        'Intended Audience :: Science/Research',
        'License :: Creative Commons',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5+',
    ],
)
