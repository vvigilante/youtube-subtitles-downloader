from setuptools import setup, find_packages
import os


def clean_dist():
    dist_path = 'dist'
    if os.path.isdir('dist'):
        files = [f for f in os.listdir(dist_path) if
                 os.path.isfile(os.path.join(dist_path, f))]
        for file in files:
            os.remove(os.path.join(dist_path, file))


def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


def upload_to_pypi():
    os.system("twine upload dist/*")


clean_dist()

setup(
    name='ytsubtitles',
    version="0.1.0",
    author='Vincenzo Vigilante, Gioele Crispo',
    author_email='info@vvigilante.com',
    package_dir={'ytsubtitles': 'ytsubtitles'},
    packages=find_packages('.'),
    entry_points={
        'console_scripts': [
            'ytsubtitles = ytsubtitles:download_subs_arguments'
        ]
    },
    # scripts=['bin/script1', 'bin/script2'],
    url='https://github.com/vvigilante/decoripy.git',
    license='MIT',
    license_file='LICENSE',
    platform='any',
    description='ytsubtitles makes you download subs from youtube.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read_file('requirements.txt').splitlines(),
    python_requires='>=3.4',
    package_data={
        # '': ['package_data.dat'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

upload_to_pypi()
