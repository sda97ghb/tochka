#!/usr/bin/env bash

printf 'from shortcuts import replicate\nreplicate()' | ./manage.py shell
