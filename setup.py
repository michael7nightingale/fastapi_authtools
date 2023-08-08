from setuptools import setup, find_packages

setup(
    name='fastapi_authtools',
    version='0.5',
    url='https://github.com/michael7nightingale/fastapi_authtools',
    install_requires=[
        "fastapi==0.100.0", "python-jose",
        'pydantic==2.0.2'
    ],
    license='MIT',
    author='Michael Nightingale',
    author_email='suslanchikmopl@gmail.com',
    description='Simple and comfortable FastAPI JWT authentication.',
    packages=find_packages(exclude=['tests', "app.py"]),
    long_description_content_type="Markdown",
    long_description=open('README.md').read(),
    zip_safe=False
)
