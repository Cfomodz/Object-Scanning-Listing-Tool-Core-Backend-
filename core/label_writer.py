from abc import ABC, abstractmethod
from typing import Any, Optional
import os
import barcode
from barcode.writer import ImageWriter

try:
    import win32print
    import win32api
    WINDOWS_PRINTING = True
except ImportError:
    WINDOWS_PRINTING = False

class LabelWriter(ABC):
    """
    Abstract base class for generating and printing labels for inventory objects (any type).
    Provides static helpers for barcode generation.
    OS-agnostic: printing is a no-op or message on non-Windows systems.
    """
    @staticmethod
    def create_barcode(barcode_data: str) -> str:
        """
        Generate a barcode image and return its file path.
        """
        ean = barcode.get('code128', barcode_data, writer=ImageWriter())
        barcode_path = f"barcode_{barcode_data}"
        ean.save(barcode_path)
        return f"{barcode_path}.png"

    @abstractmethod
    def create_label_content(self, item: Any) -> str:
        """
        Generate the label content for the given object (any type).
        """
        pass

    @abstractmethod
    def create_label_document(self, item: Any, **kwargs) -> str:
        """
        Create a label document (e.g., PDF) and return its file path.
        """
        pass

    def print_label(self, pdf_file_path: str, printer_name: str) -> None:
        """
        Print a label. On Windows, attempts to print; on other OSes, prints a message.
        """
        absolute_path = os.path.abspath(pdf_file_path)
        if not os.path.exists(absolute_path):
            print(f"File not found: {absolute_path}")
            return
        if WINDOWS_PRINTING:
            try:
                win32api.ShellExecute(
                    0,
                    "print",
                    absolute_path,
                    f'/d:"{printer_name}"',
                    ".",
                    0
                )
                print(f"Sent print job for {absolute_path} to printer {printer_name}")
            except Exception as e:
                print(f"Failed to print {absolute_path} to printer {printer_name}. Error: {e}")
        else:
            print(f"[PRINT] Would print {pdf_file_path} to {printer_name} (printing is only available on Windows with win32api)") 