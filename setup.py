from distutils.core import setup

setup(
    name='argchoose',
    packages=['argchoose'],
    version='0.1',
    license='MIT',
    description='Choose which functions to execute by simply creating clear cmdline menu and cmdline args parser in one step',
    author='Paweł Kusiński',
    author_email='KusinskiP@protonmail.com',
    url='https://github.com/Djkusik/ArgChooser',
    download_url='https://github.com/Djkusik/ArgChooser/archive/v0.1.tar.gz',
    keywords=['cmdline', 'function', 'parser', 'menu', 'commandline', 'execute', 'create', 'args', 'arguments', 'easy', 'fast'],
    install_requires=[
        'PyInquirer',
        'argparse',
    ],
    classifiers=[
        'Environment :: Console',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ]
)
