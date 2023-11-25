import pandas as pd
import os

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe
from autolabel import LabelingAgent, AutolabelDataset

class RefuelAutolabel(AbstractFunction):

    @setup(cacheable=False, batchable=False)
    def setup(self):
        """
        no actions are needed to set up the Refuel Autolabel function
        """
        pass

    @property
    def name(self) -> str:
        return "AutoLabel"

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["data"],
                column_types=[NdArrayType.STR],
                column_shapes=[(1, None)],
            ),
        ],
        output_signatures=[
            PandasDataframe(
                columns=[],
            )
        ],
    )
    def forward(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Plan or run the labeling task specfied by the given arguments to Refuel Autolabel

        input: 
            df (pd.DataFrame) -> dataframe containing the function args:
                1. the mode to execute in (plan, run, explain)
                2. config file
                3. dataset file
                4. (optional) output file
                5. (optional) max items
                6. (optional) start index
                7. (optional) skip eval
                note that items 4-7 can be passed when using the "run" mode; they correspond to optional arguments in LabelingAgent.run()
        output:
            out (pd.DataFrame) -> dataframe containing the results of planning or running a labeling task with Refuel Autolabel
        """
        mode = df.iloc[0,0]
        config_file = df.iloc[0,1]
        dataset_file = df.iloc[0,2]
    
        # configure the labeling agent and autolabel dataset for Refuel
        agent = LabelingAgent(config=config_file)
        ds = AutolabelDataset(dataset_file, config = config_file)

        """ 
        the three types of labeling tasks are plan, run, and explain
            1. plan -> estimate the cost of the labeling task and provide an example prompt
            2. run -> label the provided dataset using prompts generated from the config file
            3. explain -> prompt the LLM to justify why each label was chosen for examples in the dataset
        """
        if (mode == "plan"):
            return agent.plan(ds)
        elif (mode == "run"):
            output_file = None
            max_items = None
            start_idx = 0
            skip_eval = False

            # check for optional arguments to LabelingAgent.run()
            if df.shape[1] >= 4:
                output_file = df.iloc[0,3]
            if df.shape[1] >= 5:
                max_items = int(df.iloc[0,4])
            if df.shape[1] >= 6:
                start_idx = int(df.iloc[0,5])
            if df.shape[1] >= 7:
                skip_eval = True if df.iloc[0,5].lower() == "true" else False

            ds = agent.run(ds, output_name = output_file, max_items = max_items, start_index = start_idx, skip_eval = skip_eval)
            return ds.df.head()
        elif (mode == "explain"):
            return agent.generate_explanations(dataset_file)
        else:
            return pd.DataFrame()