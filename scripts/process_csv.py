
class csvDirectory:
    def __init__(self, period: int=5, rf: float= 4.0, interval: str ="1wk", confidence_level: float = 5.0, exclude_warrant:bool=True):
        self.bursa_companies_csv = f"./data/bursa_companies_p{period}_rf{rf}_int{interval}_cl{confidence_level}_exw{exclude_warrant}.csv"
        self.sector_overview_csv = f"./data/sector_overview_p{period}_rf{rf}_int{interval}_cl{confidence_level}_exw{exclude_warrant}.csv"
        self.subsector_overview_csv = f"./data/subsector_overview_p{period}_rf{rf}_int{interval}_cl{confidence_level}_exw{exclude_warrant}.csv"