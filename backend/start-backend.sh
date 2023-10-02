#!/bin/bash -x


activate(){
	. venv/bin/activate
}
activate &&
wait &&
python3 run.py

