#!/bin/bash

py.test --pep8 --flakes --cov . . $*
