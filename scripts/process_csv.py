
class csvDirectory:
    def __init__(self, period: int=5, rf: float= 0.04, interval: str ="1wk", confidence_level: float = 0.05, exclude_warrant:bool=True):
        self.bursa_companies_csv = f"./data/bursa_companies_p{int(period)}_rf{rf}_int{interval}_cl{float(confidence_level)}.csv"
        self.sector_overview_csv = f"./data/sector_overview_p{int(period)}_rf{rf}_int{interval}_cl{float(confidence_level)}.csv"
        self.subsector_overview_csv = f"./data/subsector_overview_p{int(period)}_rf{rf}_int{interval}_cl{float(confidence_level)}.csv"