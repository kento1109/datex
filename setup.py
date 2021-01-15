from setuptools  import setup, find_packages

setup(name='datex',
      version='0.1.0',
      description='DATE mentions EXtraction tool',
      author='MICIN, Inc.',
      url="https://github.com/micin-jp/datex",
      packages=find_packages("src"),
      package_dir={'': 'src'},
      package_data={'': ['keys/*']},
      include_package_data=True,
     )