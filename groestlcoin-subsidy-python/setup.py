from distutils.core import setup, Extension

groestlcoin_module = Extension('groestlcoin_subsidy', sources = ['groestlcoin_subsidy.cpp'])

setup (name = 'groestlcoin_subsidy',
       version = '1.0',
       description = 'Subsidy function for GroestlCoin',
       ext_modules = [groestlcoin_module])
