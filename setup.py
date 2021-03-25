import setuptools

setuptools.setup(name='annihilation',
                 version='0.0.1',
                 description='Annihilation',
                 long_description=open('README.md').read().strip(),
                 author='Xacce',
                 author_email='thisice@gmail.com',
                 url='https://github.com/xacce/annihilation',
                 packages=setuptools.find_packages(),
                 include_package_data=True,
                 install_requires=[
                     'certifi==2018.4.16',
                     'chardet==3.0.4',
                     'idna==2.7',
                     'oyaml==0.5',
                     'pytils==0.3',
                     'PyYAML==5.4',
                     'requests==2.19.1',
                     'simplejson==3.16.0',
                     'urllib3==1.23',
                     'xmltodict==0.11.0',
                     'feedparser==5.2.1',
                     'funcsigs==1.0.2'
                 ],
                 license='MIT License',
                 zip_safe=False,
                 scripts=['annihilation/bin/annihilate.py']
                 )
