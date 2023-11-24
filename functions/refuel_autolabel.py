import pandas as pd
import os

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.decorators.decorators import forward, setup
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe
from autolabel import LabelingAgent, AutolabelDataset

class RefuelAutolabel(AbstractFunction):

    @setup(cacheable=False, function_type="FeatureExtraction", batchable=False)
    def setup(self):
        pass

    @property
    def name(self) -> str:
        return "AutoLabel"

    @forward(
        input_signatures=[
            PandasDataframe(
                columns=["data"],
                column_types=[NdArrayType.STR],
                column_shapes=[(1, 3)],
            ),
        ],
        output_signatures=[
            PandasDataframe(
                columns=[],
            )
        ],
    )
    def forward(self, df: pd.DataFrame) -> pd.DataFrame:
        mode = df.iloc[0,0]
        config_file = df.iloc[0,1]
        dataset_file = df.iloc[0,2]
        # output_file = ""

        # if df.shape[1] > 3:
        #     output_file = df.iloc[0,3]

        print(mode, config_file, dataset_file)

        agent = LabelingAgent(config=config_file)
        ds = AutolabelDataset(dataset_file, config = config_file)

        if (mode == "plan"):
            return agent.plan(ds)
        else:
            ds = agent.run(ds)
            return ds.df.head()