"""Utilities for integrating PDF generation workers with the Job Manager."""

from .pdf_job_worker import PdfJobWorker, WorkerConfig

__all__ = ["PdfJobWorker", "WorkerConfig"]


