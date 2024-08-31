from setuptools import setup

setup(
  name="process_data",
  version="0.1.0",
  author="Mahid Dandamun",
  description="A package for the  data manipulations",
  packages=["data_package", "data_package.data_cleaning", "data_package.process_data", "predictive_model", "predictive_model.forecast"],
  install_includes=['numpy']
)