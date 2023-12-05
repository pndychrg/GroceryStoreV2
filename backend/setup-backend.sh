#!/bin/bash
python3 -m venv venv &&
activate(){
	. venv/bin/activate
}
activate && wait && pip install -r requirements.txt