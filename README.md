# 🛂 AI-Powered MRZ Passport Reader from Image

This project is an AI-based **Machine Readable Zone (MRZ)** reader designed to automatically extract MRZ text from a batch of passport images. It uses segmentation, face detection, image preprocessing, and OCR to accurately identify and log passport details.

---

## 🚀 Features

- 📸 **Batch Processing** of passport images
- 🧠 **MRZ Region Segmentation** using a TensorFlow Lite model
- 🧾 **Text Extraction** using EasyOCR
- 🙎 **Face Detection** using a Caffe model
- 🧼 **Image Preprocessing**: shadow removal, background clearing, skew correction
- 📊 **Excel Export**: Results saved to `mrz_results.xlsx` with formatted output
- 🔁 Automatically creates backups if Excel file access fails

---

## 📁 Project Structure

```
ai-powered-mrz-passport-reader/
│
├── input_images/                  # Folder containing passport images
├── weights/
│   ├── face_detector/             # Caffe model for face detection
│   └── mrz_detector/              # TFLite model for MRZ segmentation
│
├── mrz_reader/                    # Core processing module
├── main.py                        # 🔁 Main batch processing script
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── .gitignore
```

---

## 📦 Installation

### Requirements

- Python 3.10+
- Recommended: Create and activate a virtual environment

### Setup

```bash
git clone https://github.com/AkramUllahKhan/ai-powered-mrz-passport-reader.git
cd ai-powered-mrz-passport-reader
pip install -r requirements.txt
```

---

## 📂 How to Use

1. Add all your passport images (`.jpg`, `.jpeg`, `.png`) to the `input_images/` folder.

2. Place model weights (Optional):

```
weights/
├── face_detector/
│   ├── deploy.prototxt
│   └── res10_300x300_ssd_iter_140000.caffemodel
├── mrz_detector/
│   └── mrz_seg.tflite
```

3. Run the script:

```bash
python main.py
```

4. Output will be saved to:

```
mrz_results.xlsx
```

---

## 📤 Output Format (Excel)

| Passport Image Path | MRZ Text | Confidence |
|---------------------|----------|------------|
| ./input_images/img1.jpg | P<PAK...ULLAH<<AKRAM... | 0.91 |

If any error occurs while processing an image, it logs the error in the MRZ column with `0` confidence.

---

## 🌍 Sample MRZ (Pakistani Passport Example)

```
P<PAKKHAN<<AKRAM<ULLAH<<<<<<<<<<<<<<<<<<<<<<<<
CN9876543<PAK9901019M2501013<<<<<<<<<<<<<<08
```

---

## 📊 Technologies Used

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — For text extraction
- [OpenCV](https://opencv.org/) — For face detection and image processing
- [TensorFlow Lite](https://www.tensorflow.org/lite) — For MRZ segmentation
- [Caffe](https://caffe.berkeleyvision.org/) — For face detection
- [Pandas](https://pandas.pydata.org/) — Excel data handling
- [XlsxWriter](https://pypi.org/project/XlsxWriter/) + [openpyxl](https://openpyxl.readthedocs.io/) — Excel writing/formatting
- [TQDM](https://tqdm.github.io/) — CLI progress bar

---

## 📝 License

This project is licensed under the MIT License.  
Please contact the author for commercial use or adaptation.

---

## 👤 Author

**Akram Ullah Khan**  
🎓 CS Graduate – UET Peshawar  
📍 Developed for **MORA** (Ministry of Religious Affairs)  
🔗 [GitHub](https://github.com/AkramUllahKhan)

---

## 💬 Feedback & Contributions

- Found a bug? Open an [issue](https://github.com/AkramUllahKhan/ai-powered-mrz-passport-reader/issues)
- Want to contribute? Fork the repo and send a pull request!
---