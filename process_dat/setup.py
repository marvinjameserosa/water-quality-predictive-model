from setuptools import setup,find_packages

setup (
  author="Mahid Dandamun",
  description="A package for processing data",
  name="process_data",
  version='0.1.0',
  packages=find_packages(inclues=["process_dat", "process_data.*"])
)
