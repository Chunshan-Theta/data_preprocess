export BASE_DIR=/Users/gavinwang/Desktop/prior0708
export DATA_FOLDER=data
export OUTPUT_FOLDER=output
python3 process.py \
  --input_folder=$BASE_DIR/$DATA_FOLDER/ \
  --output_folder=$BASE_DIR/$OUTPUT_FOLDER/ \
  --allow_label_dict=[\"a_感謝\",\"a_抱怨\",\"a_催促\",\"a_不耐\",\"a_同意\",\"a_否定\"] \
  --skip_additional_information=True \
  --label_to_index=False \
  --label_Filter=False
