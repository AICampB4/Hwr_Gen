# Hwr_Gen
##Data: CVL and IAM offline handwritten text image  
  
##Model reference:   
https://github.com/herobd/handwriting_line_generation  
  
##Data Normalization:   
Convert xml format of IAM to the csv with the same format with CVL. The execute file can be found in Data_Processing\parseXMLtoCSV_IAM.py. The path of xml folder and csv folder can be set up in Data_Processing\configs\config_IAM_XMLtoCSV.json. To execute **!python Data_Processing\parseXMLtoCSV_IAM.py -c path_to_config_file**   
  
##Data preparation  
Move all subdir out of the dir and delete it. Can found in Data_Processing/Data_Transformation.py. Only use for lines, sentences and words dataset with IAM/CVL layout. The path of the dataset can change in Data_Processing\configs\config_data_trans.json. To execute **!python Data_Processing/Data_Transformation.py -c path_to_config_file**  
  
##Train test split  
Split Data to Train test val set which each set has all forms (words, sentences, lines, pages, forms) with ratio train 0.7, validation 0.15 and test 0.15. The execution file can found in Data_Processing/Data_Transformation.py. The path of original database and desired output directory can be found at Data_Processing\configs\config_data_trans.json. To execute: **!python Data_Processing/Data_Transformation.py -c path_to_config_file**   
  
##Data Augmentation  
Apply the following methods: apply_tensmeyer_brightness, apply_random_brightness, apply_random_color_rotation, affine_trans, add_random_lines, mmd_crop, bad_crop, warp_image, skeletonize, deskew. To apply one of those methods:   **!python src/path/augmentation.py -f method_name -c src/path/configuration.json**  
  
