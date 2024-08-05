class Covid():
    def __init__(self, id):
        self.id = id
        self.results = ""
        self.rox = None
        self.fam = None
        self.cy5 = None


    def calculate_results(self):

            # Check if the fam and rox attributes have been set.
        if self.fam is None or self.rox is None or self.cy5 is None:
            return

            # Convert the fam and rox attributes to floats before subtracting them.
        fam_float = float(self.fam)
        rox_float = float(self.rox)
        cy5_float = float(self.cy5)

        if self.fam - self.rox < -2:
            self.results = "Flagged"
        elif self.cy5 > 35:
            self.results = "Invalid"
        elif self.rox < 40.0 or self.fam < 40.0:
            self.results = "Positive"
        else:
            self.results = "Negative"







