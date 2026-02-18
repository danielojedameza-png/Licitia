"""PDF document processing"""

try:
    import PyPDF2
    PYPDF2_OK = True
except ImportError:
    PYPDF2_OK = False


class ManejadorDocumentos:
    """PDF document handler"""
    
    def __init__(self, usar_ocr=False):
        self.usar_ocr = usar_ocr
    
    def procesar_pdf(self, ruta_o_bytes, tipo='archivo'):
        """
        Process PDF file and extract text.
        
        Args:
            ruta_o_bytes: File path or bytes
            tipo: 'archivo' for file path, 'bytes' for bytes
            
        Returns:
            dict with extraction results
        """
        if not PYPDF2_OK:
            return {
                'exito': False,
                'error': 'PyPDF2 not installed',
                'texto': ''
            }
        
        try:
            if tipo == 'bytes':
                import io
                pdf_file = io.BytesIO(ruta_o_bytes)
            else:
                pdf_file = open(ruta_o_bytes, 'rb')
            
            reader = PyPDF2.PdfReader(pdf_file)
            texto = []
            
            for pagina in reader.pages:
                texto.append(pagina.extract_text())
            
            if tipo != 'bytes':
                pdf_file.close()
            
            return {
                'exito': True,
                'texto': '\n'.join(texto),
                'num_paginas': len(reader.pages),
                'metodo_extraccion': 'pypdf2'
            }
        except Exception as e:
            return {
                'exito': False,
                'error': str(e),
                'texto': ''
            }


# Alias for compatibility
PDFHandler = ManejadorDocumentos
