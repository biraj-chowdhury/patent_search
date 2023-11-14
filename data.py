from datasets import load_dataset

dataset_dict = load_dataset(
    'HUPD/hupd',
    name='sample',
    data_files="https://huggingface.co/datasets/HUPD/hupd/blob/main/hupd_metadata_2022-02-22.feather", 
    icpr_label=None,
    train_filing_start_date='2016-01-01',
    train_filing_end_date='2016-01-21',
    val_filing_start_date='2016-01-22',
    val_filing_end_date='2016-01-31',
)


train_dataset = dataset_dict['train']
val_dataset = dataset_dict['validation']
#print(train_dataset.column_names)
print(train_dataset.column_names) 


