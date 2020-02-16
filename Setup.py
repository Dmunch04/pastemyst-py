import multiprocessing
from setuptools import setup

with open ('README.md', 'r') as README:
	Description = README.read ()

setup (
	name = 'pastemyst',
	version = '1.2',
	packages = ['pastemyst'],
	author = 'Munchii',
	author_email = 'contact@munchii.me',
	license = 'MIT',
	description = 'Simple API wrapper for paste.myst.rs written in Python',
	long_description = Description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/Dmunch04/PasteMyst.py',
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
            	'Intended Audience :: Developers',
            	'License :: OSI Approved :: MIT License',
            	'Programming Language :: Python :: 3',
            	'Operating System :: OS Independent',
	],
	keywords = 'simple api wrapper python3 python pastemyst pastemyst.rs'
)
