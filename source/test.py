from pkgs.test.test_data_manager import TestDataManager

data_manager = TestDataManager('/Users/r/Documents/fastapi/testdata.xlsx')
sample_dict = data_manager.getSampleDict()
print(sample_dict['3-6'])