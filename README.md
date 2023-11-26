# EvaDB x Refuel Autolabel

The primary aim of this project is to integrate the [Refuel Autolabel](https://github.com/refuel-ai/autolabel) project into EvaDB. 
Autolabel is used to automatically label datasets using large language models. This reduces the time and cost of producing labeling data while preserving accuracy.

## Table of Contents

1. [Getting Started](#1-getting-started)
2. [Project Overview](#2-project-overview)
3. [Project Structure](#3-project-structure)

## 1. Getting Started

To get started, clone this repository

```
git clone https://github.com/nathankrish/refuel-evadb.git
```

Then create a virtual environment and install the appropriate requirements

On Mac/Linux

```
python3 -m venv evadb_env
source evadb_env/bin/activate
pip install -r requirements.txt
```

On Windows

```
py -m venv evadb_env
evadb_env\bin\Activate.bat
pip install -r requirements.txt
```

After this, you can run the notebooks and python files using the Python interpreter from evadb_env


## 2. Project Overview

This project involved integrating parts of Refuel Autolabel into EvaDB as a custom function. 
In particular, I focused on Refuel's [LabelingAgent](https://docs.refuel.ai/autolabel/reference/labeler/?h=labelingagent#src.autolabel.labeler.LabelingAgent) since it is the class which is used to plan, run, and explain autolabeling tasks when using Autolabel's Python SDK.

Create the RefuelAutolabel function in EvaDB with the following snippet

```
import evadb
cursor = evadb.connect().cursor()
create_function_query = f"""CREATE FUNCTION IF NOT EXISTS RefuelAutolabel
            IMPL  './functions/refuel_autolabel.py';
            """
cursor.query("DROP FUNCTION IF EXISTS RefuelAutolabel;").execute()
cursor.query(create_function_query).execute()
```

The plan, run, and explain methods in `LabelingAgent` can be then be used from EvaDB with the following queries

```
# plan autolabeling task
query= f""" SELECT RefuelAutolabel("plan", 'config_banking.json', 'seed.csv');"""

# run autolabeling task, second call has optional arguments
query= f""" SELECT RefuelAutolabel("run", 'config_banking.json', 'seed.csv');"""
query= f""" SELECT RefuelAutolabel("run", 'config_walmart.json', 'seed.csv', 'output.csv', '10', '1', 'false');"""

# explain the labels generated for each example
query= f"""SELECT RefuelAutolabel("explain", 'config_banking.json', 'seed.csv');"""
```


## 3. Project Structure

The implementation of the RefuelAutolabel function to be used in EvaDB is contained in

```
functions/
    |-- refuel_autolabel.py
```

You can bring this function into EvaDB using the following snippet

```
create_function_query = f"""CREATE FUNCTION IF NOT EXISTS RefuelAutolabel
            IMPL  './functions/refuel_autolabel.py';
            """
cursor.query("DROP FUNCTION IF EXISTS RefuelAutolabel;").execute()
cursor.query(create_function_query).execute()
```

In the examples folder, the `autolabel_pythonic.ipynb` file shows how to use Refuel Autolabel in a typical Pythonic setting. This was mostly an exploratory exercise to understand how the library worked before trying to integrate it into EvaDB.
The `autolabel_evadb.ipynb` file shows how to use Refuel Autolabel through the custom function in EvaDB.
You can use the plan, run, and explain functions from `LabelingAgent` through the `RefuelAutolabel` function I defined.

This code is also in the self contained python files `autolabel_pythonic.py` and `autolabel_evadb.py`

You will need a `my_secrets.py` file in the examples folder with this line
```
OPENAI_KEY = <Your OpenAI API Key>
```