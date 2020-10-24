from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
	desc = readme.read()

setup(
	name='pastemyst',
	version='2.2.4',
	packages=find_packages(),
	author='Munchii',
	author_email='daniellmunch@gmail.com',
	license='MIT',
	description='api wrapper for pastemyst-v2 written in python.',
	long_description=desc,
	long_description_content_type='text/markdown',
	url='https://github.com/Dmunch04/pastemyst-py',
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: End Users/Desktop',
            	'Intended Audience :: Developers',
            	'License :: OSI Approved :: MIT License',
            	'Programming Language :: Python :: 3',
            	'Operating System :: OS Independent',
	],
	keywords='simple api wrapper python3 python pastemyst pastemyst.rs',
	install_requires=[
		'asks',
		'trio',
		'multio'
	]
)
