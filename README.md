# Thermal-Impedance-SPICE-Modeling
Thermal Impedance SPICE Modeling software based on the bachelor thesis "Simplified Heat Simulation of PCB Circuit" at Chalmers University of Technology: https://odr.chalmers.se/items/fc7c82ce-7964-4356-9dae-14a6085a0620

## How to run the software as a docker image
You can run the jupyter notebook as a docker image using docker-compose with the token=easy or with plain docker using automatically generated token available from the docker cli. The notebook can be accessed from the browser with the address localhost:8888.

```command
docker-compose up
```

## How to run the software locally
You can also install all the python packages using the following commands in the same directory as the requirements.txt

```command
python -m pip install --upgrade pip
```

```command
python -m pip install -r requirements.txt
```

Then to start the jupyter notebook run the following command inside the notebook folder

```command
jupyter notebook
```

On windows this opens the notebook automatically otherwise the notebook can be accessed from the browser with the address localhost:8888 using the token provided in the commanline.
