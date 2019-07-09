#python3
import re
import json
import sys, os
from absl import app
from absl import flags
from os import listdir
from os.path import isfile, join




'''
load args
'''
FLAGS = flags.FLAGS

flags.DEFINE_string('allow_label_dict', "[\"a_感謝\",\"a_抱怨\",\"a_催促\",\"a_不耐\",\"a_同意\",\"a_否定\"]", 'format: [\"a_感謝\",\"a_抱怨\",\"a_催促\",\"a_不耐\",\"a_同意\",\"a_否定\"]')
flags.DEFINE_string('input_folder', "./data", "loaction of the input folder")
flags.DEFINE_string('output_folder', "./output", "loaction of the output folder")
flags.DEFINE_string('output_label', "processed", "label for the output file.")
flags.DEFINE_bool('skip_additional_information', True, "skip additional information of sentence (like time)")
flags.DEFINE_bool('label_to_index',False, 'change label text to array index')
flags.DEFINE_bool('label_Filter', True, "filing False if want to process the all of labels.(if true, don't forget to filing allow_label_dict)")


        


def main(argv):
    '''
    loading valid labels, only those labels will be process.
    example and testing:
    allow_label_dict="[\"h_詢問處理方式\",\"h_要求回覆\",\"h_已過\",\"h_調情\",\"h_了解\",\"h_進不去\",\"h_投訴\",\"h_詢問處理方式\",\"h_要求回覆\",\"h_已過\",\"h_調情\",\"h_了解\",\"h_進不去\",\"h_投訴\",\"h_問_充值\",\"h_問_充值渠道\",\"h_問_格式\",\"h_問_紅包\",\"h_問_客服電話\",\"h_問_提現手續費\",\"h_問_投訴入口\",\"h_問_怎麼提現\",\"h_問_無法充值\",\"h_問_無法上傳\",\"h_問_憑證上傳方法\",\"h_問_聲請代理\",\"h_輸錢\",\"h_咒罵\",\"a_感謝\",\"a_抱怨\",\"a_催促\",\"a_不耐\",\"a_同意\",\"a_否定\",\"e_遊戲名稱或內容\",\"e_充值渠道\",\"e_金額\",\"e_姓名\",\"e_銀行\",\"e_日期\",\"e_時間\",\"e_時間間隔\",\"e_金幣\",\"e_訂單號\"]"
    '''
    allow_label_dict = json.loads(FLAGS.allow_label_dict)


    '''
    loading files need be processed,
    catch name of those files
    '''
    source_files = [f for f in listdir(FLAGS.input_folder) if isfile(join(FLAGS.input_folder, f))]
    file_names = []
    for sf in source_files:
        if not sf[-3:] == "ann" and not sf[-3:] == "txt":continue
        f =  sf[:-4]
        if not f in file_names:file_names.append(f)


    '''
    start to loading and processing the each content of file
    '''
    for f_name in file_names: 


        '''
        open file(.txt) and tagging data (.ann)
        '''
        with open(FLAGS.input_folder+f_name+".txt") as f_txt, open(FLAGS.input_folder+f_name+".ann") as f_ann:
            
            '''
            insert split symbol to repalce line break symbol (\n)
            '''

            # defined
            split_symbol ="<|split|>"
            split_symbol_len = len(split_symbol)



            # loadng source content
            content,source = split_symbol,""
            for line in f_txt.readlines():
                #preporcess
                line_cleaned = re.sub(r'\t', ' ', line)

                #save source data without processed
                source += line

                #replace \n wilth split symbol 
                content+=(line_cleaned).strip('\n')+split_symbol



            '''
            1.catch tag resource
            2.process to catch the label and label's location
            3.output format line based 2th step
            '''
            #output data
            output_file_data = ""
            for tag_source in f_ann.readlines():


                #skip invalid information 
                if tag_source[0]!="T":continue


                '''
                cutting sentence and convert to array,
                catch label of tag, the index of label
                '''
                tag_array = re.split(' |\t|\n',tag_source)
                label = tag_array[1]
                start_labeling_index=int(tag_array[2])
                end_labeling_index=int(tag_array[3])

                
                '''
                fine tune location of labels, because insert split symbol into sentence in previous steps.
                '''
                line_index = source[:start_labeling_index].count("\n")
                start_index = start_labeling_index +(split_symbol_len-1)*line_index+split_symbol_len
                end_index = end_labeling_index +(split_symbol_len-1)*line_index+split_symbol_len
                


                #catching full content of sentence based on location of labels and the split symbol
                sentence_start_index = content[:start_index].rfind(split_symbol)+split_symbol_len
                sentence_end_index = content[end_index:].index(split_symbol)+end_index
                sentence_content = (content[sentence_start_index:sentence_end_index])

                #skip additional information of sentence (like time)
                skip_len = 40
                sentence_content_without_additional = sentence_content[skip_len:]

                
                #temporarily saving the label and content
                if not FLAGS.label_Filter or label in allow_label_dict:
                    if FLAGS.label_to_index: label = str(allow_label_dict.index(label))
                    if FLAGS.skip_additional_information: 
                        output_file_data+=(label+","+sentence_content_without_additional)+"\n"
                    else:
                        output_file_data+=(label+" "+sentence_content)+"\n"

            #write file with processed files
            with open(FLAGS.output_folder+FLAGS.output_label+"_"+f_name+".csv","w") as output_file:
                output_file.write(output_file_data)

if __name__ == '__main__':
    app.run(main)












   
