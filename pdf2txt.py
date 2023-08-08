from PyPDF2 import PdfReader

class PDFProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.reader = PdfReader(self.pdf_path)
        self.num_pages = len(self.reader.pages)
    
    def get_text_from_page(self, page_number):
        if 0 <= page_number < self.num_pages:
            page = self.reader.pages[page_number]
            extracted_text = page.extract_text()
            if  extracted_text == None or len(extracted_text)< 10:
                print("Either the pdf is too short or is not readable. Try again...")
                return 0
            else:
                return extracted_text
        else:
            return "Invalid page number"
    
    def get_num_pages(self):
        return self.num_pages

# Example usage
if __name__ == "__main__":
    pdf_path = "D:\Resume (2).pdf"
    # pdf_path = "C:/Users/HP/Desktop/Doc1.pdf"
    
    pdf_processor = PDFProcessor(pdf_path)
    
    num_pages = pdf_processor.get_num_pages()    
    page_number = 0
    page_text = pdf_processor.get_text_from_page(page_number)
    # print(f"Text from page {page_number}:\n{page_text}")
    if page_text != 0:
        print(f"Text from page {page_number}:\n{page_text}")