from setuptools import setup, find_packages

setup(
    name='fastapi_auth',
    version='0.1',
    url='https://github.com/the-gigi/pathology',
    install_requires=[
        "fastapi", "python-jose"
    ],
    license='MIT',
    author='Michael Nightingale',
    author_email='suslanchikmopl@gmail.com',
    description='Simple and comfortable FastAPI JWT authentication.',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    zip_safe=False
)
