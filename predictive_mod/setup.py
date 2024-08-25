from setuptools import setup,find_packages

setup (
  author="John Carlo Alam",
  description="A package for predictive model",
  name="predictive_model",
  version='0.1.0',
  packages=find_packages(inclues=["predictive_mod", "predictive_model.*"])
)
