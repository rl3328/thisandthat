import matplotlib.pyplot as plt
import math
import os
import numpy as np
def preview_pdfs(pdf_directory, figsize=(200, 200), max_cols=20, dpi=72):
    """
    Display multiple PDF files in a grid layout.
    Parameters:
    pdf_directory (str): Directory containing PDF files
    figsize (tuple): Size of the entire figure (width, height)
    max_cols (int): Maximum number of columns in the grid
    dpi (int): Resolution for PDF rendering
    """
    # Get list of PDF files
    pdf_files = [f for f in os.listdir(pdf_directory) if f.lower().endswith('.pdf')]
    n_plots = len(pdf_files)
    n_cols = min(max_cols, n_plots)
    n_rows = math.ceil(n_plots / n_cols)
    # Create figure
    fig = plt.figure(figsize=figsize)
    plt.gcf().texts.clear()
    plt.gcf().canvas.manager.set_window_title('')
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    # Create each subplot
    for i, pdf_file in enumerate(pdf_files):
        try:
            # Open PDF using PyMuPDF
            pdf_path = os.path.join(pdf_directory, pdf_file)
            doc = fitz.open(pdf_path)
            # Get first page
            page = doc[0]
            # Convert to image
            pix = page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n
            )
            # Create subplot
            ax = plt.subplot(n_rows, n_cols, i + 1)
            ax.imshow(img)
            # ax.set_title(pdf_file[:20] + '...' if len(pdf_file) > 20 else pdf_file)
            ax.axis('off')  # Hide axes
            # Close the document
            doc.close()
        except Exception as e:
            print(f"Error processing {pdf_file}: {str(e)}")
            continue
    plt.tight_layout()
    return fig
# Example usage:
# preview_pdfs("/path/to/your/pdf/directory")
# plt.show()
# Optional: Function to save the preview as an image
def save_pdf_preview(pdf_directory, output_file, **kwargs):
    """
    Create and save a preview of multiple PDFs as an image file.
    Parameters:
    pdf_directory (str): Directory containing PDF files
    output_file (str): Path to save the output image (e.g., 'preview.png')
    **kwargs: Additional arguments to pass to preview_pdfs
    """
    fig = preview_pdfs(pdf_directory, **kwargs)
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Preview saved as {output_file}")
save_pdf_preview("/Users/liruixi/Documents", "output_preview.png")