import mrz_reader
import os
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import time

# Initialize MRZ reader
reader = mrz_reader.reader.MRZReader(
    facedetection_protxt = "./weights/face_detector/deploy.prototxt",
    facedetection_caffemodel = "./weights/face_detector/res10_300x300_ssd_iter_140000.caffemodel",
    segmentation_model = "./weights/mrz_detector/mrz_seg.tflite",
    easy_ocr_params = {"lang_list": ["en"], "gpu": False}
)

# Get all image files from input_images directory
input_dir = "./input_images"
image_extensions = ['.jpg', '.jpeg', '.png']
image_files = []

for file in os.listdir(input_dir):
    file_path = os.path.join(input_dir, file)
    if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in image_extensions):
        image_files.append(file_path)

# Set up Excel file and formatting
excel_path = "mrz_results.xlsx"
column_names = ["passport_image", "mrz", "confidence"]

# Create a new Excel file with headers if it doesn't exist
if not os.path.exists(excel_path):
    # Create an empty DataFrame with just the headers
    header_df = pd.DataFrame(columns=column_names)
    
    # Create Excel writer with xlsxwriter engine
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        header_df.to_excel(writer, index=False, sheet_name='MRZ Results')
        
        # Get workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['MRZ Results']
        
        # Set column widths
        worksheet.set_column('A:A', 40)  # Passport image path
        worksheet.set_column('B:B', 50)  # MRZ text
        worksheet.set_column('C:C', 15)  # Confidence
        
        # Add header format
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'bg_color': '#D9D9D9',
            'border': 1
        })
        
        # Write headers with formatting
        for col_num, value in enumerate(header_df.columns.values):
            worksheet.write(0, col_num, value, header_format)
    
    print(f"Created new results file: {excel_path}")

# Process each image with progress bar
for i, image_path in enumerate(tqdm(image_files, desc="Processing images")):
    try:
        # Process image
        text_results, segmented_image, face = reader.predict(
            image_path,
            do_facedetect=True,
            preprocess_config={
                "do_preprocess": True,
                "skewness": True,
                "delete_shadow": True,
                "clear_background": True
            }
        )
        
        # Combine MRZ text
        combined_mrz = ""
        
        for result in text_results:
            bbox, text, confidence = result
            combined_mrz += text + "\n"
        
        # Create a single-row DataFrame for this result
        result_data = {
            "passport_image": image_path,
            "mrz": combined_mrz.strip(),
            "confidence": confidence
        }
    except Exception as e:
        # Handle errors
        result_data = {
            "passport_image": image_path,
            "mrz": f"Error: {str(e)}",
            "confidence": 0
        }
    
    # Create a DataFrame with just this result
    result_df = pd.DataFrame([result_data])
    
    # Read existing Excel file to get current data
    try:
        existing_df = pd.read_excel(excel_path)
        # Append new result (use mode='a' for append mode)
        with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            result_df.to_excel(writer, index=False, header=False, sheet_name='MRZ Results', startrow=len(existing_df) + 1)
    except Exception as append_error:
        print(f"Error appending to Excel: {str(append_error)}. Creating new file.")
        # If append fails, create a new file with all data processed so far
        combined_df = result_df
        if os.path.exists(excel_path):
            try:
                existing_df = pd.read_excel(excel_path)
                combined_df = pd.concat([existing_df, result_df], ignore_index=True)
            except Exception as read_error:
                print(f"Error reading existing file: {str(read_error)}")
        
        # Write complete dataframe to a new file
        backup_path = f"mrz_results_backup_{int(time.time())}.xlsx"
        with pd.ExcelWriter(backup_path, engine='xlsxwriter') as writer:
            combined_df.to_excel(writer, index=False, sheet_name='MRZ Results')
            
            # Format the new file
            workbook = writer.book
            worksheet = writer.sheets['MRZ Results']
            
            # Set column widths
            worksheet.set_column('A:A', 40)
            worksheet.set_column('B:B', 50)
            worksheet.set_column('C:C', 15)
            
            # Add header format
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'bg_color': '#D9D9D9',
                'border': 1
            })
            
            # Write headers with formatting
            for col_num, value in enumerate(combined_df.columns.values):
                worksheet.write(0, col_num, value, header_format)
        
        print(f"Created backup file with all processed results: {backup_path}")
    
    # Small delay to ensure file is not locked
    time.sleep(0.1)

print(f"All results have been saved to {excel_path}")