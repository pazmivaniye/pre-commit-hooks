#!/usr/bin/env bash

! { (($# > 0)) && grep -Hn '^.\{81\}' "$@"; }
