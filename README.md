# DocuScan Tool

## Overview
The DocuScan Tool is a Python script that allows you to automatically detect and process documents in images. It includes features such as document edge detection, manual corner selection, and perspective transformation for document processing. Additionally, it provides the ability to check if the detected document size matches standard official document sizes for printing.

## Features
- Automatic document edge detection using Canny edge detection.
- Manual selection of document corners for precise adjustment.
- Perspective transformation to obtain a "birds-eye view" of the document.
- Real-time display of the document selection and transformation.
- (not done yet) Ability to check if the detected document size matches standard official document sizes for printing on A4 or other paper sizes.

## Usage
1. Replace `path/to/your/image.jpg` with the path to the image containing the document you want to process.

```python
image = cv2.imread('path/to/your/image.jpg')
```

2. Run the script. This will display the original image with automatic edge detection.

3. Manually select the four corners of the document by clicking near each corner. The script will update the display in real-time to show the selected corners.

4. Press 'q' to exit the corner selection mode when you are done.

5. Press 'p' to apply perspective transformation and display the processed document. You can adjust the transformation until you are satisfied with the result.

6. Close the display window when you are finished processing the document.

7. The script also checks if the processed document size matches standard official document sizes. If a match is found, you can use it as a template for printing on A4 or other paper sizes.

## Requirements
- Python 3
- OpenCV (cv2)
- Numpy

Install the required libraries using pip:

```bash
pip install opencv-python-headless numpy
```

## Contributions
Contributions, suggestions, and improvements to this tool are welcome. Feel free to fork the repository and create pull requests.

## License
This tool is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.
