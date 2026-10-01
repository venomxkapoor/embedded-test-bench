import pandas as pd
import pytest

@pytest.fixture
def good_frame():
    return pd.DataFrame({'timestamp': [0.,1.,2.,3.,4.,5.], 'voltage': [3.3,3.31,3.29,3.32,3.3,3.31], 'temperature': [25.,25.1,25.2,25.3,25.4,25.5]})
