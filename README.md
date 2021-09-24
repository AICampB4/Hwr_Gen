# Hwr_Gen
* Data: CVL and IAM offline handwritten text image
* Model reference: ./https://github.com/herobd/handwriting_line_generation
* Data Normalization: Convert xml format of IAM to the csv with the same format with CVL
* Data preparation - Move all subdir out of the dir and delete it
* Train test split - Split Data to Train test val set which each set has all forms (words, sentences, lines, pages, forms) with ratio train 0.7, validation 0.15 and test 0.15 
* Data Augmentation: Apply the following methods: apply_tensmeyer_brightness, apply_random_brightness, apply_random_color_rotation, affine_trans, add_random_lines, mmd_crop, bad_crop, warp_image, skeletonize, deskew. To apply one of those methods: **!python src/path/augmentation.py -f method_name -c src/path/configuration.json**
