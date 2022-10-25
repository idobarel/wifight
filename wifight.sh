#!/bin/bash

args=("$@")
cmd="python3 -m wifight "
for ((i=0;i<$#;i++));do
    cmd+=" ${args[$i]}"
done
$cmd