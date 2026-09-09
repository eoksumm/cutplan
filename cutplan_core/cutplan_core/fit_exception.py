"""Raised by a CutAlgorithm when a part cannot be made to fit on the sheet at all."""


class FitException(Exception):
    def __init__(self, part_label: str, message: str):
        super().__init__(message)
        self.part_label = part_label
